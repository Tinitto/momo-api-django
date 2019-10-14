from django.db.models.signals import post_save
from django.dispatch import receiver

from momo_requests.models import MomoRequest
from momo_requests.tasks import request_for_payment


@receiver(post_save, sender=MomoRequest)
def make_momo_collection_request(sender, instance, created, **kwargs):
    if created:
        # Run only on creation of the MomoRequest
        request_for_payment.delay(instance)
