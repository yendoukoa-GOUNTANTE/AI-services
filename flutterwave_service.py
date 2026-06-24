import os
import requests
import uuid

FLUTTERWAVE_SECRET_KEY = os.environ.get('FLUTTERWAVE_SECRET_KEY')
FLUTTERWAVE_BASE_URL = 'https://api.flutterwave.com/v3'

def get_headers():
    return {
        "Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}",
        "Content-Type": "application/json"
    }

def initialize_transaction(email, amount, currency="NGN", callback_url=None, metadata=None):
    """
    Initializes a Flutterwave transaction.
    """
    if not FLUTTERWAVE_SECRET_KEY:
        return {"status": "error", "message": "Flutterwave Secret Key not configured"}

    url = f"{FLUTTERWAVE_BASE_URL}/payments"
    tx_ref = str(uuid.uuid4())

    payload = {
        "tx_ref": tx_ref,
        "amount": str(amount),
        "currency": currency,
        "redirect_url": callback_url,
        "customer": {
            "email": email
        },
        "meta": metadata,
        "customizations": {
            "title": "Yendoukoa AI Payment",
            "logo": "https://yendoukoa.ai/logo.png"
        }
    }

    try:
        response = requests.post(url, json=payload, headers=get_headers(), timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"status": "error", "message": str(e)}

def verify_transaction(transaction_id):
    """
    Verifies a Flutterwave transaction.
    """
    if not FLUTTERWAVE_SECRET_KEY:
        return {"status": "error", "message": "Flutterwave Secret Key not configured"}

    url = f"{FLUTTERWAVE_BASE_URL}/transactions/{transaction_id}/verify"

    try:
        response = requests.get(url, headers=get_headers(), timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"status": "error", "message": str(e)}
