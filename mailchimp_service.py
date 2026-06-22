import os
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

def get_mailchimp_client():
    api_key = os.environ.get("MAILCHIMP_API_KEY")
    server_prefix = os.environ.get("MAILCHIMP_SERVER_PREFIX")

    if not api_key or not server_prefix:
        return None, "Mailchimp API key or Server Prefix not configured"

    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": api_key,
        "server": server_prefix
    })
    return client, None

def subscribe_to_newsletter(email, list_id=None):
    client, config_error = get_mailchimp_client()
    if config_error:
        return {"error": config_error, "code": "CONFIG_ERROR"}

    if not list_id:
        list_id = os.environ.get("MAILCHIMP_LIST_ID")

    if not list_id:
        return {"error": "Mailchimp List ID not configured", "code": "CONFIG_ERROR"}

    try:
        response = client.lists.add_list_member(list_id, {
            "email_address": email,
            "status": "subscribed",
        })
        return {"status": "success", "id": response['id']}
    except ApiClientError as e:
        return {"error": str(e.text), "code": "API_ERROR"}
    except Exception as e:
        return {"error": str(e), "code": "RUNTIME_ERROR"}

def create_campaign(subject_line, preview_text, title, from_name, reply_to, list_id=None):
    client, config_error = get_mailchimp_client()
    if config_error:
        return {"error": config_error, "code": "CONFIG_ERROR"}

    if not list_id:
        list_id = os.environ.get("MAILCHIMP_LIST_ID")

    if not list_id:
        return {"error": "Mailchimp List ID not configured", "code": "CONFIG_ERROR"}

    try:
        campaign_config = {
            "type": "regular",
            "recipients": {
                "list_id": list_id
            },
            "settings": {
                "subject_line": subject_line,
                "preview_text": preview_text,
                "title": title,
                "from_name": from_name,
                "reply_to": reply_to
            }
        }
        response = client.campaigns.create(campaign_config)
        return {"status": "success", "id": response['id']}
    except ApiClientError as e:
        return {"error": str(e.text), "code": "API_ERROR"}
    except Exception as e:
        return {"error": str(e), "code": "RUNTIME_ERROR"}

def set_campaign_content(campaign_id, html_content):
    client, config_error = get_mailchimp_client()
    if config_error:
        return {"error": config_error, "code": "CONFIG_ERROR"}

    try:
        response = client.campaigns.set_content(campaign_id, {"html": html_content})
        return {"status": "success"}
    except ApiClientError as e:
        return {"error": str(e.text), "code": "API_ERROR"}
    except Exception as e:
        return {"error": str(e), "code": "RUNTIME_ERROR"}

def send_campaign(campaign_id):
    client, config_error = get_mailchimp_client()
    if config_error:
        return {"error": config_error, "code": "CONFIG_ERROR"}

    try:
        client.campaigns.send(campaign_id)
        return {"status": "success"}
    except ApiClientError as e:
        return {"error": str(e.text), "code": "API_ERROR"}
    except Exception as e:
        return {"error": str(e), "code": "RUNTIME_ERROR"}

def get_campaign_reports():
    client, config_error = get_mailchimp_client()
    if config_error:
        return {"error": config_error, "code": "CONFIG_ERROR"}

    try:
        response = client.reports.get_all_campaign_reports()
        return {"status": "success", "reports": response['reports']}
    except ApiClientError as e:
        return {"error": str(e.text), "code": "API_ERROR"}
    except Exception as e:
        return {"error": str(e), "code": "RUNTIME_ERROR"}
