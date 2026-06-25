import pytest
from unittest.mock import patch

def test_airtable_assistance_endpoint(client, auth_headers):
    with patch('google_ai.provide_airtable_assistance') as mock_ai:
        mock_ai.return_value = "Airtable advice"
        response = client.post('/api/v1/database/airtable/assistance',
                               json={'prompt': 'How to use Airtable?'},
                               headers=auth_headers)
        assert response.status_code == 200
        assert response.json['message'] == "Airtable advice"

def test_quickbooks_assistance_endpoint(client, auth_headers):
    with patch('google_ai.provide_quickbooks_assistance') as mock_ai:
        mock_ai.return_value = "QuickBooks advice"
        response = client.post('/api/v1/finance/quickbooks/assistance',
                               json={'prompt': 'How to use QuickBooks?'},
                               headers=auth_headers)
        assert response.status_code == 200
        assert response.json['message'] == "QuickBooks advice"

def test_airtable_execution_endpoint(client, auth_headers):
    with patch('google_ai.generate_airtable_record_data') as mock_gen, \
         patch('airtable_service.create_record') as mock_service:

        mock_gen.return_value = {'table_name': 'Tasks', 'fields': {'Name': 'Test Task'}}
        mock_service.return_value = {'status': 'success', 'record': {'id': 'rec123'}}

        response = client.post('/api/v1/database/airtable/assistance',
                               json={'prompt': 'Create a task', 'execute': True},
                               headers=auth_headers)
        assert response.status_code == 200
        assert "Successfully executed Airtable action" in response.json['message']
        assert response.json['record']['id'] == 'rec123'

def test_quickbooks_execution_endpoint(client, auth_headers):
    with patch('google_ai.generate_quickbooks_invoice_data') as mock_gen, \
         patch('quickbooks_service.create_customer') as mock_cust, \
         patch('quickbooks_service.create_invoice') as mock_inv:

        mock_gen.return_value = {'customer_name': 'John Doe', 'amount': 100, 'description': 'Consulting'}
        mock_cust.return_value = {'status': 'success', 'customer': {'Id': 'cust123'}}
        mock_inv.return_value = {'status': 'success', 'invoice': {'Id': 'inv123'}}

        response = client.post('/api/v1/finance/quickbooks/assistance',
                               json={'prompt': 'Invoice John Doe 100', 'execute': True},
                               headers=auth_headers)
        assert response.status_code == 200
        assert "Successfully executed QuickBooks action" in response.json['message']
        assert response.json['invoice']['Id'] == 'inv123'
