import os
from xero_python.accounting.api import AccountingApi
from xero_python.api_client import ApiClient
from xero_python.api_client.configuration import Configuration
from xero_python.api_client.oauth2 import OAuth2Token

# In a real application, you would handle OAuth2 token refresh and storage properly.
# For this integration, we provide a skeleton that uses environment variables for configuration.

XERO_TENANT_ID = os.environ.get("XERO_TENANT_ID")

def get_xero_client():
    # This is a simplified client initialization.
    # Real Xero integration requires a complex OAuth2 flow.
    # Here we assume some mechanism provides a valid token.
    token = os.environ.get("XERO_ACCESS_TOKEN")
    if not token or not XERO_TENANT_ID:
        return None

    config = Configuration()
    api_client = ApiClient(configuration=config)
    # Mocking the token attachment
    api_client.oauth2_token = OAuth2Token(access_token=token)
    return AccountingApi(api_client)

def create_contact(name, email=None):
    """
    Creates a contact in Xero. Checks if it exists first.
    """
    api_instance = get_xero_client()
    if not api_instance:
        return {"error": "Xero credentials not configured"}

    from xero_python.accounting.models import Contact, Contacts

    try:
        # Check if contact exists
        where = f'Name=="{name}"'
        existing_contacts = api_instance.get_contacts(XERO_TENANT_ID, where=where)
        if existing_contacts.contacts:
            return {"status": "success", "contact": existing_contacts.contacts[0].to_dict(), "existed": True}

        contact = Contact(name=name, email_address=email)
        contacts = Contacts(contacts=[contact])

        result = api_instance.create_contacts(XERO_TENANT_ID, contacts)
        return {"status": "success", "contact": result.contacts[0].to_dict(), "existed": False}
    except Exception as e:
        return {"error": str(e)}

def create_invoice(contact_id, amount, description="Service"):
    """
    Creates an invoice in Xero.
    """
    api_instance = get_xero_client()
    if not api_instance:
        return {"error": "Xero credentials not configured"}

    from xero_python.accounting.models import Invoice, LineItem, Contact, Invoices
    import datetime

    line_item = LineItem(
        description=description,
        quantity=1.0,
        unit_amount=float(amount),
        account_code="200" # Example Sales account
    )

    invoice = Invoice(
        type="ACCREC",
        contact=Contact(contact_id=contact_id),
        line_items=[line_item],
        date=datetime.date.today(),
        due_date=datetime.date.today() + datetime.timedelta(days=30),
        status="DRAFT"
    )

    invoices = Invoices(invoices=[invoice])

    try:
        result = api_instance.create_invoices(XERO_TENANT_ID, invoices)
        return {"status": "success", "invoice": result.invoices[0].to_dict()}
    except Exception as e:
        return {"error": str(e)}
