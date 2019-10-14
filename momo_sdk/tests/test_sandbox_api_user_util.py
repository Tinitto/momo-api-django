"""
The tests for the sandbox_api_user utility that is used to create sandbox users
It is ported from the mtn-pay-js Typescript package by Martin Ahindura
https://github.com/sopherapps/mtn-pay-js/blob/master/src/__tests__/sandboxApiUser.Spec.ts
"""
import os
from unittest import TestCase
from unittest.mock import patch
from momo_sdk.utils.sandbox_api_user import SandboxApiUser


class TestSandboxApiUser(TestCase):
    """
    Tests for the SandboxApiUser utility class that creates a
    Sandbox user for MOMO Open API
    """

    def setUp(self):
        """Initialize a few variables"""
        self.subscription_key = os.environ.get(
            'TEST_SUBSCRIPTION_KEY_FOR_COLLECTIONS', '')
        self.api_base_url = os.environ.get(
            'TEST_BASE_URL', 'https://ericssonbasicapi2.azure-api.net/v1_0')

        self.sandbox_api_user = SandboxApiUser(
            subscription_key=self.subscription_key, api_base_url=self.api_base_url)

    def test_environment_variables_are_set(self):
        """
        It requires process environment variables TEST_BASE_URL, TEST_SUBSCRIPTION_KEY
        """
        self.assertIsNotNone(self.api_base_url)
        self.assertNotEqual(self.subscription_key, '')

    def test_initialize(self):
        """
        Makes a POST request to the "apiuser" resource endpoint
        and returns a status of 201
        """
        response = self.sandbox_api_user.initialize()
        self.assertEqual(response.status_code, 201)

    def test_get_user(self):
        """
        Returns the API key and referenceId among the details of the user
        """
        response = self.sandbox_api_user.get_user()
        keys = list(response.keys())
        self.assertIn('apiKey', keys)
        self.assertIn('referenceId', keys)

# Does not work yet


"""
import SandboxApiUser from '../sandboxApiUser';

describe('sandboxApiUser', () => {


  describe('methods', () => {
    const subscriptionKey = process.env.TEST_SUBSCRIPTION_KEY_FOR_COLLECTIONS || '';
    const baseURL = process.env.TEST_BASE_URL || 'https://ericssonbasicapi2.azure-api.net/v1_0';

    const sandboxApiUser = new SandboxApiUser({ baseURL, subscriptionKey });

    describe('initialize', () => {
      it('Makes a POST request to the "apiuser" resource endpoint\
       and returns a status of 201', async () => {
        
      });
    });

    describe('getUser', () => {
      it('Returns the API key and referenceId among the details of the user', async () => {
        const response: any = await sandboxApiUser.getUser();
        expect(Object.keys(response)).toEqual(expect.arrayContaining(['apiKey', 'referenceId']));
      });
    });
  });
});
"""
