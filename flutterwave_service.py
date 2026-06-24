import os
import requests

FLUTTERWAVE_SECRET_KEY = os.environ.get('FLUTTERWAVE_SECRET_KEY')
FLUTTERWAVE_BASE_URL = 'https://api.flutterwave.com/v3'

def get_headers():
    return {
        "Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}",
        "Content-Type": "application/json"
    }

def initialize_transaction(email, amount, tx_ref, currency='NGN', callback_url=None, customizations=None):
    """
    Initializes a Flutterwave transaction.
    :param email: Customer's email address
    :param amount: Amount to charge
    :param tx_ref: Unique transaction reference
    :param currency: Currency to charge in (default NGN)
    :param callback_url: URL to redirect the user to after payment
    :param customizations: Dict with title, description, and logo
    :return: Dict with status, message and data (including link)
    """
    if not FLUTTERWAVE_SECRET_KEY:
        return {"status": "error", "message": "Flutterwave Secret Key not configured"}

    url = f"{FLUTTERWAVE_BASE_URL}/payments"
    payload = {
        "tx_ref": tx_ref,
        "amount": amount,
        "currency": currency,
        "redirect_url": callback_url,
        "customer": {
            "email": email
        },
        "customizations": customizations or {
            "title": "Yendoukoa AI",
            "description": "Payment for AI Services"
        }
    }

    try:
        response = requests.post(url, json=payload, headers=get_headers(), timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"status": "error", "message": str(e)}

def verify_transaction(transaction_id):
    """
    Verifies a Flutterwave transaction.
    :param transaction_id: Transaction ID to verify
    :return: Dict with verification details
    """
    if not FLUTTERWAVE_SECRET_KEY:
        return {"status": "error", "message": "Flutterwave Secret Key not configured"}

    url = f"{FLUTTERWAVE_BASE_URL}/transactions/{transaction_id}/verify"

    try:
        response = requests.get(url, headers=get_headers(), timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"status": "error", "message": str(e)}
