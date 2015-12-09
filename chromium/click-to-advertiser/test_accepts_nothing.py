#!/usr/bin/env python3

import test_chromium
import unittest


class TestChromiumAcceptNothing(test_chromium.TestChromium):
    """ Test suite to test a click on an Ad in publisher's website and a redirect to advertiser's website
        with Chromium browser.
        When a user clicks an Ad it is redirected to adsp with a device id in querystring for ALL tests
        in the suite.
        Landing page has a our lib tracker.js, and it triggers a lead automatically.
    """

    def setUp(self):
        super().setUp()

        # set cookie behavior
        self.browser.setCookieBehavior('nothing')


    def test_allIsEmpty(self):
        """ Device id in click's url querystring won't we saved in cookies, but tracking request
            will still log device id because it's in landing's page url.
            Remark that device id from existing cookies are not sent because cookies are disabled.
        """
        super().setup_allIsEmpty()

        # cookies are empty
        self.assertEqual(len(self.devicesFirst), 0, 'First party cookies not are empty.')
        self.assertEqual(len(self.devicesThird), 0, 'Third party cookies not are empty.')
        # original device id from querystring not saved in cookies
        self.assertNotIn(self.device_id_querystring, self.devicesFirst, 'Device ids found are different.')
        self.assertNotIn(self.device_id_querystring, self.devicesThird, 'Device ids found are different.')
        # device id is logged (because a device id exists in querystring)
        self.assertIn(self.device_id_querystring, self.devicesLogs, 'Device ids in adsp logs are different than device ids in querystring.')


    def test_cookieThirdIsEmpty(self):
        """ Device id in click's url querystring won't we saved in cookies, but tracking request
            will still log device id because it's in landing's page url.
            Remark that device id from existing cookies are not sent because cookies are disabled.
        """
        super().setup_cookieThirdIsEmpty()

        # cookies are not empty
        self.assertNotEqual(len(self.devicesFirst), 0, 'First party cookies are empty.')
        # cookies are empty
        self.assertEqual(len(self.devicesThird), 0, 'Third party cookies not are empty.')
        # original device id from querystring not saved in cookies
        self.assertNotIn(self.device_id_querystring, self.devicesFirst, 'Original device id from querystring was found in first party cookies.')
        self.assertNotIn(self.device_id_querystring, self.devicesThird, 'Original device id from querystring was found in third party cookies.')
        # device id is not logged
        self.assertNotIn(self.deviceIdA, self.devicesLogs, 'Original device id from cookies was found in adsp logs.')
        # device id is logged (because a device id exists in querystring)
        self.assertIn(self.device_id_querystring, self.devicesLogs, 'Original device id from querystring was not found in adsp logs.')


    def test_cookieFirstIsEmpty(self):
        """ Device id in click's url querystring won't we saved in cookies, but tracking request
            will still log device id because it's in landing's page url.
            Remark that device id from existing cookies are not sent because cookies are disabled.
        """
        super().setup_cookieFirstIsEmpty()

        # cookies are empty
        self.assertEqual(len(self.devicesFirst), 0, 'First party cookies are not empty.')
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty.')
        # original device id in cookies third is still there
        self.assertIn(self.deviceIdA, self.devicesThird, 'Original device id was not found in third party cookies.')
        # cookies 1st not restored from cookie 3rd
        self.assertNotIn(self.deviceIdA, self.devicesFirst, 'Original device id was found in first party cookies.')
        # original device id in querystring ignored because device id was restored from cookies 3rd
        self.assertNotIn(self.device_id_querystring, self.devicesFirst, 'Original device id from querystring was found in first party cookies.')
        # original device id from third party cookies was not logged
        self.assertNotIn(self.deviceIdA, self.devicesLogs, 'Original device ids was not found in adsp logs.')
        # device id is logged (because a device id exists in querystring)
        self.assertIn(self.device_id_querystring, self.devicesLogs, 'Original device id from querystring was not found in adsp logs.')


    def test_cookiesContainSameDevice(self):
        """ Device id in click's url querystring won't we saved in cookies, but tracking request
            will still log device id because it's in landing's page url.
            Remark that device id from existing cookies are not sent because cookies are disabled.
        """

        super().setup_cookiesContainSameDevice()

        # cookies are not empty
        self.assertNotEqual(len(self.devicesFirst), 0, 'First party cookies are empty.')
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty.')
        # original device id is still there
        self.assertIn(self.deviceIdA, self.devicesFirst, 'Original device id was not found in first party cookies.')
        self.assertIn(self.deviceIdA, self.devicesThird, 'Original device id was not found in third party cookies.')
        # original device id in querystring not prepended to cookies 1st
        self.assertNotIn(self.device_id_querystring, self.devicesFirst, 'Original device id from querystring was found in first party cookies.')
        # original device id from cookies was not logged
        self.assertNotIn(self.deviceIdA, self.devicesLogs, 'Original device ids from cookies were not found in adsp logs.')
        # device id is logged (because a device id exists in querystring)
        self.assertIn(self.device_id_querystring, self.devicesLogs, 'Original device id from querystring was not found in adsp logs.')


    def test_cookiesContainDifferentDevices(self):
        """ Device id in click's url querystring won't we saved in cookies, but tracking request
            will still log device id because it's in landing's page url.
            Remark that device id from existing cookies are not sent because cookies are disabled.
        """
        super().setup_cookiesContainDifferentDevices()

        # cookies are not empty
        self.assertNotEqual(len(self.devicesFirst), 0, 'First party cookies are empty.')
        self.assertNotEqual(len(self.devicesThird), 0, 'Third party cookies are empty.')
        # original device id is still there
        self.assertIn(self.deviceIdA, self.devicesFirst, 'Original device id was not found in first party cookies.')
        self.assertIn(self.deviceIdB, self.devicesThird, 'Original device id was not found in third party cookies.')
        # device id from cookies 3rd not prepended to cookies 1st
        self.assertNotIn(self.deviceIdB, self.devicesFirst, 'Original device id from cookies 3rd was found in first party cookies.')
        # original device id in querystring not prepended to cookies 1st
        self.assertNotIn(self.device_id_querystring, self.devicesFirst, 'Original device id from querystring was found in first party cookies.')
        # original device id from first party cookies was not logged
        self.assertNotIn(self.deviceIdA, self.devicesLogs, 'Original device ids was found in adsp logs.')
        # original device id from third party cookies was not logged
        self.assertNotIn(self.deviceIdB, self.devicesLogs, 'Original device ids was found in adsp logs.')
        # device id is logged (because a device id exists in querystring)
        self.assertIn(self.device_id_querystring, self.devicesLogs, 'Original device id from querystring was not found in adsp logs.')




if __name__ == '__main__':
        unittest.main()
