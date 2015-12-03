#!/usr/bin/env python3

from firefox.firefox import *
from common.adsplog import *
import unittest
import time
import settings

class TestFirefoxAcceptNothing(unittest.TestCase):
    """ Test suite to test a click on an Ad in publisher's website and a redirect to advertiser's website
        with Firefox browser.
        When a user clicks an Ad it is redirected to adsp with a device id in querystring for ALL tests
        in the suite.
        Landing page has a our lib tracker.js, and it triggers a lead automatically.
    """

    def setUp(self):

        time.sleep(settings.wait_before)

        # setup adsp log
        self.adsplog = AdspLog(settings.folder_adsp_logs)

        # setup website
        self.url = settings.url
        self.timeout = settings.http_get_timeout
        self.cookie_name = settings.cookie_name
        self.domains = settings.domains

        # setup firefox
        profile_name = settings.firefox['profile_name']
        profile_folder = settings.firefox['profile_folder']
        self.browser = Firefox(profile_name, profile_folder)

        # flush cookies before browsing
        db_name = settings.firefox['cookie_db']
        db_table = settings.firefox['cookie_table']
        self.cookies = Cookies(profile_folder, db_name, db_table)
        self.cookies.setup()
        self.cookies.flush()
        self.cookies.close()

        # set cookie behavior
        self.browser.setCookieBehavior('nothing')


    def test_allIsEmpty(self):
        """ Device id in click's url querystring won't we saved in cookies, but tracking request
            will still log device id because it's in landing's page url.
            Remark that device id from existing cookies are not sent because cookies are disabled.
        """

        """ http request
        """
        # setup querystring
        device_id_querystring = '1447344866.44444444-4444-4444-aaaa-444444444444'
        url = self.url.format(device_id_querystring)

        # http get
        self.browser.openUrl(url, self.timeout)

        """ fetch all device ids from cookies and logs
        """
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

        """ assertions
        """
        # cookies are empty
        self.assertEqual(len(devicesFirst), 0, 'First party cookies not are empty.')
        self.assertEqual(len(devicesThird), 0, 'Third party cookies not are empty.')
        # original device id from querystring not saved in cookies
        self.assertNotIn(device_id_querystring, devicesFirst, 'Device ids found are different.')
        self.assertNotIn(device_id_querystring, devicesThird, 'Device ids found are different.')
        # device id is logged (because a device id exists in querystring)
        self.assertIn(device_id_querystring, devicesLogs, 'Device ids in adsp logs are different than device ids in querystring.')


    def test_cookieThirdIsEmpty(self):
        """ Device id in click's url querystring won't we saved in cookies, but tracking request
            will still log device id because it's in landing's page url.
            Remark that device id from existing cookies are not sent because cookies are disabled.
        """

        """ http request
        """
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

        """ fetch all device ids from cookies and logs
        """
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

        """ assertions
        """

        # cookies are not empty
        self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are empty.')
        # cookies are empty
        self.assertEqual(len(devicesThird), 0, 'Third party cookies not are empty.')
        # original device id from querystring not saved in cookies
        self.assertNotIn(device_id_querystring, devicesFirst, 'Original device id from querystring was found in first party cookies.')
        self.assertNotIn(device_id_querystring, devicesThird, 'Original device id from querystring was found in third party cookies.')
        # device id is not logged
        self.assertNotIn(deviceIdA, devicesLogs, 'Original device id from cookies was found in adsp logs.')
        # device id is logged (because a device id exists in querystring)
        self.assertIn(device_id_querystring, devicesLogs, 'Original device id from querystring was not found in adsp logs.')


    def test_cookieFirstIsEmpty(self):
        """ Device id in click's url querystring won't we saved in cookies, but tracking request
            will still log device id because it's in landing's page url.
            Remark that device id from existing cookies are not sent because cookies are disabled.
        """

        """ http request
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

        """ fetch all device ids from cookies and logs
        """
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

        """ assertions
        """

        # cookies are empty
        self.assertEqual(len(devicesFirst), 0, 'First party cookies are not empty.')
        self.assertNotEqual(len(devicesThird), 0, 'Third party cookies are empty.')
        # original device id in cookies third is still there
        self.assertIn(deviceIdA, devicesThird, 'Original device id was not found in third party cookies.')
        # cookies 1st not restored from cookie 3rd
        self.assertNotIn(deviceIdA, devicesFirst, 'Original device id was found in first party cookies.')
        # original device id in querystring ignored because device id was restored from cookies 3rd
        self.assertNotIn(device_id_querystring, devicesFirst, 'Original device id from querystring was found in first party cookies.')
        # original device id from third party cookies was not logged
        self.assertNotIn(deviceIdA, devicesLogs, 'Original device ids was not found in adsp logs.')
        # device id is logged (because a device id exists in querystring)
        self.assertIn(device_id_querystring, devicesLogs, 'Original device id from querystring was not found in adsp logs.')


    def test_cookiesContainSameDevice(self):
        """ Device id in click's url querystring won't we saved in cookies, but tracking request
            will still log device id because it's in landing's page url.
            Remark that device id from existing cookies are not sent because cookies are disabled.
        """

        """ http request
        """
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

        """ fetch all device ids from cookies and logs
        """
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

        """ assertions
        """


        # cookies are not empty
        self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are empty.')
        self.assertNotEqual(len(devicesThird), 0, 'Third party cookies are empty.')
        # original device id is still there
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies.')
        self.assertIn(deviceIdA, devicesThird, 'Original device id was not found in third party cookies.')
        # original device id in querystring not prepended to cookies 1st
        self.assertNotIn(device_id_querystring, devicesFirst, 'Original device id from querystring was found in first party cookies.')
        # original device id from cookies was not logged
        self.assertNotIn(deviceIdA, devicesLogs, 'Original device ids from cookies were not found in adsp logs.')
        # device id is logged (because a device id exists in querystring)
        self.assertIn(device_id_querystring, devicesLogs, 'Original device id from querystring was not found in adsp logs.')


    def test_cookiesContainDifferentDevices(self):
        """ Device id in click's url querystring won't we saved in cookies, but tracking request
            will still log device id because it's in landing's page url.
            Remark that device id from existing cookies are not sent because cookies are disabled.
        """

        """ http request
        """
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

        """ fetch all device ids from cookies and logs
        """
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

        """ assertions
        """

        # cookies are not empty
        self.assertNotEqual(len(devicesFirst), 0, 'First party cookies are empty.')
        self.assertNotEqual(len(devicesThird), 0, 'Third party cookies are empty.')
        # original device id is still there
        self.assertIn(deviceIdA, devicesFirst, 'Original device id was not found in first party cookies.')
        self.assertIn(deviceIdB, devicesThird, 'Original device id was not found in third party cookies.')
        # device id from cookies 3rd not prepended to cookies 1st
        self.assertNotIn(deviceIdB, devicesFirst, 'Original device id from cookies 3rd was found in first party cookies.')
        # original device id in querystring not prepended to cookies 1st
        self.assertNotIn(device_id_querystring, devicesFirst, 'Original device id from querystring was found in first party cookies.')
        # original device id from first party cookies was not logged
        self.assertNotIn(deviceIdA, devicesLogs, 'Original device ids was found in adsp logs.')
        # original device id from third party cookies was not logged
        self.assertNotIn(deviceIdB, devicesLogs, 'Original device ids was found in adsp logs.')
        # device id is logged (because a device id exists in querystring)
        self.assertIn(device_id_querystring, devicesLogs, 'Original device id from querystring was not found in adsp logs.')


    def tearDown(self):
        # restore cookie behavior
        self.browser.restorePreferences(self.browser.prefs_file)




if __name__ == '__main__':
        unittest.main()
