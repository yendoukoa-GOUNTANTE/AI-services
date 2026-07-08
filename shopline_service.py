import os
import requests
from typing import Dict, Any, Optional

def get_headers():
    access_token = os.getenv('SHOPLINE_ACCESS_TOKEN')
    return {
        "YY-Access-Token": access_token,
        "Content-Type": "application/json"
    }

def create_product(title: str, body_html: str = "", vendor: str = "", product_type: str = "", price: str = "0.00") -> Dict[str, Any]:
    """
    Creates a product on Shopline using the REST Admin API.
    """
    store_handle = os.getenv('SHOPLINE_STORE_HANDLE')
    if not store_handle:
        return {"error": "SHOPLINE_STORE_HANDLE not configured"}

    url = f"https://{store_handle}.myshopline.com/admin/api/2022-09/products.json"

    product_data = {
        "product": {
            "title": title,
            "body_html": body_html,
            "vendor": vendor,
            "product_type": product_type,
            "variants": [
                {
                    "price": price
                }
            ]
        }
    }

    try:
        response = requests.post(url, headers=get_headers(), json=product_data, timeout=30)
        if response.status_code == 201:
            return response.json()
        else:
            return {"error": f"Shopline API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": str(e)}
