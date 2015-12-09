from common import database
from sqlite3 import Binary
import subprocess
import sys
import re
import shutil
from datetime import datetime, timedelta, timezone
import urllib.parse
import json
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2


class Cookies(database.Database):
    def __init__(self, *args):
        super().__init__(*args)
        self.salt = b'saltysalt'
        self.iv = b' ' * 16
        self.length = 16
        self.password = 'peanuts'.encode('utf8')
        self.iterations = 1
        self.key = PBKDF2(self.password, self.salt, self.length, self.iterations)

    def delete(self, name, domain):
        query = 'DELETE FROM {} WHERE name=? AND host=?;'.format(self.db_table)
        values = (name, domain)
        self.db_cursor.execute(query, values);


    def get(self, name, domain):
        # domain
        if 'http' not in domain:
            domain = 'http://{}'.format(domain)
        parsed_domain = urllib.parse.urlparse(domain).netloc 
        host_key = '.'.join(parsed_domain.split('.')[-2:])

        query = 'SELECT name, host_key, value, encrypted_value FROM {} WHERE name=? AND host_key LIKE ?;'.format(self.db_table)
        values = (name, '%{}'.format(host_key))
        result = self.db_cursor.execute(query, values).fetchone()

        cookie = {}
        if result:
            (cookie_name, cookie_domain, cookie_value, cookie_encrypted_value) = result
            cookie = {
                'name': cookie_name,
                'domain': cookie_domain,
                'value': cookie_value,
                'encrypted_value': cookie_encrypted_value,
            }

        # decrypt
        if cookie:
            decrypted_value = self.decrypt(cookie['encrypted_value'])
            cookie['value'] = decrypted_value

        return cookie


    def set(self, name, value, domain, path='/', creation_utc=None, expires_utc=None, secure=0, httponly=0, last_access_utc=None, has_expires=1, persistent=1, priority=1, firstpartyonly=0):

        # [Google Chrome's] timestamp is formatted as the number of microseconds since January, 1601"
        start_date = datetime(1601, 1, 1, hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)

        a_year = timedelta(days=365)
        today = datetime.now(tz=timezone.utc)

        # domain
        begins_with_point = domain[0] == '.'
        if 'http' not in domain:
            domain = 'http://{}'.format(domain)
        parsed_domain = urllib.parse.urlparse(domain).netloc 
        host_key = '.'.join(parsed_domain.split('.')[-2:])
        if begins_with_point:
            host_key = '.{}'.format(host_key)


        if expires_utc is None:
            expires_utc = int(((today + a_year) - start_date).total_seconds() * 1000000) # in microseconds
            expires_utc = expires_utc * 10  # move floating point to the right

        if last_access_utc is None:
            last_access_utc = (today - start_date).total_seconds() * 1000000 # in microseconds
            last_access_utc = last_access_utc * 10  # move floating point to the right

        if creation_utc is None:
            creation_utc = last_access_utc # in microseconds

        # encrypt
        encrypted_value = self.encrypt(value)

        query = """
                INSERT INTO {}(creation_utc, host_key, name, value, path, expires_utc, secure, httponly, last_access_utc, has_expires, persistent, priority, encrypted_value, firstpartyonly) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """.format(self.db_table)
        values = (creation_utc, host_key, name, value, path, expires_utc, secure, httponly, last_access_utc, has_expires, persistent, priority, Binary(encrypted_value), firstpartyonly)
        cookie = self.db_cursor.execute(query, values);
        self.db_connection.commit()


    def encrypt(self, decrypted_value):

        if not decrypted_value:
            raise ValueError('Cookies.encrypt(): decrypted_value argument not valid')

        # work with bytes
        decrypted_value = decrypted_value.encode('utf-8')

        # add padding
        length = 16 - (len(decrypted_value) % 16)
        decrypted_value += bytes([length])*length

        cipher = AES.new(self.key, AES.MODE_CBC, IV=self.iv)
        encrypted = cipher.encrypt(decrypted_value)

        # add prefix
        encrypted_value = b"".join([b"v10", encrypted])

        return encrypted_value


    def decrypt(self, encrypted_value):
        # Encrypted cookies should be prefixed with 'v10' according to the
        # Chromium code. Strip it off.
        encrypted_value = encrypted_value[3:]

        # Strip padding by taking off number indicated by padding
        # eg if last is '\x0e' then ord('\x0e') == 14, so take off 14.
        def clean(x):
            return x[:-x[-1]].decode('utf8')

        cipher = AES.new(self.key, AES.MODE_CBC, IV=self.iv)
        decrypted = cipher.decrypt(encrypted_value)

        return clean(decrypted)


    def getDeviceIdsFromCookie(self, cookie):
        rawValue = cookie['value']
        separator_first = '='
        separator_third = '%3D'
        pattern = 'di(?:=|%3D)([0-9]+\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})+'

        p = re.compile(pattern)
        devices = p.findall(rawValue)

        return devices



