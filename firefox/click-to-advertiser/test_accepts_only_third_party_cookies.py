#!/usr/bin/env python3

from firefox.firefox import *
from common.adsplog import *
import unittest
import time

class TestFirefoxAcceptOnlyThirdPartyCookies(unittest.TestCase):
    """ Test suite to test a click on an Ad in publisher's website and a redirect to advertiser's website
        with Firefox browser.
        When a user clicks an Ad it is redirected to adsp with a device id in querystring for ALL tests
        in the suite.
        Landing page has a our lib tracker.js, and it triggers a lead automatically.
    """

    def setUp(self):

        time.sleep(5)

        # setup adsp log
        self.adsplog = AdspLog('/home/rsicart/Repo/adsp-front/sd/www2/www/data/access')

        # setup website
        self.url = 'http://www2.adsp.localhost/click.php?id=2763-21915-5069&context-hash=e0ff593dd1fbda31689e7e1826d4e4aef0394f5a&di={}&data=&preurl='
        self.timeout = 4
        self.cookie_name = 'adsp_di'
        self.domains = {'first': 'advertiser.localhost', 'third': '.adsp.localhost'}

        # setup firefox
        profile_name = 'CookiesAll'
        profile_folder = '/home/rsicart/.mozilla/firefox/jl065qo8.CookiesAll'
        self.browser = Firefox(profile_name, profile_folder)

        # flush cookies before browsing
        db_name = 'cookies.sqlite'
        db_table = 'moz_cookies'
        self.cookies = Cookies(profile_folder, db_name, db_table)
        self.cookies.setup()
        self.cookies.flush()
        self.cookies.close()

        # set cookie behavior
        self.browser.setCookieBehavior('all')

        # blacklist first party domain
        db_name = 'permissions.sqlite'
        db_table = 'moz_perms'
        self.blacklist = Blacklist(profile_folder, db_name, db_table)
        self.blacklist.setup()
        self.blacklist.add(self.domains['first'])
        self.blacklist.close()


    #def test_allIsEmpty(self):

    #    # setup querystring
    #    device_id_querystring = '1447344866.44444444-4444-4444-aaaa-444444444444'
    #    url = self.url.format(device_id_querystring)

    #    # http get
    #    self.browser.openUrl(url, self.timeout)

    #    # fetch device ids from cookies
    #    self.cookies.setup()
    #    cookieFirst = self.cookies.get(self.cookie_name, self.domains['first'])
    #    cookieThird = self.cookies.get(self.cookie_name, self.domains['third'])
    #    self.cookies.close()

    #    devicesFirst = []
    #    devicesThird = []
    #    if cookieFirst:
    #        devicesFirst = self.cookies.getDeviceIdsFromCookie(cookieFirst)
    #    if cookieThird:
    #        devicesThird = self.cookies.getDeviceIdsFromCookie(cookieThird)

    #    # fetch device ids from adsp logs
    #    devicesLogs = self.adsplog.getDeviceIds(self.adsplog.getLastLine())

    #    # cookies are not empty
    #    # that's unexpected but amazingly firefox still sets cookie for a blacklisted domain
    #    self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
    #    # cookies are not empty
    #    self.assertNotEqual(len(devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
    #    # original device id from querystring saved in cookies 1st
    #    self.assertIn(device_id_querystring, devicesFirst, 'Original device id from querystring was not found in first party cookies, but it should.')
    #    # original device id from querystring saved in cookies 3rd
    #    self.assertIn(device_id_querystring, devicesThird, 'Original device id from querystring was not found in third party cookies, but it should.')
    #    # all device id is logged (because a device id exists in querystring)
    #    self.assertIn(device_id_querystring, devicesLogs, 'Device ids in adsp logs are different than device ids in cookies.')


    #def test_cookieThirdIsEmpty(self):

    #    # setup querystring
    #    device_id_querystring = '1447344866.44444444-4444-4444-bbbb-444444444444'
    #    url = self.url.format(device_id_querystring)

    #    # fill cookie 1st only
    #    deviceIdA = '1447859209.11111111-1111-1111-bbbb-111111111111'
    #    cookie_value = 'ls=1447859209770|v=1|di={}'.format(deviceIdA)
    #    self.cookies.setup()
    #    self.cookies.set(self.cookie_name, cookie_value, self.domains['first'])
    #    self.cookies.close()

    #    # http get
    #    self.browser.openUrl(url, self.timeout)

    #    # fetch device ids from cookies
    #    self.cookies.setup()
    #    cookieFirst = self.cookies.get(self.cookie_name, self.domains['first'])
    #    cookieThird = self.cookies.get(self.cookie_name, self.domains['third'])
    #    self.cookies.close()

    #    devicesFirst = []
    #    devicesThird = []
    #    if cookieFirst:
    #        devicesFirst = self.cookies.getDeviceIdsFromCookie(cookieFirst)
    #    if cookieThird:
    #        devicesThird = self.cookies.getDeviceIdsFromCookie(cookieThird)

    #    # fetch device ids from adsp logs
    #    devicesLogs = self.adsplog.getDeviceIds(self.adsplog.getLastLine())

    #    # cookies are not empty
    #    self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
    #    # cookies are not empty
    #    self.assertNotEqual(len(devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
    #    # original device id is still there
    #    self.assertIn(deviceIdA, devicesFirst, 'Original device id  was not found in first party cookies, but it should.')
    #    # original device id from querystring prepended to cookies 1st
    #    self.assertIn(device_id_querystring, devicesFirst, 'Original device id from querystring was not found in first party cookies, but it should.')
    #    # original device id from querystring saved in cookies 3rd
    #    self.assertIn(device_id_querystring, devicesThird, 'Original device id  was not found in third party cookies, but it should.')
    #    # all device ids were logged
    #    self.assertIn(deviceIdA, devicesLogs, 'Device ids in adsp logs are different than device ids in cookies.')
    #    self.assertIn(device_id_querystring, devicesLogs, 'Device ids in adsp logs are different than device ids in cookies.')



    def test_cookieFirstIsEmpty(self):
        """
            Device id in click's url querystring will be replaced by device id in third party cookies.
            That's because our adserver, before redirecting the user to advertiser's website, will append
            the most relevant device id.
        """

        # setup querystring
        device_id_querystring = '1447344866.44444444-4444-4444-cccc-444444444444'
        url = self.url.format(device_id_querystring)

        # fill cookie 3rd only
        deviceIdA = '1447859209.33333333-3333-3333-cccc-333333333333'
        cookie_value = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value, self.domains['third'])
        self.cookies.close()

        # http get
        self.browser.openUrl(url, self.timeout)

        # fetch device ids from cookies
        self.cookies.setup()
        cookieFirst = self.cookies.get(self.cookie_name, self.domains['first'])
        cookieThird = self.cookies.get(self.cookie_name, self.domains['third'])
        self.cookies.close()

        devicesFirst = []
        devicesThird = []
        if cookieFirst:
            devicesFirst = self.cookies.getDeviceIdsFromCookie(cookieFirst)
        if cookieThird:
            devicesThird = self.cookies.getDeviceIdsFromCookie(cookieThird)

        # fetch device ids from adsp logs
        devicesLogs = self.adsplog.getDeviceIds(self.adsplog.getLastLine())

        # cookies are not empty
        self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
        self.assertNotEqual(len(devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # original device id in cookies third is still there
        self.assertIn(deviceIdA, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # cookie 1st restored from cookie 3rd
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, but it should be there.')
        # original device id in querystring is not prepended to cookie 1st
        self.assertNotIn(device_id_querystring, devicesFirst, 'Original device id from querystring was found in first party cookies, but it should not be there because third party cookies were used instead.')
        # device id is logged
        self.assertIn(deviceIdA, devicesLogs, 'Original device ids was not found in adsp logs.')
        # device id is not logged
        self.assertNotIn(device_id_querystring, devicesLogs, 'Device ids in adsp logs are different than device ids in querystring.')


    #def test_cookiesContainSameDevice(self):

    #    # setup querystring
    #    device_id_querystring = '1447344866.44444444-4444-4444-dddd-444444444444'
    #    url = self.url.format(device_id_querystring)

    #    deviceIdA = '1447859209.11111111-3333-1111-dddd-111111111111'
    #    cookie_value_first = 'ls=1447859209000|v=1|di={}'.format(deviceIdA)
    #    cookie_value_third = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(deviceIdA)
    #    self.cookies.setup()
    #    self.cookies.set(self.cookie_name, cookie_value_first, self.domains['first'])
    #    self.cookies.set(self.cookie_name, cookie_value_third, self.domains['third'])
    #    self.cookies.close()

    #    # http get
    #    self.browser.openUrl(url, self.timeout)

    #    # fetch device ids from cookies
    #    self.cookies.setup()
    #    cookieFirst = self.cookies.get(self.cookie_name, self.domains['first'])
    #    cookieThird = self.cookies.get(self.cookie_name, self.domains['third'])
    #    self.cookies.close()

    #    devicesFirst = []
    #    devicesThird = []
    #    if cookieFirst:
    #        devicesFirst = self.cookies.getDeviceIdsFromCookie(cookieFirst)
    #    if cookieThird:
    #        devicesThird = self.cookies.getDeviceIdsFromCookie(cookieThird)

    #    # fetch device ids from adsp logs
    #    devicesLogs = self.adsplog.getDeviceIds(self.adsplog.getLastLine())


    #    # cookies are empty
    #    self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
    #    self.assertNotEqual(len(devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
    #    # original device id in cookies third is still there
    #    self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
    #    self.assertIn(deviceIdA, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
    #    # original device id in querystring not prepended to cookies 1st
    #    self.assertNotIn(device_id_querystring, devicesFirst, 'Original device id from querystring was found in first party cookies, but it should not be there because all cookies are disabled.')
    #    # original device id from cookies was not logged
    #    self.assertNotIn(deviceIdA, devicesLogs, 'Original device ids from cookies were not found in adsp logs.')
    #    # device id is logged (because a device id exists in querystring)
    #    self.assertIn(device_id_querystring, devicesLogs, 'Device ids in adsp logs are different than device ids in querystring.')


    #def test_cookiesContainDifferentDevices(self):

    #    # setup querystring
    #    device_id_querystring = '1447344866.44444444-4444-4444-eeee-444444444444'
    #    url = self.url.format(device_id_querystring)

    #    deviceIdA = '1447859209.11111111-1111-1111-eeee-111111111111'
    #    cookie_value_first = 'ls=1447859209000|v=1|di={}'.format(deviceIdA)
    #    deviceIdB = '1447859209.33333333-3333-3333-eeee-333333333333'
    #    cookie_value_third = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(deviceIdB)
    #    self.cookies.setup()
    #    self.cookies.set(self.cookie_name, cookie_value_first, self.domains['first'])
    #    self.cookies.set(self.cookie_name, cookie_value_third, self.domains['third'])
    #    self.cookies.close()

    #    # http get
    #    self.browser.openUrl(url, self.timeout)

    #    # fetch device ids from cookies
    #    self.cookies.setup()
    #    cookieFirst = self.cookies.get(self.cookie_name, self.domains['first'])
    #    cookieThird = self.cookies.get(self.cookie_name, self.domains['third'])
    #    self.cookies.close()

    #    devicesFirst = []
    #    devicesThird = []
    #    if cookieFirst:
    #        devicesFirst = self.cookies.getDeviceIdsFromCookie(cookieFirst)
    #    if cookieThird:
    #        devicesThird = self.cookies.getDeviceIdsFromCookie(cookieThird)

    #    # fetch device ids from adsp logs
    #    devicesLogs = self.adsplog.getDeviceIds(self.adsplog.getLastLine())

    #    # cookies are empty
    #    self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
    #    self.assertNotEqual(len(devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
    #    # original device id in cookies is still there
    #    self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
    #    self.assertIn(deviceIdB, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
    #    # device id from cookies 3rd not prepended to cookies 1st
    #    self.assertNotIn(deviceIdB, devicesFirst, 'Original device id from cookies 3rd was found in first party cookies, but it should not be there because all cookies are disabled.')
    #    # original device id in querystring not prepended to cookies 1st
    #    self.assertNotIn(device_id_querystring, devicesFirst, 'Original device id from querystring was found in first party cookies, but it should not be there because all cookies are disabled.')
    #    # original device id from first party cookies was not logged
    #    self.assertNotIn(deviceIdA, devicesLogs, 'Original device ids was not found in adsp logs.')
    #    # original device id from third party cookies was not logged
    #    self.assertNotIn(deviceIdB, devicesLogs, 'Original device ids was not found in adsp logs.')
    #    # device id is logged (because a device id exists in querystring)
    #    self.assertIn(device_id_querystring, devicesLogs, 'Device ids in adsp logs are different than device ids in querystring.')


    def tearDown(self):
        # remove blacklist
        self.blacklist.setup()
        self.blacklist.flush()
        self.blacklist.close()
        # restore cookie behavior
        self.browser.restorePreferences(self.browser.prefs_file)


if __name__ == '__main__':
        unittest.main()
