import os
import requests

# QuickBooks integration usually requires OAuth2 flow.
# This is a skeleton that assumes an access token is available.

QUICKBOOKS_REALM_ID = os.environ.get("QUICKBOOKS_REALM_ID")
QUICKBOOKS_ENVIRONMENT = os.environ.get("QUICKBOOKS_ENVIRONMENT", "sandbox") # 'sandbox' or 'production'

BASE_URL = "https://sandbox-quickbooks.api.intuit.com" if QUICKBOOKS_ENVIRONMENT == "sandbox" else "https://quickbooks.api.intuit.com"

def get_headers():
    token = os.environ.get("QUICKBOOKS_ACCESS_TOKEN")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def create_customer(display_name, email=None):
    """
    Creates a customer in QuickBooks.
    """
    if not QUICKBOOKS_REALM_ID:
        return {"error": "QuickBooks Realm ID not configured"}

    url = f"{BASE_URL}/v3/company/{QUICKBOOKS_REALM_ID}/customer"
    payload = {
        "DisplayName": display_name
    }
    if email:
        payload["PrimaryEmailAddr"] = {"Address": email}

    try:
        response = requests.post(url, json=payload, headers=get_headers(), timeout=10)
        response.raise_for_status()
        return {"status": "success", "customer": response.json()}
    except Exception as e:
        return {"error": str(e)}

def create_invoice(customer_id, amount, description="Service"):
    """
    Creates an invoice in QuickBooks.
    """
    if not QUICKBOOKS_REALM_ID:
        return {"error": "QuickBooks Realm ID not configured"}

    url = f"{BASE_URL}/v3/company/{QUICKBOOKS_REALM_ID}/invoice"
    payload = {
        "Line": [
            {
                "Amount": float(amount),
                "DetailType": "SalesItemLineDetail",
                "SalesItemLineDetail": {
                    "ItemRef": {
                        "value": "1", # Default Service item usually
                        "name": "Services"
                    }
                },
                "Description": description
            }
        ],
        "CustomerRef": {
            "value": customer_id
        }
    }

    try:
        response = requests.post(url, json=payload, headers=get_headers(), timeout=10)
        response.raise_for_status()
        return {"status": "success", "invoice": response.json()}
    except Exception as e:
        return {"error": str(e)}
