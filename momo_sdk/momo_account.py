"""
This is a module that utilities to do with the account endpoint of the MOMO Open API
It has been ported by Martin Ahindura from the mtn-pay-js Typescript package
https://github.com/sopherapps/mtn-pay-js/blob/master/src/account/index.ts
"""
from .base_momo_product import BaseProduct
from .utils.repository import RemoteResource
from datetime import datetime

ACCOUNT_TYPES = {
    'COLLECTION': 'collection',
    'DISBURSEMENT': 'disbursement',
    'REMITTANCE': 'remittance',
}


class MomoAccount(BaseProduct):
    """
    Details about a Momo account
    """

    def __init__(self, account_type, config):
        self.last_modified = None
        self.__details = None
        auth_base_url = config.get('auth_base_url',
                                   'https://ericssonbasicapi2.azure-api.net/{}'.format(
                                       account_type))

        super(MomoAccount, self).__init__(
            **config, auth_base_url=auth_base_url)

        api_base_url = config.get('api_base_url',
                                  "https://ericssonbasicapi2.azure-api.net/{}/v1_0".format(
                                      account_type))

        self.__account_resource = RemoteResource(
            'account', api_base_url, common_headers=self.common_headers)

    def get_details(self, force_refresh=False):
        """Returns the details in the account e.g. balance, currency"""
        self.authenticate()

        if force_refresh and self.last_modified is None:
            headers = {'Authorization': "Bearer {}".format(
                self.api_token['access_token'])}
            response = self.__account_resource.get_one(
                'balance', headers=headers)

            json_response = response.json()
            if response.status_code == 200:
                self.__details = {
                    'balance': float(json_response['availableBalance']),
                    'currency': json_response['currency']
                }
                self.last_modified = datetime.now()
            else:
                message = json_response.get('message', 'Error making request')
                raise Exception(message)

        return self.__details
