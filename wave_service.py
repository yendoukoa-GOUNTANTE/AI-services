import os
import requests

WAVE_ACCESS_TOKEN = os.environ.get("WAVE_ACCESS_TOKEN")
WAVE_BUSINESS_ID = os.environ.get("WAVE_BUSINESS_ID")

BASE_URL = "https://gql.waveapps.com/graphql/public"

def get_headers():
    return {
        "Authorization": f"Bearer {WAVE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

def execute_query(query, variables=None):
    if not WAVE_ACCESS_TOKEN:
        return {"error": "Wave access token not configured"}

    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    try:
        response = requests.post(BASE_URL, json=payload, headers=get_headers(), timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def create_customer(name, email=None):
    """
    Creates a customer in Wave.
    """
    if not WAVE_BUSINESS_ID:
        return {"error": "Wave Business ID not configured"}

    query = """
    mutation ($input: CustomerCreateInput!) {
      customerCreate(input: $input) {
        didSucceed
        inputErrors {
          code
          message
          path
        }
        customer {
          id
          name
          email
        }
      }
    }
    """
    variables = {
        "input": {
            "businessId": WAVE_BUSINESS_ID,
            "name": name,
            "email": email
        }
    }

    result = execute_query(query, variables)
    if "error" in result:
        return result

    data = result.get("data", {}).get("customerCreate", {})
    if data.get("didSucceed"):
        return {"status": "success", "customer": data["customer"]}
    else:
        return {"error": data.get("inputErrors", [{"message": "Unknown error"}])[0]["message"]}

def create_invoice(customer_id, amount, description="Service"):
    """
    Creates a draft invoice in Wave.
    """
    if not WAVE_BUSINESS_ID:
        return {"error": "Wave Business ID not configured"}

    query = """
    mutation ($input: InvoiceCreateInput!) {
      invoiceCreate(input: $input) {
        didSucceed
        inputErrors {
          code
          message
          path
        }
        invoice {
          id
          invoiceNumber
          total {
            value
            currency {
              code
            }
          }
        }
      }
    }
    """

    # We need a product/service ID. In a real app, you'd fetch this.
    # For the skeleton, we'll assume a standard item ID or require one.
    item_id = os.environ.get("WAVE_ITEM_ID")
    if not item_id:
        return {"error": "WAVE_ITEM_ID not configured"}

    variables = {
        "input": {
            "businessId": WAVE_BUSINESS_ID,
            "customerId": customer_id,
            "items": [
                {
                    "productId": item_id,
                    "description": description,
                    "quantity": "1",
                    "unitPrice": str(amount)
                }
            ]
        }
    }

    result = execute_query(query, variables)
    if "error" in result:
        return result

    data = result.get("data", {}).get("invoiceCreate", {})
    if data.get("didSucceed"):
        return {"status": "success", "invoice": data["invoice"]}
    else:
        return {"error": data.get("inputErrors", [{"message": "Unknown error"}])[0]["message"]}
