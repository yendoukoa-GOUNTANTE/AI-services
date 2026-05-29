import pytest
from unittest.mock import patch

def test_xero_assistance_endpoint(client, auth_headers):
    with patch('google_ai.provide_xero_assistance') as mock_ai:
        mock_ai.return_value = "Xero Mocked response"
        response = client.post('/api/v1/xero/assistance',
                               json={'prompt': 'test xero prompt'},
                               headers=auth_headers)
        assert response.status_code == 200
        assert response.json['message'] == "Xero Mocked response"
