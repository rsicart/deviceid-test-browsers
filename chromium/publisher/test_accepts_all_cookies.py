#!/usr/bin/env python3

import test_chromium
import unittest

class TestChromiumAcceptAllCookies(test_chromium.TestChromium):
    """ Test suite to test a display in a publisher's website with Chromium browser.
    """

    def setUp(self):

        super().setUp() 

        # set cookie behavior
        self.browser.setCookieBehavior('all')


    def test_allIsEmpty(self):
        super().setup_allIsEmpty()

        # cookies are not empty
        self.assertNotEqual(len(self.devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
        # cookies are not empty
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # cookies contain same device id
        self.assertEqual(self.devicesFirst, self.devicesThird, 'Device ids found are different.')
        # device id is logged
        self.assertEqual(self.devicesFirst, self.devicesLogs, 'Device ids in adsp logs are different than device ids in cookies.')


    def test_cookieThirdIsEmpty(self):
        super().setup_cookieThirdIsEmpty()

        # cookies are not empty
        self.assertNotEqual(len(self.devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
        # cookies are not empty
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # original device id is still there
        self.assertIn(self.deviceIdA, self.devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        # cookie 3rd is restored from cookie 1st
        self.assertEqual(self.devicesFirst, self.devicesThird, 'Device ids found are different.')
        # device id is logged
        self.assertIn(self.deviceIdA, self.devicesLogs, 'Original device ids was not found in adsp logs.')


    def test_cookieFirstIsEmpty(self):
        super().setup_cookieFirstIsEmpty()

        # cookies are not empty
        self.assertNotEqual(len(self.devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
        # cookies are not empty
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # original device id is still there
        self.assertIn(self.deviceIdA, self.devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # cookie 1st is restored from cookie 3rd
        self.assertIn(self.deviceIdA, self.devicesFirst, 'Original device id A from third party cookies was not found in first party cookies, but it should be there.')
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
        # original device id from cookie 3rd is prepended to cookie 1st
        self.assertIn(self.deviceIdB, self.devicesFirst, 'Original device id from third party cookies was not found in first party cookies, but it should be in.')
        # device id is logged
        self.assertIn(self.deviceIdA, self.devicesLogs, 'Original device id from cookie first was not found in adsp logs.')
        self.assertIn(self.deviceIdB, self.devicesLogs, 'Original device id from cookie third was not found in adsp logs.')


    def tearDown(self):
        super().tearDown()



if __name__ == '__main__':
    unittest.main()
