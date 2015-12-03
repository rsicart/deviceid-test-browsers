#!/usr/bin/env python3

import test_firefox
import unittest

class TestFirefoxAcceptNothing(test_firefox.TestFirefox):
    """ Test suite to test a display in a publisher's website with Firefox browser.
    """

    def setUp(self):

        super().setUp() 

        # set cookie behavior
        self.browser.setCookieBehavior('nothing')


    def test_allIsEmpty(self):
        super().setup_allIsEmpty()

        # cookies are empty
        self.assertEqual(len(self.devicesFirst), 0, 'First party cookies are not empty, but they should.')
        # cookies are empty
        self.assertEqual(len(self.devicesThird), 0, 'Third party cookies are not empty, but they should.')
        # cookies don't contain any device id
        self.assertEqual(self.devicesFirst, self.devicesThird, 'Device ids found are equal.')
        # a different device id is logged every time
        self.assertNotEqual(self.devicesFirst, self.devicesLogs, 'Device ids in adsp logs are different than device ids in cookies.')
        self.assertNotEqual(self.devicesThird, self.devicesLogs, 'Device ids in adsp logs are different than device ids in cookies.')


    def test_cookieThirdIsEmpty(self):
        super().setup_cookieThirdIsEmpty()

        # cookies are not empty
        self.assertNotEqual(len(self.devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
        # cookies are empty
        self.assertEqual(len(self.devicesThird), 0, 'Third party cookies are not empty, but they should.')
        # original device id is still there
        self.assertIn(self.deviceIdA, self.devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        # cookie 3rd is restored not from cookie 1st
        self.assertNotEqual(self.devicesFirst, self.devicesThird, 'Device ids found are equal.')
        # a different device id is logged
        self.assertNotIn(self.deviceIdA, self.devicesLogs, 'Original device ids was found in adsp logs.')


    def test_cookieFirstIsEmpty(self):
        super().setup_cookieFirstIsEmpty()

        # cookies are empty
        self.assertEqual(len(self.devicesFirst), 0, 'First party cookies are not empty, but they should.')
        # cookies are not empty
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # original device id is still there
        self.assertIn(self.deviceIdA, self.devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # cookie 1st is not restored from cookie 3rd
        self.assertNotIn(self.deviceIdA, self.devicesFirst, 'Original device id A from third party cookies was found in first party cookies, but it should not be there because third party cookies are disabled.')
        # a different device id is logged
        self.assertNotIn(self.deviceIdA, self.devicesLogs, 'Original device ids was found in adsp logs.')


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
        # a different device id is logged
        self.assertNotIn(self.deviceIdA, self.devicesLogs, 'Original device ids was found in adsp logs.')



    def test_cookiesContainDifferentDevices(self):
        super().setup_cookiesContainDifferentDevices()

        # cookies are not empty
        self.assertNotEqual(len(self.devicesFirst), 0, 'First party cookies are empty, but they should contain a device id.')
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty, but they should contain a device id.')
        # original device id is still there
        self.assertIn(self.deviceIdA, self.devicesFirst, 'Original device id was not found in first party cookies, seems that it was overriden by a new one.')
        # original device id is still there
        self.assertIn(self.deviceIdB, self.devicesThird, 'Original device id was not found in third party cookies, seems that it was overriden by a new one.')
        # device id from cookie 3rd is not prepended to cookie 1st
        self.assertNotIn(self.deviceIdB, self.devicesFirst, 'Original device id from third party cookies was found in first party cookies, but it should not be there because third party cookies are disabled.')
        # a different device id is logged
        self.assertNotIn(self.deviceIdA, self.devicesLogs, 'Original device id from first party cookies was found in adsp logs.')
        self.assertNotIn(self.deviceIdB, self.devicesLogs, 'Original device id from third party cookies was found in adsp logs.')




if __name__ == '__main__':
    unittest.main()
