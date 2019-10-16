# import uuid
# from datetime import datetime
from django.test import TestCase
from django.conf import settings
from unittest.mock import patch
from momo_requests.models import MomoRequest
from momo_requests.tasks import create_basic_auth_header,\
    request_for_payment, authenticate_with_momo,\
    update_payment_status, update_status_for_all_pending_payments


class MomoRequestTasksTest(TestCase):
    """Tests for the momo_requests.tasks"""

    def setUp(self):
        """Initialize a few variables"""
        self.amount = 500
        self.currency = 'EUR'
        self.payer_party_id = '46733123453'
        self.dummy_auth_response = {"access_token": "hi",
                                    "token_type": "you",
                                    "expires_in": 3600}
        self.base_headers = {
            'X-Target-Environment': settings.MOMO_TARGET_ENVIRONMENT,
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': settings.MOMO_SUBSCRIPTION_KEY_FOR_COLLECTIONS
        }

    def test_create_basic_auth_header(self):
        """Creates a Basic header for a given api user id and api key"""
        api_user_id = 'hello'
        api_key = 'world'
        self.assertEqual(create_basic_auth_header(
            api_user_id=api_user_id, api_key=api_key), 'Basic aGVsbG86d29ybGQ=')

    @patch('momo_requests.tasks.requests.post')
    def test_authenticate_with_momo(self, mock_post):
        """
        the authenticate_with_momo() task returns an access_token
        for the current MOMO_API_USER_ID and MOMO_API_KEY
        """
        collections_auth_url = 'https://sandbox.momodeveloper.mtn.com/collection/token/'
        basic_auth_header = create_basic_auth_header(
            api_user_id=settings.MOMO_API_USER_ID, api_key=settings.MOMO_API_KEY)
        headers = {
            'Authorization': basic_auth_header,
            'Ocp-Apim-Subscription-Key': settings.MOMO_SUBSCRIPTION_KEY_FOR_COLLECTIONS
        }
        expected_result = self.dummy_auth_response

        mock_post.return_value.json.return_value = expected_result
        response = authenticate_with_momo()

        mock_post.assert_called_once_with(
            collections_auth_url, headers=headers)
        self.assertEqual(response, expected_result)

    @patch('momo_requests.tasks.authenticate_with_momo')
    @patch('momo_requests.tasks.requests.post')
    def test_request_for_payment(self, mock_post, mock_authenticate_with_momo):
        """
        the 'request_for_payment' task creates a new payment request
        on the MOMO Open API for the MomoRequest whose id is passed to it
        """
        collections_post_url = 'https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay'
        # pylint: disable=no-member
        momo_request = MomoRequest.objects.create(
            amount=self.amount, currency=self.currency,
            payer_party_id=self.payer_party_id
        )
        auth_response = self.dummy_auth_response
        mock_authenticate_with_momo.return_value = auth_response
        headers = {
            'Authorization': 'Bearer {}'.format(auth_response['access_token']),
            'X-Reference-Id': str(momo_request.reference_id),
            **self.base_headers
        }
        data = {
            'amount': momo_request.amount,
            'currency': momo_request.currency,
            'externalId': str(momo_request.external_id),
            'payer': {
                'partyIdType': momo_request.payer_party_id_type,
                'partyId': momo_request.payer_party_id,
            },
            'payerMessage': momo_request.payer_message,
            'payeeNote': momo_request.payee_note
        }
        request_for_payment(momo_request.id)
        mock_post.assert_called_once_with(
            collections_post_url, data=data, headers=headers)

    @patch('momo_requests.tasks.authenticate_with_momo')
    @patch('momo_requests.tasks.requests.get')
    def test__update_payment_status_remote_call(self, mock_get, mock_authenticate_with_momo):
        """
        __update_payment_status function makes updates the status of
        the MomoRequest passed to it if the status
        """
        # pylint: disable=no-member
        momo_request = MomoRequest.objects.create(
            amount=self.amount, currency=self.currency,
            payer_party_id=self.payer_party_id
        )
        single_collection_url = 'https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay/{}'.format(
            str(momo_request.reference_id))
        headers = {
            'Authorization': 'Bearer {}'.format(self.dummy_auth_response['access_token']),
            **self.base_headers
        }

        mock_authenticate_with_momo.return_value = self.dummy_auth_response
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = momo_request.__dict__

        update_payment_status(momo_request)

        mock_get.assert_called_once_with(
            single_collection_url, headers=headers)

    @patch('momo_requests.tasks.authenticate_with_momo')
    @patch('momo_requests.tasks.requests.get')
    def test__update_payment_status_update_process(
            self, mock_get, mock_authenticate_with_momo):
        """
        __update_payment_status task updates the MomoRequest object
        passed to it
        """
        # pylint: disable=no-member
        momo_request = MomoRequest.objects.create(
            amount=self.amount, currency=self.currency,
            payer_party_id=self.payer_party_id
        )
        expected_response = {'status': 'SUCCESSFUL', 'reason': {
            'message': 'hello world'}, 'financialTransactionId': '234356'}

        mock_authenticate_with_momo.return_value = self.dummy_auth_response
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = expected_response

        update_payment_status(momo_request)

        self.assertEqual(momo_request.status, expected_response['status'])
        self.assertEqual(momo_request.reason,
                         expected_response['reason']['message'])
        self.assertEqual(momo_request.financial_transaction_id,
                         expected_response['financialTransactionId'])

    @patch('momo_requests.tasks.update_payment_status')
    @patch('momo_requests.models.MomoRequest.objects.filter')
    def test_update_status_for_all_pending_payments(
            self, mock_momo_requests_objects_filter, mock_update_payment_status):
        """
        update_status_for_all_pending_payments updates the status of all
        MomoRequest objects with PENDING status if the status has changed on API
        """
        # pylint: disable=no-member
        momo_requests = [MomoRequest.objects.create(
            amount=self.amount, currency=self.currency,
            payer_party_id=self.payer_party_id
        ) for num in range(0, 3)]
        mock_momo_requests_objects_filter.return_value = momo_requests

        update_status_for_all_pending_payments()

        mock_momo_requests_objects_filter.assert_called_once_with(
            status='PENDING')
        mock_update_payment_status.assert_any_call(momo_requests[0])
        mock_update_payment_status.assert_any_call(momo_requests[1])
        mock_update_payment_status.assert_any_call(momo_requests[2])
