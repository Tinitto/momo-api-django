import requests
import base64
from celery import shared_task
from django.conf import settings

from momo_requests.models import MomoRequest


def create_basic_auth_header(api_user_id='', api_key=''):
    """Creates a Basic Auth header for the MOMO Open API"""
    base64_encoded_header = base64.b64encode(
        '{api_user_id}:{api_key}'.format(api_user_id=api_user_id, api_key=api_key
                                         ).encode('utf-8'))
    return 'Basic {}'.format(base64_encoded_header.decode('utf-8'))


@shared_task
def authenticate_with_momo():
    """
    Authenticates with the MOMO API to return an
    {
        "access_token": "string",
        "token_type": "string",
        "expires_in": 0
    }
    """
    endpoint_url = "{}/collection/token/".format(settings.MOMO_BASE_URL)
    basic_auth_header = create_basic_auth_header(
        api_user_id=settings.MOMO_API_USER_ID, api_key=settings.MOMO_API_KEY)
    headers = {
        'Authorization': basic_auth_header,
        'Ocp-Apim-Subscription-Key': settings.MOMO_SUBSCRIPTION_KEY_FOR_COLLECTIONS
    }
    response = requests.post(endpoint_url, headers=headers)
    if(response.ok):
        return response.json()


@shared_task
def request_for_payment(momo_request_id):
    """
    Makes a remote request to the MOMO API
    to request for payment from a payer
    """
    auth_response = authenticate_with_momo()

    if auth_response:
        # get the MomoRequest
        # pylint: disable=no-member
        momo_request = MomoRequest.objects.get(id=momo_request_id)
        endpoint_url = '{}/collection/v1_0/requesttopay'.format(
            settings.MOMO_BASE_URL)

        headers = {
            'Authorization': 'Bearer {}'.format(auth_response['access_token']),
            'X-Reference-Id': str(momo_request.reference_id),
            'X-Target-Environment': settings.MOMO_TARGET_ENVIRONMENT,
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': settings.MOMO_SUBSCRIPTION_KEY_FOR_COLLECTIONS
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

        payment_response = requests.post(
            endpoint_url, data=data, headers=headers)

        if not payment_response.ok:
            momo_request.status = 'FAILED'
            momo_request.save()
    else:
        raise Exception('Failed to authenticate with MOMO API')


def update_payment_status(momo_request):
    """
    Calls the MOMO api to determine the status of 
    the MomoRequest
    """
    # poll only payments that have 'PENDING' status
    if momo_request.status != 'PENDING':
        return

    auth_response = authenticate_with_momo()
    if auth_response:
        endpoint_url = '{0}/collection/v1_0/requesttopay/{1}'.format(
            settings.MOMO_BASE_URL, str(momo_request.reference_id))
        headers = {
            'Authorization': 'Bearer {}'.format(auth_response['access_token']),
            'X-Target-Environment': settings.MOMO_TARGET_ENVIRONMENT,
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': settings.MOMO_SUBSCRIPTION_KEY_FOR_COLLECTIONS
        }

        api_response = requests.get(endpoint_url, headers=headers)
        parsed_response = api_response.json()
        status = parsed_response.get('status')

        if(api_response.status_code == 404):
            momo_request.status = parsed_response.get('code')
            momo_request.reason = parsed_response.get('message')
            momo_request.save()

        elif(api_response.ok and status != 'PENDING'):
            momo_request.status = status
            momo_request.reason = parsed_response.get(
                'reason', {}).get('message', '')
            momo_request.financial_transaction_id = parsed_response.get(
                'financialTransactionId')
            momo_request.save()

    else:
        raise Exception('Failed to authenticate with MOMO API')


@shared_task
def update_status_for_all_pending_payments():
    """
    Retrieves all MomoRequest instances that have pending
    status and loops through each updating the status
    """
    # pylint: disable=no-member
    all_pending_momo_requests = MomoRequest.objects.filter(status='PENDING')
    for momo_request in all_pending_momo_requests:
        update_payment_status(momo_request)
