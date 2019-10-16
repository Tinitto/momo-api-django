import uuid

from django.test import TestCase
from datetime import datetime
from unittest.mock import patch

from momo_requests.models import MomoRequest


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
            amount=self.amount, currency=self.currency,
            payer_party_id=self.payer_party_id
        )

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

    @patch('momo_requests.signals.request_for_payment.delay')
    def test_request_for_payment_post_save(self, mock_request_for_payment):
        """
        After a new MomoRequest is created, a payment request is created
        on the MOMO Open API for it by request_for_payment.delay(momo_request.id)
        """
        # pylint: disable=no-member
        request = MomoRequest.objects.create(
            amount=self.amount, currency=self.currency,
            payer_party_id=self.payer_party_id
        )

        mock_request_for_payment.assert_called_once_with(request.id)
