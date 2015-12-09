#!/usr/bin/env python3

import test_chromium
import unittest


class TestChromiumAcceptOnlyFirstPartyCookies(test_chromium.TestChromium):
    """ Test suite to test a click on an Ad in publisher's website and a redirect to advertiser's website
        with Chromium browser.
        When a user clicks an Ad it is redirected to adsp with a device id in querystring for ALL tests
        in the suite.
        Landing page has a our lib tracker.js, and it triggers a lead automatically.
    """

    def setUp(self):
        super().setUp()

        # set cookie behavior
        self.browser.setCookieBehavior('only_1')


    def test_allIsEmpty(self):
        super().setup_allIsEmpty()

        # cookies are not empty
        # that's unexpected but amazingly chromium still sets cookie for a blacklisted domain
        self.assertNotEqual(len(self.devicesFirst), 0, 'First party cookies are empty.')
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty.')
        # original device id from querystring saved in cookies 1st
        self.assertIn(self.device_id_querystring, self.devicesFirst, 'Original device id from querystring was not found in first party cookies.')
        # original device id from querystring saved in cookies 3rd
        self.assertIn(self.device_id_querystring, self.devicesThird, 'Original device id from querystring was not found in third party cookies.')
        # device id is logged
        self.assertIn(self.device_id_querystring, self.devicesLogs, 'Original device id from querystring was not found in adsp logs.')


    def test_cookieThirdIsEmpty(self):
        super().setup_cookieThirdIsEmpty()

        # cookies are not empty
        self.assertNotEqual(len(self.devicesFirst), 0, 'First party cookies are empty.')
        # cookies are not empty
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty.')
        # original device id is still there
        self.assertIn(self.deviceIdA, self.devicesFirst, 'Original device id  was not found in first party cookies.')
        # original device id from querystring prepended to cookies 1st
        self.assertIn(self.device_id_querystring, self.devicesFirst, 'Original device id from querystring was not found in first party cookies.')
        # original device id from querystring saved in cookies 3rd
        self.assertIn(self.device_id_querystring, self.devicesThird, 'Original device id  was not found in third party cookies.')
        # all device ids were logged
        self.assertIn(self.deviceIdA, self.devicesLogs, 'Original device id from cookies was not found in adsp logs.')
        self.assertIn(self.device_id_querystring, self.devicesLogs, 'Original device id from querystring was not found in adsp logs.')


    def test_cookieFirstIsEmpty(self):
        """ Device id in click's url querystring will be replaced by device id in third party cookies.
            After that, device id in 3rd party cookies will be stacked into 1st party cookies.
        """
        super().setup_cookieFirstIsEmpty()

        # cookies are not empty
        self.assertNotEqual(len(self.devicesFirst), 0, 'First party cookies are empty.')
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty.')
        # original device id in cookies third is still there
        self.assertIn(self.deviceIdA, self.devicesThird, 'Original device id was not found in third party cookies.')
        # cookie 1st restored from cookie 3rd
        self.assertIn(self.deviceIdA, self.devicesFirst, 'Original device id was not found in first party cookies.')
        # original device id in querystring is not prepended to cookie 1st
        self.assertNotIn(self.device_id_querystring, self.devicesFirst, 'Original device id from querystring was found in first party cookies.')
        # device id is logged
        self.assertIn(self.deviceIdA, self.devicesLogs, 'Original device id from cookies was found in adsp logs.')
        # device id is not logged
        self.assertNotIn(self.device_id_querystring, self.devicesLogs, 'Original device id from querystring was found in adsp logs.')


    def test_cookiesContainSameDevice(self):
        super().setup_cookiesContainSameDevice()

        # cookies are not empty
        self.assertNotEqual(len(self.devicesFirst), 0, 'First party cookies are empty.')
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty.')
        # original device id is still there
        self.assertIn(self.deviceIdA, self.devicesFirst, 'Original device id was not found in first party cookies.')
        self.assertIn(self.deviceIdA, self.devicesThird, 'Original device id was not found in third party cookies.')
        # original device id in querystring not prepended to cookies 1st
        self.assertNotIn(self.device_id_querystring, self.devicesFirst, 'Original device id from querystring was found in first party cookies.')
        # original device id from cookies was logged
        self.assertIn(self.deviceIdA, self.devicesLogs, 'Original device id from cookies was not found in adsp logs.')
        # device id is not logged
        self.assertNotIn(self.device_id_querystring, self.devicesLogs, 'Original device id from querystring was found in adsp logs.')


    def test_cookiesContainDifferentDevices(self):
        super().setup_cookiesContainDifferentDevices()

        # cookies are not empty
        self.assertNotEqual(len(self.devicesFirst), 0, 'First party cookies are empty.')
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty.')
        # original device id in cookies is still there
        self.assertIn(self.deviceIdA, self.devicesFirst, 'Original device id was not found in first party cookies.')
        self.assertIn(self.deviceIdB, self.devicesThird, 'Original device id was not found in third party cookies.')
        # device id from cookies 3rd prepended to cookies 1st
        self.assertIn(self.deviceIdB, self.devicesFirst, 'Original device id from cookies 3rd was not found in first party cookies.')
        # original device id in querystring ignored
        self.assertNotIn(self.device_id_querystring, self.devicesFirst, 'Original device id from querystring was found in first party cookies.')
        # original device id from first party cookies was logged
        self.assertIn(self.deviceIdA, self.devicesLogs, 'Original device id from cookies was found in adsp logs.')
        # original device id from third party cookies was logged
        self.assertIn(self.deviceIdB, self.devicesLogs, 'Original device id from cookies was found in adsp logs.')
        # device id is not logged
        self.assertNotIn(self.device_id_querystring, self.devicesLogs, 'Original device id from querystring was found in adsp logs.')




if __name__ == '__main__':
        unittest.main()
