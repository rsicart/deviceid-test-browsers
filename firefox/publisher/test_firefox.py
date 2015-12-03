#!/usr/bin/env python3

from firefox.firefox import *
from common.adsplog import *
import unittest
import time
import settings

class TestFirefox(unittest.TestCase):
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
        self.browser = Firefox(settings.firefox['profile_name'], settings.firefox['profile_folder'])

        # flush cookies before browsing
        self.cookies = Cookies(settings.firefox['profile_folder'], settings.firefox['cookie_db'], settings.firefox['cookie_table'])
        self.cookies.setup()
        self.cookies.flush()
        self.cookies.close()


    def fetch_devices(self):
        # fetch device ids from cookies
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

        # fetch device ids from adsp logs
        self.devicesLogs = []
        self.devicesLogs = self.adsplog.getDeviceIds(self.adsplog.getLastLine())


    def setup_allIsEmpty(self):
        self.browser.openUrl(self.url, self.timeout)
        self.fetch_devices()


    def setup_cookieThirdIsEmpty(self):
        # fill cookie 1st only
        self.deviceIdA = '1447859209.11111111-1111-1111-bbbb-111111111111'
        cookie_value = 'ls=1447859209770|v=1|di={}'.format(self.deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value, self.domains['first'])
        self.cookies.close()

        self.browser.openUrl(self.url, self.timeout)
        self.fetch_devices()


    def setup_cookieFirstIsEmpty(self):
        # fill cookie 3rd only
        self.deviceIdA = '1447859209.33333333-3333-3333-cccc-333333333333'
        cookie_value = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(self.deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value, self.domains['third'])
        self.cookies.close()

        self.browser.openUrl(self.url, self.timeout)
        self.fetch_devices()


    def setup_cookiesContainSameDevice(self):
        self.deviceIdA = '1447859209.11111111-3333-1111-dddd-111111111111'
        cookie_value_first = 'ls=1447859209000|v=1|di={}'.format(self.deviceIdA)
        cookie_value_third = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(self.deviceIdA)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value_first, self.domains['first'])
        self.cookies.set(self.cookie_name, cookie_value_third, self.domains['third'])
        self.cookies.close()

        self.browser.openUrl(self.url, self.timeout)
        self.fetch_devices()


    def setup_cookiesContainDifferentDevices(self):
        self.deviceIdA = '1447859209.11111111-1111-1111-eeee-111111111111'
        cookie_value_first = 'ls=1447859209000|v=1|di={}'.format(self.deviceIdA)
        self.deviceIdB = '1447859209.33333333-3333-3333-eeee-333333333333'
        cookie_value_third = 'ls%3D1447859209000%7Cv%3D1%7Cdi%3D{}'.format(self.deviceIdB)
        self.cookies.setup()
        self.cookies.set(self.cookie_name, cookie_value_first, self.domains['first'])
        self.cookies.set(self.cookie_name, cookie_value_third, self.domains['third'])
        self.cookies.close()

        self.browser.openUrl(self.url, self.timeout)
        self.fetch_devices()


    def tearDown(self):
        # restore cookie behavior
        self.browser.restorePreferences(self.browser.prefs_file)




if __name__ == '__main__':
        unittest.main()
