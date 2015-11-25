#!/usr/bin/env python3

from firefox import *
from common.adsplog import *
import unittest

class TestFirefoxAcceptAllCookies(unittest.TestCase):
    """ Test suite to test a display in a publisher's website with Firefox browser.
    """

    def setUp(self):
        # setup adsp log
        self.adsplog = AdspLog('/home/rsicart/Repo/adsp-front/sd/www2/www/data/access')

        # setup website
        self.url = 'http://publisher.localhost/publisher.html'
        self.timeout = 3
        self.cookie_name = 'adsp_di'
        self.domains = {'first': 'publisher.localhost', 'third': '.adsp.localhost'}

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
        # http get
        self.browser.openUrl(self.url, self.timeout)

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
        # cookies contain same device id
        self.assertEqual(devicesFirst, devicesThird, 'Device ids found are different.')
        # device id is logged
        self.assertEqual(devicesFirst, devicesLogs, 'Device ids in adsp logs are different than device ids in cookies.')


    def test_cookieThirdIsEmpty(self):
        # fill cookie 1st only
        deviceIdA = '1447859209.11111111-1111-1111-bbbb-111111111111'
        cookie_value = 'ls=1447859209770|v=1|di={}'.format(deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value, self.domains['first'])
        self.cookies.close()

        # http get
        self.browser.openUrl(self.url, self.timeout)

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
        # original device id is still there
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        # cookie 3rd is restored from cookie 1st
        self.assertEqual(devicesFirst, devicesThird, 'Device ids found are different.')
        # device id is logged
        self.assertIn(deviceIdA, devicesLogs, 'Original device ids was not found in adsp logs.')


    def test_cookieFirstIsEmpty(self):
        # fill cookie 3rd only
        deviceIdA = '1447859209.33333333-3333-3333-cccc-333333333333'
        cookie_value = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value, self.domains['third'])
        self.cookies.close()

        # http get
        self.browser.openUrl(self.url, self.timeout)

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
        # original device id is still there
        self.assertIn(deviceIdA, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # cookie 1st is restored from cookie 3rd
        self.assertEqual(devicesFirst, devicesThird, 'Device ids found are different.')
        # device id is logged
        self.assertIn(deviceIdA, devicesLogs, 'Original device ids was not found in adsp logs.')


    def test_cookiesContainSameDevice(self):
        deviceIdA = '1447859209.11111111-3333-1111-dddd-111111111111'
        cookie_value_first = 'ls=1447859209000|v=1|di={}'.format(deviceIdA)
        cookie_value_third = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value_first, self.domains['first'])
        self.cookies.set(self.cookie_name, cookie_value_third, self.domains['third'])
        self.cookies.close()

        # http get
        self.browser.openUrl(self.url, self.timeout)

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
        # original device id is still there
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        self.assertIn(deviceIdA, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # cookies contain same device ids
        self.assertEqual(devicesFirst, devicesThird, 'Device ids found are different.')
        # device id is logged
        self.assertIn(deviceIdA, devicesLogs, 'Original device ids was not found in adsp logs.')


    def test_cookiesContainDifferentDevices(self):
        deviceIdA = '1447859209.11111111-1111-1111-eeee-111111111111'
        cookie_value_first = 'ls=1447859209000|v=1|di={}'.format(deviceIdA)
        deviceIdB = '1447859209.33333333-3333-3333-eeee-333333333333'
        cookie_value_third = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(deviceIdB)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value_first, self.domains['first'])
        self.cookies.set(self.cookie_name, cookie_value_third, self.domains['third'])
        self.cookies.close()

        # http get
        self.browser.openUrl(self.url, self.timeout)

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
        # original device id is still there
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        # original device id is still there
        self.assertIn(deviceIdB, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # original device id from cookie 3rd is prepended to cookie 1st
        self.assertIn(deviceIdB, devicesFirst, 'Original device id from third party cookies was not found in first party cookies, but it should be in.')
        self.assertEqual(devicesFirst[0], devicesThird[0], 'Device ids found are different.')
        # device id is logged
        self.assertIn(deviceIdA, devicesLogs, 'Original device id from cookie first was not found in adsp logs.')
        self.assertIn(deviceIdB, devicesLogs, 'Original device id from cookie third was not found in adsp logs.')


    def tearDown(self):
        # restore cookie behavior
        self.browser.restorePreferences(self.browser.prefs_file)



class TestFirefoxAcceptOnlyFirstPartyCookies(unittest.TestCase):

    def setUp(self):
        # setup adsp log
        self.adsplog = AdspLog('/home/rsicart/Repo/adsp-front/sd/www2/www/data/access')

        # setup website
        self.url = 'http://publisher.localhost/publisher.html'
        self.timeout = 3
        self.cookie_name = 'adsp_di'
        self.domains = {'first': 'publisher.localhost', 'third': '.adsp.localhost'}

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
        self.browser.setCookieBehavior('only_1')


    def test_allIsEmpty(self):
        # http get
        self.browser.openUrl(self.url, self.timeout)

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


        # cookies 1st are not empty
        self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
        # cookies 3rd are empty
        self.assertEqual(len(devicesThird), 0, 'Third party cookies are not empty, but they should.')
        # device id is logged
        self.assertEqual(devicesFirst, devicesLogs, 'Device ids in adsp logs are different than device ids in first party cookies.')


    def test_cookieThirdIsEmpty(self):
        # fill cookie 1st only
        deviceIdA = '1447859209.11111111-1111-1111-bbbb-111111111111'
        cookie_value = 'ls=1447859209770|v=1|di={}'.format(deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value, self.domains['first'])
        self.cookies.close()

        # http get
        self.browser.openUrl(self.url, self.timeout)

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

        # cookie 1st is restored from cookie 3rd


        # cookies 1st are not empty
        self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
        # cookies 3rd are empty
        self.assertEqual(len(devicesThird), 0, 'Third party cookies are not empty, but they should.')
        # original device id is still there
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        # device id is logged
        self.assertIn(deviceIdA, devicesLogs, 'Original device ids was not found in adsp logs.')


    def test_cookieFirstIsEmpty(self):
        # fill cookie 3rd only
        deviceIdA = '1447859209.33333333-3333-3333-cccc-333333333333'
        cookie_value = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value, self.domains['third'])
        self.cookies.close()

        # http get
        self.browser.openUrl(self.url, self.timeout)

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
        # original device id is still there
        self.assertIn(deviceIdA, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # cookie 1st is not restored from cookie 3rd
        self.assertNotIn(deviceIdA, devicesFirst, 'Original device id A from third party cookies was found in first party cookies, but it should not be there because third party cookies are disabled.')
        # device id is logged
        self.assertEqual(devicesFirst, devicesLogs, 'Device ids in adsp logs are different than device ids in cookies.')


    def test_cookiesContainSameDevice(self):
        # fill cookie 1st only
        deviceIdA = '1447859209.11111111-3333-1111-dddd-111111111111'
        cookie_value_first = 'ls=1447859209000|v=1|di={}'.format(deviceIdA)
        cookie_value_third = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value_first, self.domains['first'])
        self.cookies.set(self.cookie_name, cookie_value_third, self.domains['third'])
        self.cookies.close()

        # http get
        self.browser.openUrl(self.url, self.timeout)

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
        # original device id is still there
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        self.assertIn(deviceIdA, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # device id is logged
        self.assertIn(deviceIdA, devicesLogs, 'Original device ids was not found in adsp logs.')


    def test_cookiesContainDifferentDevices(self):
        deviceIdA = '1447859209.11111111-1111-1111-eeee-111111111111'
        cookie_value_first = 'ls=1447859209000|v=1|di={}'.format(deviceIdA)
        deviceIdB = '1447859209.33333333-3333-3333-eeee-333333333333'
        cookie_value_third = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(deviceIdB)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value_first, self.domains['first'])
        self.cookies.set(self.cookie_name, cookie_value_third, self.domains['third'])
        self.cookies.close()

        # http get
        self.browser.openUrl(self.url, self.timeout)

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
        # original device id is still there
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        self.assertIn(deviceIdB, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # cookie 1st is not restored from cookie 3rd
        self.assertNotIn(deviceIdB, devicesFirst, 'Original device id from third party cookies was found in first party cookies, but it should not be there because third party cookies are disabled.')
        # device id is logged
        self.assertIn(deviceIdA, devicesLogs, 'Original device id from first party cookies was not found in adsp logs.')
        self.assertNotIn(deviceIdB, devicesLogs, 'Original device id from third party cookies was found in adsp logs.')


    def tearDown(self):
        # restore cookie behavior
        self.browser.restorePreferences(self.browser.prefs_file)



class TestFirefoxAcceptNothing(unittest.TestCase):

    def setUp(self):
        # setup adsp log
        self.adsplog = AdspLog('/home/rsicart/Repo/adsp-front/sd/www2/www/data/access')

        # setup website
        self.url = 'http://publisher.localhost/publisher.html'
        self.timeout = 3
        self.cookie_name = 'adsp_di'
        self.domains = {'first': 'publisher.localhost', 'third': '.adsp.localhost'}

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
        self.browser.setCookieBehavior('nothing')


    def test_allIsEmpty(self):
        # http get
        self.browser.openUrl(self.url, self.timeout)

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

        # cookies are empty
        self.assertEqual(len(devicesFirst), 0, 'First party cookies are not empty, but they should.')
        self.assertEqual(len(devicesThird), 0, 'Third party cookies are not empty, but they should.')
        # device id is not logged
        self.assertNotEqual(devicesFirst, devicesLogs, 'Device ids in adsp logs are different than device ids in cookies.')
        self.assertNotEqual(devicesThird, devicesLogs, 'Device ids in adsp logs are different than device ids in cookies.')


    def test_cookieThirdIsEmpty(self):
        # fill cookie 1st only
        deviceIdA = '1447859209.11111111-1111-1111-bbbb-111111111111'
        cookie_value = 'ls=1447859209770|v=1|di={}'.format(deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value, self.domains['first'])
        self.cookies.close()

        # http get
        self.browser.openUrl(self.url, self.timeout)

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
        # cookies are empty
        self.assertEqual(len(devicesThird), 0, 'Third party cookies are not empty, but they should.')
        # original device id is still there
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        # a different device id is logged
        self.assertNotIn(deviceIdA, devicesLogs, 'Original device ids was found in adsp logs.')


    def test_cookieFirstIsEmpty(self):
        # fill cookie 3rd only
        deviceIdA = '1447859209.33333333-3333-3333-cccc-333333333333'
        cookie_value = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value, self.domains['third'])
        self.cookies.close()

        # http get
        self.browser.openUrl(self.url, self.timeout)

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

        # cookies are empty
        self.assertEqual(len(devicesFirst), 0, 'First party cookies are not empty, but they should.')
        # cookies are not empty
        self.assertNotEqual(len(devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # original device id is still there
        self.assertIn(deviceIdA, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # cookie 1st is not restored from cookie 3rd
        self.assertNotIn(deviceIdA, devicesFirst, 'Original device id A from third party cookies was found in first party cookies, but it should not be there because third party cookies are disabled.')
        # a different device id is logged
        self.assertNotIn(deviceIdA, devicesLogs, 'Original device ids was found in adsp logs.')


    def test_cookiesContainSameDevice(self):
        # fill cookie 1st only
        deviceIdA = '1447859209.11111111-3333-1111-dddd-111111111111'
        cookie_value_first = 'ls=1447859209000|v=1|di={}'.format(deviceIdA)
        cookie_value_third = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value_first, self.domains['first'])
        self.cookies.set(self.cookie_name, cookie_value_third, self.domains['third'])
        self.cookies.close()

        # http get
        self.browser.openUrl(self.url, self.timeout)

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
        # original device id is still there
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        self.assertIn(deviceIdA, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # a different device id is logged
        self.assertNotIn(deviceIdA, devicesLogs, 'Original device ids was found in adsp logs.')



    def test_cookiesContainDifferentDevices(self):
        deviceIdA = '1447859209.11111111-1111-1111-eeee-111111111111'
        cookie_value_first = 'ls=1447859209000|v=1|di={}'.format(deviceIdA)
        deviceIdB = '1447859209.33333333-3333-3333-eeee-333333333333'
        cookie_value_third = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(deviceIdB)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value_first, self.domains['first'])
        self.cookies.set(self.cookie_name, cookie_value_third, self.domains['third'])
        self.cookies.close()

        # http get
        self.browser.openUrl(self.url, self.timeout)

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
        # original device id is still there
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        self.assertIn(deviceIdB, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # device id from cookie 3rd is not prepended to cookie 1st
        self.assertNotIn(deviceIdB, devicesFirst, 'Original device id from third party cookies was found in first party cookies, but it should not be there because third party cookies are disabled.')
        # a different device id is logged
        self.assertNotIn(deviceIdA, devicesLogs, 'Original device id from first party cookies was found in adsp logs.')
        self.assertNotIn(deviceIdB, devicesLogs, 'Original device id from third party cookies was found in adsp logs.')


    def tearDown(self):
        # restore cookie behavior
        self.browser.restorePreferences(self.browser.prefs_file)



class TestFirefoxAcceptOnlyThirdPartyCookies(unittest.TestCase):

    def setUp(self):

        # setup adsp log
        self.adsplog = AdspLog('/home/rsicart/Repo/adsp-front/sd/www2/www/data/access')

        # setup website
        self.url = 'http://publisher.localhost/publisher.html'
        self.timeout = 3
        self.cookie_name = 'adsp_di'
        self.domains = {'first': 'publisher.localhost', 'third': '.adsp.localhost'}

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


    def test_allIsEmpty(self):

        # http get
        self.browser.openUrl(self.url, self.timeout)

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
        # that's unexpected but amazingly firefox still sets cookie for a blacklisted domain
        self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are not empty, but they should.')
        # cookies are not empty
        self.assertNotEqual(len(devicesThird), 0, 'Third party cookies are empty, but they should contain a new device id.')
        # device id is logged
        self.assertEqual(devicesThird, devicesLogs, 'Device ids in adsp logs are different than device ids in cookies.')


    def test_cookieThirdIsEmpty(self):
        # fill cookie 1st only
        deviceIdA = '1447859209.11111111-1111-1111-bbbb-111111111111'
        cookie_value = 'ls=1447859209770|v=1|di={}'.format(deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value, self.domains['first'])
        self.cookies.close()

        # http get
        self.browser.openUrl(self.url, self.timeout)

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
        self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are empty, but they should.')
        self.assertNotEqual(len(devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # original device id is still there
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        # cookie 3rd is restored from cookie 1st
        self.assertIn(deviceIdA, devicesThird, 'Original device id A from first party cookies was not found in third party cookies, but it should be there.')
        # device id is logged
        self.assertEqual(devicesThird, devicesLogs, 'Device ids in adsp logs are different than device ids in cookies.')


    def test_cookieFirstIsEmpty(self):
        # fill cookie 3rd only
        deviceIdA = '1447859209.33333333-3333-3333-cccc-333333333333'
        cookie_value = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value, self.domains['third'])
        self.cookies.close()

        # http get
        self.browser.openUrl(self.url, self.timeout)

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
        self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are empty, but they should not because firefox still first party cookies of blacklisted domains.')
        self.assertNotEqual(len(devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # original device id is still there
        self.assertIn(deviceIdA, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # cookie 1st is restored from cookie 3rd
        self.assertIn(deviceIdA, devicesFirst, 'Original device id A from third party cookies was not found in first party cookies, but it should be there.')
        # device id is logged
        self.assertIn(deviceIdA, devicesLogs, 'Original device ids was not found in adsp logs.')


    def test_cookiesContainSameDevice(self):
        # fill cookie 1st only
        deviceIdA = '1447859209.11111111-3333-1111-dddd-111111111111'
        cookie_value_first = 'ls=1447859209000|v=1|di={}'.format(deviceIdA)
        cookie_value_third = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value_first, self.domains['first'])
        self.cookies.set(self.cookie_name, cookie_value_third, self.domains['third'])
        self.cookies.close()

        # http get
        self.browser.openUrl(self.url, self.timeout)

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
        # original device id is still there
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        self.assertIn(deviceIdA, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        self.assertEqual(devicesFirst, devicesThird, 'Device ids found are different.')
        # device id is logged
        self.assertIn(deviceIdA, devicesLogs, 'Original device ids was not found in adsp logs.')


    def test_cookiesContainDifferentDevices(self):
        deviceIdA = '1447859209.11111111-1111-1111-dddd-111111111111'
        cookie_value_first = 'ls=1447859209000|v=1|di={}'.format(deviceIdA)
        deviceIdB = '1447859209.33333333-3333-3333-dddd-333333333333'
        cookie_value_third = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(deviceIdB)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value_first, self.domains['first'])
        self.cookies.set(self.cookie_name, cookie_value_third, self.domains['third'])
        self.cookies.close()

        # http get
        self.browser.openUrl(self.url, self.timeout)

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
        # original device id is still there
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        self.assertIn(deviceIdB, devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # cookie 3rd is prepended to cookie 1st
        self.assertIn(deviceIdB, devicesFirst, 'Original device id from third party cookies was found in first party cookies, but it should not be there because third party cookies are disabled.')
        # device id is logged
        self.assertIn(deviceIdA, devicesLogs, 'Original device id from first party cookies was found in adsp logs.')
        # device id is logged
        self.assertIn(deviceIdB, devicesLogs, 'Original device id from third party cookies was found in adsp logs.')


    def tearDown(self):
        # remove blacklist
        self.blacklist.setup()
        self.blacklist.flush()
        self.blacklist.close()
        # restore cookie behavior
        self.browser.restorePreferences(self.browser.prefs_file)




if __name__ == '__main__':
    unittest.main()
