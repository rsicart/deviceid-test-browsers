#!/usr/bin/env python3

from chromium.chromium import *
from common.adsplog import *
import unittest
import time
import settings

class TestChromium(unittest.TestCase):
    """ Test suite to test a click on an Ad in publisher's website and a redirect to advertiser's website
        with Chromium browser.
        When a user clicks an Ad it is redirected to adsp with a device id in querystring for ALL tests
        in the suite.
        Landing page has a our lib tracker.js, and it triggers a lead automatically.
    """

    def setUp(self):

        time.sleep(settings.wait_before)

        # setup adsp log
        self.adsplog = AdspLog(settings.folder_adsp_logs)

        # setup website
        self.url = settings.click_to_advertiser['url']
        self.timeout = settings.http_get_timeout
        self.cookie_name = settings.cookie_name
        self.domains = settings.click_to_advertiser['domains']

        # setup chromium
        self.browser = Chromium(settings.chromium['profile_folder'])

        # flush cookies before browsing
        db_path = '{}/Default'.format(settings.chromium['profile_folder'], settings.chromium['profile_name'])
        self.cookies = Cookies(db_path, settings.chromium['cookie_db'], settings.chromium['cookie_table'])
        self.cookies.setup()
        self.cookies.flush()
        self.cookies.close()


    def fetch_devices(self):
        """ fetch all device ids from cookies and logs
        """
        self.cookies.setup()
        cookieFirst = self.cookies.get(self.cookie_name, self.domains['first'])
        cookieThird = self.cookies.get(self.cookie_name, self.domains['third'])
        self.cookies.close()

        self.devicesFirst = []
        self.devicesThird = []
        if cookieFirst:
            self.devicesFirst = self.cookies.getDeviceIdsFromCookie(cookieFirst)
        if cookieThird:
            self.devicesThird = self.cookies.getDeviceIdsFromCookie(cookieThird)

        self.devicesLogs = self.adsplog.getDeviceIds(self.adsplog.getLastLine())


    def setup_allIsEmpty(self):
        """ Device id in click's url querystring will be used to set 1st and 3rd party cookies.
        """

        """ http request
        """
        # setup querystring
        self.device_id_querystring = '1447344866.44444444-4444-4444-aaaa-444444444444'
        url = self.url.format(self.device_id_querystring)

        # http get
        self.browser.openUrl(url, self.timeout)
        time.sleep(settings.wait_after)
        self.fetch_devices()


    def setup_cookieThirdIsEmpty(self):
        """ Device id in click's url querystring will be set in 3rd party cookies.
            After that, device id in 3rd party cookies will be stacked into 1st party cookies.
        """

        """ http request
        """
        # setup querystring
        self.device_id_querystring = '1447344866.44444444-4444-4444-bbbb-444444444444'
        url = self.url.format(self.device_id_querystring)

        # fill cookie 1st only
        self.deviceIdA = '1447859209.11111111-1111-1111-bbbb-111111111111'
        cookie_value = 'ls=1447859209770|v=1|di={}'.format(self.deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value, self.domains['first'])
        self.cookies.close()

        # http get
        self.browser.openUrl(url, self.timeout)
        time.sleep(settings.wait_after)
        self.fetch_devices()


    def setup_cookieFirstIsEmpty(self):
        """ Device id in click's url querystring will be replaced by device id in third party cookies.
            After that, device id in 3rd party cookies will be stacked into 1st party cookies.
        """

        """ http request
        """
        # setup querystring
        self.device_id_querystring = '1447344866.44444444-4444-4444-cccc-444444444444'
        url = self.url.format(self.device_id_querystring)

        # fill cookie 3rd only
        self.deviceIdA = '1447859209.33333333-3333-3333-cccc-333333333333'
        cookie_value = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(self.deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value, self.domains['third'])
        self.cookies.close()

        # http get
        self.browser.openUrl(url, self.timeout)
        time.sleep(settings.wait_after)
        self.fetch_devices()


    def setup_cookiesContainSameDevice(self):
        """ Device id in click's url querystring will be replaced by device id in third party cookies.
            Device ids in first party cookies will stay the same, like third party cookies.
        """

        """ http request
        """
        # setup querystring
        self.device_id_querystring = '1447344866.44444444-4444-4444-dddd-444444444444'
        url = self.url.format(self.device_id_querystring)

        self.deviceIdA = '1447859209.11111111-3333-1111-dddd-111111111111'
        cookie_value_first = 'ls=1447859209000|v=1|di={}'.format(self.deviceIdA)
        cookie_value_third = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(self.deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value_first, self.domains['first'])
        self.cookies.set(self.cookie_name, cookie_value_third, self.domains['third'])
        self.cookies.close()

        # http get
        self.browser.openUrl(url, self.timeout)
        time.sleep(settings.wait_after)
        self.fetch_devices()


    def setup_cookiesContainDifferentDevices(self):
        """ Device id in click's url querystring will be replaced by device id in third party cookies.
            After that, device id in 3rd party cookies will be stacked into 1st party cookies.
        """

        """ http request
        """
        # setup querystring
        self.device_id_querystring = '1447344866.44444444-4444-4444-eeee-444444444444'
        url = self.url.format(self.device_id_querystring)

        self.deviceIdA = '1447859209.11111111-1111-1111-eeee-111111111111'
        cookie_value_first = 'ls=1447859209000|v=1|di={}'.format(self.deviceIdA)
        self.deviceIdB = '1447859209.33333333-3333-3333-eeee-333333333333'
        cookie_value_third = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(self.deviceIdB)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value_first, self.domains['first'])
        self.cookies.set(self.cookie_name, cookie_value_third, self.domains['third'])
        self.cookies.close()

        # http get
        self.browser.openUrl(url, self.timeout)
        time.sleep(settings.wait_after)
        self.fetch_devices()


    def tearDown(self):
        # restore cookie behavior
        self.browser.restorePreferences(self.browser.prefs_file)




if __name__ == '__main__':
        unittest.main()
