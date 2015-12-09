#!/usr/bin/env python3

import test_chromium
from chromium.chromium import *
import unittest
import settings

class TestChromiumAcceptOnlyThirdPartyCookies(test_chromium.TestChromium):
    """ Test suite to test a display in a publisher's website with Chromium browser.
        
        Note: when a domain is blacklisted, Chromium doesn't save cookies in cookie
        database, as other browsers do, for example Firefox.
        Remark that if cookie database contains already a cookie, it won't be sent
        by the browser with the following http requests.
    """

    def setUp(self):

        super().setUp() 

        # set cookie behavior
        self.browser.setCookieBehavior('all')

        # blacklist first party domain
        self.browser.blacklist(settings.domains['first'])


    def test_allIsEmpty(self):
        super().setup_allIsEmpty()

        # cookies are empty
        self.assertEqual(len(self.devicesFirst), 0, 'First party cookies are not empty.')
        # cookies are not empty
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # cookies don't contain same device id
        self.assertNotEqual(self.devicesFirst, self.devicesThird, 'Device ids found are equal.')
        # device id is logged
        self.assertEqual(self.devicesThird, self.devicesLogs, 'Device ids in adsp logs are different than device ids in cookies.')


    def test_cookieThirdIsEmpty(self):
        super().setup_cookieThirdIsEmpty()

        # cookies are not empty
        self.assertNotEqual(len(self.devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
        # cookies are not empty
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # original device id is still there
        self.assertIn(self.deviceIdA, self.devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        # cookie 3rd is not restored from cookie 1st
        self.assertNotIn(self.deviceIdA, self.devicesThird, 'Original device id was found in third party cookies.')
        # device id is logged
        self.assertEqual(self.devicesThird, self.devicesLogs, 'Original device ids was not found in adsp logs.')


    def test_cookieFirstIsEmpty(self):
        super().setup_cookieFirstIsEmpty()

        # cookies are empty
        self.assertEqual(len(self.devicesFirst), 0, 'First party cookies are not empty.')
        # cookies are not empty
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # original device id is still there
        self.assertIn(self.deviceIdA, self.devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # cookie 1st is not restored from cookie 3rd
        self.assertNotIn(self.deviceIdA, self.devicesFirst, 'Original device id was found in first party cookies.')
        # device id is logged
        self.assertIn(self.deviceIdA, self.devicesLogs, 'Original device ids was not found in adsp logs.')


    def test_cookiesContainSameDevice(self):
        super().setup_cookiesContainSameDevice()

        # cookies are not empty
        self.assertNotEqual(len(self.devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # original device id is still there
        self.assertIn(self.deviceIdA, self.devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        self.assertIn(self.deviceIdA, self.devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # cookies contain same device ids
        self.assertEqual(self.devicesFirst, self.devicesThird, 'Device ids found are different.')
        # device id is logged
        self.assertIn(self.deviceIdA, self.devicesLogs, 'Original device ids was not found in adsp logs.')


    def test_cookiesContainDifferentDevices(self):
        super().setup_cookiesContainDifferentDevices()

        # cookies are not empty
        self.assertNotEqual(len(self.devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # original device id is still there
        self.assertIn(self.deviceIdA, self.devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        # original device id is still there
        self.assertIn(self.deviceIdB, self.devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # original device id from cookie 3rd is not prepended to cookie 1st
        self.assertNotIn(self.deviceIdB, self.devicesFirst, 'Original device id from third party cookies was found in first party cookies.')
        # device id is not logged
        self.assertNotIn(self.deviceIdA, self.devicesLogs, 'Original device id from cookie first was found in adsp logs.')
        # device id is logged
        self.assertIn(self.deviceIdB, self.devicesLogs, 'Original device id from cookie third was not found in adsp logs.')


    def tearDown(self):
        super().tearDown()
        # remove blacklist
        self.browser.flushBlacklist()




if __name__ == '__main__':
    unittest.main()
