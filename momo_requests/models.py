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
    payee_note = models.TextField(default='')
    payer_message = models.TextField(default='')
    payer_party_id_type = models.CharField(max_length=100, default='MSISDN')
    payer_party_id = models.CharField(max_length=255)
    status = models.CharField(choices=STATUS_CHOICES,
                              default='PENDING', max_length=20)
    reason = models.TextField(blank=True, null=True)
    financial_transaction_id = models.CharField(
        max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
