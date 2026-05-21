import pytest
from unittest.mock import patch

def test_zapier_assistance(client):
    """Test Zapier assistance endpoint."""
    with patch('google_ai.provide_zapier_assistance') as mock_zapier:
        mock_zapier.return_value = "Zapier automation advice for France"

        register_resp = client.post('/api/v1/register_public', json={'username': 'zapier_tester'})
        api_key = register_resp.get_json()['api_key']

        response = client.post('/api/v1/zapier/assistance',
                               json={'prompt': 'Comment automatiser mon CRM?'},
                               headers={'X-API-Key': api_key})

        assert response.status_code == 200
        assert response.get_json()['message'] == "Zapier automation advice for France"
        mock_zapier.assert_called_once_with('Comment automatiser mon CRM?')

def test_odoo_assistance(client):
    """Test Odoo assistance endpoint."""
    with patch('google_ai.provide_odoo_assistance') as mock_odoo:
        mock_odoo.return_value = "Odoo implementation advice for Francophone Africa"

        register_resp = client.post('/api/v1/register_public', json={'username': 'odoo_tester'})
        api_key = register_resp.get_json()['api_key']

        response = client.post('/api/v1/odoo/assistance',
                               json={'prompt': 'Comment configurer la comptabilité OHADA?'},
                               headers={'X-API-Key': api_key})

        assert response.status_code == 200
        assert response.get_json()['message'] == "Odoo implementation advice for Francophone Africa"
        mock_odoo.assert_called_once_with('Comment configurer la comptabilité OHADA?')

def test_sage_assistance(client):
    """Test Sage assistance endpoint."""
    with patch('google_ai.provide_sage_assistance') as mock_sage:
        mock_sage.return_value = "Sage payroll advice for France"

        register_resp = client.post('/api/v1/register_public', json={'username': 'sage_tester'})
        api_key = register_resp.get_json()['api_key']

        response = client.post('/api/v1/sage/assistance',
                               json={'prompt': 'Comment générer la DSN?'},
                               headers={'X-API-Key': api_key})

        assert response.status_code == 200
        assert response.get_json()['message'] == "Sage payroll advice for France"
        mock_sage.assert_called_once_with('Comment générer la DSN?')
