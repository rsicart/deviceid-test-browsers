#!/usr/bin/env python3

from firefox.firefox import *
from common.adsplog import *
import unittest
import time

class TestFirefoxAcceptAllCookies(unittest.TestCase):
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


    def test_allIsEmpty(self):

        # setup querystring
        device_id_querystring = '1447344866.44444444-4444-4444-aaaa-444444444444'
        url = self.url.format(device_id_querystring)

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

        # cookies not empty
        self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
        self.assertNotEqual(len(devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # original device id from querystring is appended to cookie 1st
        self.assertIn(device_id_querystring, devicesFirst, 'Original device id from querystring was not found in first party cookies, but it should.')
        # original device id from querystring saved in cookie 3rd
        self.assertEqual(devicesFirst, devicesThird, 'Device ids found are different.')
        # all device ids are logged
        self.assertEqual(devicesFirst, devicesLogs, 'Device ids in adsp logs are different than device ids in cookies.')


    def test_cookieThirdIsEmpty(self):

        # setup querystring
        device_id_querystring = '1447344866.44444444-4444-4444-bbbb-444444444444'
        url = self.url.format(device_id_querystring)

        # fill cookie 1st only
        deviceIdA = '1447859209.11111111-1111-1111-bbbb-111111111111'
        cookie_value = 'ls=1447859209770|v=1|di={}'.format(deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value, self.domains['first'])
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

        # cookies not empty
        self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
        self.assertNotEqual(len(devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # original device id from querystring is appended to cookie 1st
        self.assertIn(device_id_querystring, devicesFirst, 'Original device id from querystring was not found in first party cookies, but it should.')
        # original device id from querystring saved in cookie 3rd
        self.assertIn(device_id_querystring, devicesThird, 'Original device id from querystring was not found in third party cookies, but it should.')
        # original device id from cookie 1st still there
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        # original device id from querystring is the first one in cookies 1st and 3rd (because 3rd were empty)
        self.assertEqual(devicesFirst[0], devicesThird[0], 'Device ids found are different.')
        self.assertEqual(devicesFirst, devicesLogs, 'Device ids in adsp logs are different than device ids in cookies.')


    def test_cookieFirstIsEmpty(self):

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

        # cookies not empty
        self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
        self.assertNotEqual(len(devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # original device id in cookies third is still there
        self.assertIn(deviceIdA, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # cookies 1st restored from cookie 3rd
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        # original device id in querystring ignored because 3rd party cookies are enabled
        self.assertNotIn(device_id_querystring, devicesFirst, 'Original device id from querystring was found in first party cookies, but it should not be there. When third party cookies are enabled, we use it as main option.')
        # original device id is the first one, because cookies 3rd have de highest priority
        self.assertEqual(devicesFirst[0], devicesThird[0], 'Device ids found are different.')
        # original device id from third party cookies was logged
        self.assertIn(deviceIdA, devicesLogs, 'Original device ids was not found in adsp logs.')


    def test_cookiesContainSameDevice(self):

        # setup querystring
        device_id_querystring = '1447344866.44444444-4444-4444-dddd-444444444444'
        url = self.url.format(device_id_querystring)

        deviceIdA = '1447859209.11111111-3333-1111-dddd-111111111111'
        cookie_value_first = 'ls=1447859209000|v=1|di={}'.format(deviceIdA)
        cookie_value_third = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value_first, self.domains['first'])
        self.cookies.set(self.cookie_name, cookie_value_third, self.domains['third'])
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

        # cookies not empty
        self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
        self.assertNotEqual(len(devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # original device id in cookies first is still there
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        # original device id in cookies third is still there
        self.assertIn(deviceIdA, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # original device id in querystring ignored because 3rd party cookies are enabled
        self.assertNotIn(device_id_querystring, devicesFirst, 'Original device id from querystring was found in first party cookies, but it should not be there. When third party cookies are enabled, we use it as main option.')
        # original device id is the first one, because cookies 3rd have de highest priority
        self.assertEqual(devicesFirst[0], devicesThird[0], 'Device ids found are different.')
        # original device id is logged
        self.assertIn(deviceIdA, devicesLogs, 'Original device id was not found in adsp logs.')


    def test_cookiesContainDifferentDevices(self):

        # setup querystring
        device_id_querystring = '1447344866.44444444-4444-4444-eeee-444444444444'
        url = self.url.format(device_id_querystring)

        deviceIdA = '1447859209.11111111-1111-1111-eeee-111111111111'
        cookie_value_first = 'ls=1447859209000|v=1|di={}'.format(deviceIdA)
        deviceIdB = '1447859209.33333333-3333-3333-eeee-333333333333'
        cookie_value_third = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(deviceIdB)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value_first, self.domains['first'])
        self.cookies.set(self.cookie_name, cookie_value_third, self.domains['third'])
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

        # cookies not empty
        self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
        self.assertNotEqual(len(devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # original device id in cookies first is still there
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        # original device id in cookies third is still there
        self.assertIn(deviceIdB, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        self.assertIn(deviceIdB, devicesFirst, 'Original device id from third party cookies was not found in first party cookies, but it should be in.')
        # original device id in querystring ignored because 3rd party cookies are enabled
        self.assertNotIn(device_id_querystring, devicesFirst, 'Original device id from querystring was found in first party cookies, but it should not be there. When third party cookies are enabled, we use it as main option.')
        # original device id is the first one, because cookies 3rd have de highest priority
        self.assertEqual(devicesFirst[0], devicesThird[0], 'Device ids found are different.')
        # all device ids were logged
        self.assertIn(deviceIdA, devicesLogs, 'Original device id from cookie first was not found in adsp logs.')
        self.assertIn(deviceIdB, devicesLogs, 'Original device id from cookie third was not found in adsp logs.')


    def tearDown(self):
        # restore cookie behavior
        self.browser.restorePreferences(self.browser.prefs_file)




if __name__ == '__main__':
        unittest.main()
