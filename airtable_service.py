import os
from pyairtable import Api

# Airtable integration using pyairtable
# Real integration requires AIRTABLE_ACCESS_TOKEN and AIRTABLE_BASE_ID

AIRTABLE_ACCESS_TOKEN = os.environ.get("AIRTABLE_ACCESS_TOKEN")
AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID")

def get_airtable_api():
    if not AIRTABLE_ACCESS_TOKEN:
        return None
    return Api(AIRTABLE_ACCESS_TOKEN)

def create_record(table_name, fields):
    """
    Creates a record in a specific Airtable table.
    """
    api = get_airtable_api()
    if not api or not AIRTABLE_BASE_ID:
        return {"error": "Airtable credentials not configured"}

    try:
        table = api.table(AIRTABLE_BASE_ID, table_name)
        record = table.create(fields)
        return {"status": "success", "record": record}
    except Exception as e:
        return {"error": str(e)}

def list_records(table_name, max_records=10):
    """
    Lists records from a specific Airtable table.
    """
    api = get_airtable_api()
    if not api or not AIRTABLE_BASE_ID:
        return {"error": "Airtable credentials not configured"}

    try:
        table = api.table(AIRTABLE_BASE_ID, table_name)
        records = table.all(max_records=max_records)
        return {"status": "success", "records": records}
    except Exception as e:
        return {"error": str(e)}
