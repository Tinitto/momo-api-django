import uuid
from django.db import models

# Create your models here.

STATUS_CHOICES = (
    ('SUCCESSFUL', 'SUCCESSFUL'),
    ('FAILED', 'FAILED'),
    ('PENDING', 'PENDING')
)


class MomoRequest(models.Model):
    """A model for Collection/Disbursement objects"""
    amount = models.FloatField()
    currency = models.CharField(max_length=10)
    external_id = models.UUIDField(unique=True, default=uuid.uuid4)
    reference_id = models.UUIDField(unique=True, default=uuid.uuid4)
    payee_note = models.TextField()
    payer_message = models.TextField()
    payer_party_id_type = models.CharField(max_length=100)
    payer_party_id = models.BigIntegerField()
    status = models.CharField(choices=STATUS_CHOICES, default='PENDING')
    reason = models.TextField()
    financial_transaction_id = models.CharField(max_length=255)
