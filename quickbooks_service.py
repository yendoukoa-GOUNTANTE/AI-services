import os
import requests

QUICKBOOKS_CLIENT_ID = os.environ.get('QUICKBOOKS_CLIENT_ID')
QUICKBOOKS_CLIENT_SECRET = os.environ.get('QUICKBOOKS_CLIENT_SECRET')
QUICKBOOKS_REALM_ID = os.environ.get('QUICKBOOKS_REALM_ID')
QUICKBOOKS_BASE_URL = 'https://quickbooks.api.intuit.com/v3' # Change to sandbox if needed

def get_quickbooks_info():
    """
    Returns basic QuickBooks integration info.
    Actual implementation would require OAuth2 token management.
    """
    if not all([QUICKBOOKS_CLIENT_ID, QUICKBOOKS_CLIENT_SECRET, QUICKBOOKS_REALM_ID]):
        return {"error": "QuickBooks credentials not fully configured"}

    return {
        "client_id": QUICKBOOKS_CLIENT_ID[:5] + "...",
        "realm_id": QUICKBOOKS_REALM_ID,
        "status": "Configured (OAuth2 token required for API calls)"
    }

def get_company_info(access_token):
    """
    Retrieves QuickBooks company info using an access token.
    """
    if not QUICKBOOKS_REALM_ID:
        return {"error": "QuickBooks Realm ID not configured"}

    url = f"{QUICKBOOKS_BASE_URL}/company/{QUICKBOOKS_REALM_ID}/companyinfo/{QUICKBOOKS_REALM_ID}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