class Chromium:

    def __init__(self, profile_folder):
        self.profile_folder = profile_folder
        self.prefs_file = '{}/Default/Preferences'.format(profile_folder)
        self.prefs = None
        self.cookie_behavior = None
        self.command = '/usr/bin/chromium-browser --user-data-dir={}'.format(self.profile_folder)


    def openUrl(self, target_url, timeout=3):
        cmd = '{} {}'.format(self.command, target_url)
        proc = subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.terminate()


    def close(self):
        if self.process:
            self.process.terminate()


    def loadPreferences(self):
        if not self.prefs:
            with open(self.prefs_file, mode='r', encoding='utf-8') as f:
                self.prefs = json.load(f)


    def savePreferences(self):
        if self.prefs:
            with open(self.prefs_file, mode='w', encoding='utf-8') as f:
                json.dump(self.prefs, f)


    def blacklist(self, domain=None):
        """ Blacklist a domain
        :param domain: string domain to blacklist
        """

        if not domain:
            raise ValueError("Chromium.blacklist(): domain argument must be a valid domain")

        if not self.prefs:
            self.loadPreferences()

        # be sure that content settings keys exist
        if 'cookies' not in self.prefs['profile']['content_settings']['exceptions'].keys():
            self.prefs['profile']['content_settings']['exceptions'].update({'cookies': {}})

        if 'pattern_pairs' not in self.prefs['profile']['content_settings'].keys():
            self.prefs['profile']['content_settings'].update({'pattern_pairs': {}})

        if 'http' not in domain:
            domain = 'http://{}'.format(domain)
        parsed_domain = urllib.parse.urlparse(domain).netloc 
        base_domain = '.'.join(parsed_domain.split('.')[-2:])

        self.prefs['profile']['content_settings']['exceptions']['cookies'].update({'{},*'.format(base_domain):{'setting': 2}})
        self.prefs['profile']['content_settings']['pattern_pairs'].update({'{},*'.format(base_domain):{'cookies': 2}})

        self.savePreferences()


    def flushBlacklist(self):
        """ Flushes existing blacklist
        """

        if not self.prefs:
            self.loadPreferences()

        # be sure that content settings keys exist
        if 'cookies' not in self.prefs['profile']['content_settings']['exceptions'].keys():
            self.prefs['profile']['content_settings']['exceptions'].update({'cookies': {}})
        else:
            self.prefs['profile']['content_settings']['exceptions']['cookies'] = {}

        if 'pattern_pairs' not in self.prefs['profile']['content_settings'].keys():
            self.prefs['profile']['content_settings'].update({'pattern_pairs': {}})
        else:
            self.prefs['profile']['content_settings']['pattern_pairs'] = {}

        self.savePreferences()


    def setCookieBehavior(self, cookie_behavior=None):
        """ Sets browser's cookies privacy settings
        :param cookie_behavior: string (all|only_1|visited|nothing)
        :param blacklist_domain: string domain to blacklist
        """
        allowed = ['all', 'only_1', 'nothing']

        behavior = 'all'
        if cookie_behavior in allowed:
            behavior = cookie_behavior

        self.backupPreferences(self.prefs_file);

        if not self.prefs:
            self.loadPreferences()

        # be sure that content settings keys exist
        if 'block_third_party_cookies' not in self.prefs['profile'].keys():
            self.prefs['profile'].update({'block_third_party_cookies': False})

        #if 'default_content_setting_values' not in self.prefs['profile'].keys():
        self.prefs['profile'].update({'default_content_setting_values': {}})

        #if 'default_content_settings' not in self.prefs['profile'].keys():
        self.prefs['profile'].update({'default_content_settings': {}})

        # third party cookies
        if behavior == 'only_1':
            self.prefs['profile']['block_third_party_cookies'] = True
        else:
            self.prefs['profile']['block_third_party_cookies'] = False

        # block all
        if behavior == 'nothing':
            self.prefs['profile']['default_content_setting_values']['cookies'] = 2
            self.prefs['profile']['default_content_settings']['cookies'] = 2

        self.savePreferences()


    def backupPreferences(self, filename):
        """ Copies a file to the same location with a trailing .bak extension
        :param filename: full path to file being backuped
        """
        shutil.copy(filename, '{}.bak'.format(filename))


    def restorePreferences(self, filename):
        """ Copies a backuped file to the same location without the trailing .bak extension
        :param filename: full path to file being restored
        """
        shutil.copy('{}.bak'.format(filename), filename)


