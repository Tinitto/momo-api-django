import uuid
from datetime import datetime
from django.test import TestCase
from momo_requests.models import MomoRequest

# Create your tests here.


class MomoRequestModelTest(TestCase):
    """
    Tests for the MomoRequest model
    """

    def setUp(self):
        """Initialize a few variables"""
        self.amount = 500
        self.currency = 'EUR'
        self.payer_party_id = '46733123453'

    def test_model_create(self):
        """Creates a MomoRequest object with appropriate defaults"""
        # pylint: disable=no-member
        request = MomoRequest.objects.create(
            amount=self.amount, currency=self.currency, payer_party_id=self.payer_party_id)

        self.assertEqual(request.amount, self.amount)
        self.assertEqual(request.currency, self.currency)
        self.assertEqual(request.payer_party_id, self.payer_party_id)

        self.assertIsInstance(request.external_id, uuid.UUID)
        self.assertIsInstance(request.reference_id, uuid.UUID)

        self.assertEqual(request.payee_note, '')
        self.assertEqual(request.payer_message, '')
        self.assertEqual(request.payer_party_id_type, 'MSISDN')
        self.assertEqual(request.status, 'PENDING')
        self.assertEqual(request.reason, None)
        self.assertEqual(request.financial_transaction_id, None)

        self.assertIsInstance(request.created_at, datetime)
        self.assertIsInstance(request.last_modified_at, datetime)

    def test_request_for_payment_post_save(self):
        """
        After a new MomoRequest is created, a payment request is created
        on the MOMO Open API for it
        """
        pass


class MomoRequestTasksTest(TestCase):
    """Tests for the momo_requests.tasks"""

    def setUp(self):
        """Initialize a few variables"""
        pass

    def test_authenticate_with_momo(self):
        """
        the authenticate_with_momo() task returns an access_token
        for the current API_USER and API_KEY
        """
        pass

    def test_request_for_payment(self):
        """
        the 'request_for_payment' task creates a new payment request
        on the MOMO Open API for the MomoRequest whose id is passed to it 
        """
        pass

    def test__update_payment_status(self):
        """
        __update_payment_status function makes updates the status of 
        the MomoRequest passed to it if the status was PENDING originally
        """
        pass

    def test_update_status_for_all_pending_payments(self):
        """
        update_status_for_all_pending_payments updates the status of all 
        MomoRequest objects with PENDING status if the status has changed on API
        """
        pass
