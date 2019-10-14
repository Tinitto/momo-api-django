"""
This module holds the base product for all Momo Pay Products
i.e. Collections, Disbursements, Remittances etc.
It is ported by Martin Ahindura from the mtn-pay-js package
https://github.com/sopherapps/mtn-pay-js/blob/master/src/core/index.ts
"""
import base64
from datetime import datetime
from .utils.repository import RemoteResource


def seconds_since(starting_time):
    """
    Returns the number of seconds between now and the given startingTime
    """
    return (datetime.now() - starting_time).seconds


class BaseProduct:
    """
    Base class for all products including account,
    paymentRequests, remittances and disbursements
    """

    def __init__(self, subscription_key='', api_key='', apiuser_id='',
                 auth_base_url='https://ericssonbasicapi2.azure-api.net/collection',
                 auth_url='token/', target_environment='sandbox'):
        authorization_header = base64.b64encode(
            "{apiuser_id}: {api_key}".format(apiuser_id=apiuser_id, api_key=api_key))
        self.common_headers = {
            'Authorization': "Basic {}".format(authorization_header),
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': subscription_key,
            'X-Target-Environment': target_environment,
        }
        self.auth_resource = RemoteResource(
            auth_url, auth_base_url, common_headers=self.common_headers)
        self.api_token = None

    def authenticate(self):
        """
        Authenticates with remote api if the apiToken is expired or non-existent
        """
        if self.should_authenticate():
            response = self.auth_resource.create({})
            if response.status_code in [200, 201, 202]:
                self.api_token = response.json()
                self.api_token['created_at'] = datetime.now()

    def should_authenticate(self):
        """
        Checks whether the apiToken has expired or not; or whether it is exists or not
        """
        if self.api_token is None:
            return True
        token_age_in_seconds = seconds_since(self.api_token.created_at)
        return token_age_in_seconds >= self.api_token.expires_in
