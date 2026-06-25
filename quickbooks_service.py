import os
import requests

# QuickBooks integration using the Web API
# Real QuickBooks integration requires a complex OAuth2 flow similar to Xero.
# This is a skeleton implementation that follows the pattern used in xero_service.py.

QUICKBOOKS_REALM_ID = os.environ.get("QUICKBOOKS_REALM_ID")
QUICKBOOKS_ACCESS_TOKEN = os.environ.get("QUICKBOOKS_ACCESS_TOKEN")
QUICKBOOKS_BASE_URL = os.environ.get("QUICKBOOKS_BASE_URL", "https://sandbox-quickbooks.api.intuit.com")

def get_headers():
    return {
        "Authorization": f"Bearer {QUICKBOOKS_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def create_customer(name, email=None):
    """
    Creates a customer in QuickBooks.
    """
    if not QUICKBOOKS_ACCESS_TOKEN or not QUICKBOOKS_REALM_ID:
        return {"error": "QuickBooks credentials not configured"}

    url = f"{QUICKBOOKS_BASE_URL}/v3/company/{QUICKBOOKS_REALM_ID}/customer"
    payload = {
        "DisplayName": name,
        "PrimaryEmailAddr": {
            "Address": email
        } if email else None
    }

    try:
        response = requests.post(url, json=payload, headers=get_headers(), timeout=30)
        response.raise_for_status()
        return {"status": "success", "customer": response.json()["Customer"]}
    except Exception as e:
        return {"error": str(e)}

def create_invoice(customer_id, amount, description="Service"):
    """
    Creates an invoice in QuickBooks.
    """
    if not QUICKBOOKS_ACCESS_TOKEN or not QUICKBOOKS_REALM_ID:
        return {"error": "QuickBooks credentials not configured"}

    url = f"{QUICKBOOKS_BASE_URL}/v3/company/{QUICKBOOKS_REALM_ID}/invoice"
    payload = {
        "Line": [
            {
                "Amount": float(amount),
                "DetailType": "SalesItemLineDetail",
                "SalesItemLineDetail": {
                    "ItemRef": {
                        "value": "1", # Default Service Item
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
        response = requests.post(url, json=payload, headers=get_headers(), timeout=30)
        response.raise_for_status()
        return {"status": "success", "invoice": response.json()["Invoice"]}
    except Exception as e:
        return {"error": str(e)}

def get_company_info():
    """
    Retrieves QuickBooks company info.
    """
    if not QUICKBOOKS_ACCESS_TOKEN or not QUICKBOOKS_REALM_ID:
        return {"error": "QuickBooks credentials not configured"}

    url = f"{QUICKBOOKS_BASE_URL}/v3/company/{QUICKBOOKS_REALM_ID}/companyinfo/{QUICKBOOKS_REALM_ID}"

    try:
        response = requests.get(url, headers=get_headers(), timeout=30)
        response.raise_for_status()
        return {"status": "success", "company_info": response.json()["CompanyInfo"]}
    except Exception as e:
        return {"error": str(e)}
