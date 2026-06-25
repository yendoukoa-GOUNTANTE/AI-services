import os
import requests

AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID")

def get_headers():
    return {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }

def create_record(table_name, fields):
    """
    Creates a record in the specified Airtable table.
    """
    if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
        return {"error": "Airtable credentials not configured"}

    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table_name}"
    payload = {"fields": fields}

    try:
        response = requests.post(url, json=payload, headers=get_headers(), timeout=10)
        response.raise_for_status()
        return {"status": "success", "record": response.json()}
    except Exception as e:
        return {"error": str(e)}

def list_records(table_name, max_records=10):
    """
    Lists records from the specified Airtable table.
    """
    if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
        return {"error": "Airtable credentials not configured"}

    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table_name}"
    params = {"maxRecords": max_records}

    try:
        response = requests.get(url, params=params, headers=get_headers(), timeout=10)
        response.raise_for_status()
        return {"status": "success", "records": response.json().get("records", [])}
    except Exception as e:
        return {"error": str(e)}
