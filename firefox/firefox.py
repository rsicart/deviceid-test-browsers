import sqlite3
import subprocess
import sys
import re
import shutil
from datetime import datetime, timedelta

class Database:

    def __init__(self, folder, db_name, db_table):
        self.folder = folder
        self.db_name = db_name
        self.db_table = db_table
        self.db_connection = None
        self.db_cursor = None


    def setup(self):
        self.db_connection = sqlite3.connect('%s/%s' % (self.folder, self.db_name))
        self.db_cursor = self.db_connection.cursor()


    def close(self):
        if self.db_connection:
            self.db_cursor = None
            self.db_connection.close()
            self.db_connection = None


    def flush(self):
        query = 'DELETE FROM {};'.format(self.db_table)
        self.db_cursor.execute(query);
        self.db_connection.commit()


    def __del__(self):
        if self.db_connection:
            self.db_connection.close()



class Cookies(Database):

    def delete(self, name, domain):
        query = 'DELETE FROM {} WHERE name=? AND host=?;'.format(self.db_table)
        values = (name, domain)
        self.db_cursor.execute(query, values);


    def get(self, name, domain):
        query = 'SELECT * FROM {} WHERE name=? AND host=?;'.format(self.db_table)
        values = (name, domain)
        cookie = self.db_cursor.execute(query, values).fetchone();
        return cookie


    def set(self, name, value, domain, appId=0, inBrowserElement=0, path='/', expiry=None, lastAccessed=None, creationTime=None, isSecure=0, isHttpOnly=0):
        """

        """
        a_year = timedelta(days=365)
        today = datetime.today()

        baseDomain = domain
        if domain[0] == '.':
            baseDomain = domain[1:]

        if expiry is None:
            expiry = int((today + a_year).timestamp())

        if lastAccessed is None:
            lastAccessed = today.timestamp() * 1000000 # in microseconds

        if creationTime is None:
            creationTime = lastAccessed # in microseconds

        query = 'INSERT INTO {}(baseDomain, appId, inBrowserElement, name, value, host, path, expiry, lastAccessed, creationTime, isSecure, isHttpOnly) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'.format(self.db_table)
        values = (baseDomain, appId, inBrowserElement, name, value, domain, path, expiry, lastAccessed, creationTime, isSecure, isHttpOnly)
        cookie = self.db_cursor.execute(query, values);
        self.db_connection.commit()


    def getDeviceIdsFromCookie(self, cookie):
        rawValue = cookie[5]
        separator_first = '='
        separator_third = '%3D'
        pattern = 'di(?:=|%3D)([0-9]+\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})+'

        p = re.compile(pattern)
        devices = p.findall(rawValue)

        return devices



class Blacklist(Database):

    def add(self, domain, type='cookie', permission=2, expireType=0, expireTime=0, modificationTime=None):
        """ Adds a domain to blacklist
        :param domain: domain to be blacklisted
        :param type: string permission type, default value 'cookie'
        :param permission: integer permission allow or deny, by default deny (2)
        :param expireType: integer, default 0
        :param expireTime: integer, default 0
        :param modificationTime: integer in milliseconds, default None
        """

        today = datetime.today()

        if modificationTime is None:
            modificationTime = int(today.timestamp() * 1000) # in milliseconds

        query = 'INSERT INTO {}(origin, type, permission, expireType, expireTime, modificationTime) VALUES (?, ?, ?, ?, ?, ?);'.format(self.db_table)
        values = (domain, type, permission, expireType, expireTime, modificationTime)
        cookie = self.db_cursor.execute(query, values);
        self.db_connection.commit()


class Firefox:

    def __init__(self, profile_name, profile_folder, cookie_behavior=None):
        self.profile_name = profile_name
        self.profile_folder = profile_folder
        self.prefs_file = '{}/prefs.js'.format(profile_folder)
        self.cookie_behavior = cookie_behavior
        self.command = '/usr/bin/firefox -P {} -new-window'.format(self.profile_name)


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


    def setCookieBehavior(self, cookie_behavior=None):
        """ Sets browser's cookies privacy settings
        :param cookie_behavior: string (all|only_1|visited|nothing)
        """
        allowed = {'all': None, 'only_1': 1, 'visited': 3, 'nothing': 2,}

        behavior = allowed['all']
        if cookie_behavior in allowed.keys():
            behavior = allowed[cookie_behavior]

        self.backupPreferences(self.prefs_file);

        delete_line = "network.cookie.cookieBehavior"
        self.deleteLine(self.prefs_file, delete_line)

        if behavior:
            append_line = 'user_pref("network.cookie.cookieBehavior", {});'.format(behavior)
            self.appendLine(self.prefs_file, append_line)


    def deleteLine(self, filename, match_string):
        """ Delete matching line from a file
        :param filename: full path to file being modified
        :param match_string: string to search in line that has to be deleted
        """
        with open(filename, 'r') as f:
            lines = f.readlines()

        with open(filename, 'w') as f:
            for line in lines:
                if match_string not in line:
                    f.write(line)


    def appendLine(self, filename, line):
        """ Appends a line to a file
        :param filename: full path to file being modified
        :param line: line to append
        """
        with open(filename, 'a') as f:
            f.write(line)


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



