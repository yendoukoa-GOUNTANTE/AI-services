import os
import requests
from flask import current_app

PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')
PAYSTACK_BASE_URL = 'https://api.paystack.co'

def get_headers():
    return {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

def initialize_transaction(email, amount, callback_url=None, metadata=None):
    """
    Initializes a Paystack transaction.
    :param email: Customer's email address
    :param amount: Amount in kobo (lowest currency unit)
    :param callback_url: URL to redirect the user to after payment
    :param metadata: JSON object with additional information
    :return: Dict with status, message and data (including authorization_url and reference)
    """
    if not PAYSTACK_SECRET_KEY:
        return {"status": False, "message": "Paystack Secret Key not configured"}

    url = f"{PAYSTACK_BASE_URL}/transaction/initialize"
    payload = {
        "email": email,
        "amount": amount,
        "callback_url": callback_url,
        "metadata": metadata
    }

    try:
        response = requests.post(url, json=payload, headers=get_headers(), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"status": False, "message": str(e)}

def verify_transaction(reference):
    """
    Verifies a Paystack transaction.
    :param reference: Transaction reference to verify
    :return: Dict with verification details
    """
    if not PAYSTACK_SECRET_KEY:
        return {"status": False, "message": "Paystack Secret Key not configured"}

    url = f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}"

    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"status": False, "message": str(e)}
