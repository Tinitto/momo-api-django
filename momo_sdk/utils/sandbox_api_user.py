"""
Module to generate credentials for the Sandbox User MOMO API
The Logic has been ported by Martin Ahindura from the TypeScript mtn-pay-js package
https://github.com/sopherapps/mtn-pay-js/blob/master/src/sandboxApiUser/index.ts
"""

import uuid
from .repository import RemoteResource


class SandboxApiUser:
    """A class for the Sandbox api user credentials to be used during testing"""

    def __init__(self, subscription_key, api_base_url='https://ericssonbasicapi2.azure-api.net/v1_0', provider_callback_host='https://example.com',):
        self.reference_id = str(uuid.uuid4())
        self.provider_callback_host = provider_callback_host
        self.api_key = ''
        self.provider_callback_host = ''
        self.target_environment = ''

        api_user_url = 'apiuser'
        api_key_url = "apiuser/{}/apikey".format(self.reference_id)
        common_headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': subscription_key,
        }

        self.api_user_resource = RemoteResource(
            api_user_url, api_base_url=api_base_url, common_headers=common_headers)

        self.api_key_resource = RemoteResource(
            api_key_url, api_base_url=api_base_url, common_headers=common_headers)

    def initialize(self):
        """Creates the user"""
        headers = {
            'X-Reference-Id': self.reference_id,
        }
        return self.api_user_resource.create(
            {"providerCallbackHost": self.provider_callback_host}, headers=headers)

    def __get_remote_api_key(self):
        """Creates the API key"""
        response = self.api_key_resource.create({})
        if(response.status_code == 201):
            self.api_key = response.json()['apiKey']

    def __get_remote_user_details(self):
        """Returns the user's details"""
        response = self.api_user_resource.get_one(self.reference_id)
        if (response.status == 200):
            data = response.json()
            self.target_environment = data['targetEnvironment']
            self.provider_callback_host = data['providerCallbackHost']

    def get_user(self):
        """returns the users details in a MOMO open api format"""
        if (self.api_key is None):
            self.__get_remote_api_key()

        if (self.target_environment is None):
            self.__get_remote_user_details()

        return {
            'apiKey': self.api_key,
            'providerCallbackHost': self.provider_callback_host,
            'referenceId': self.reference_id,
            'targetEnvironment': self.target_environment,
        }
