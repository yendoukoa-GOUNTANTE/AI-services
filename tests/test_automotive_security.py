import pytest
from unittest.mock import patch

def test_automotive_security_endpoint(client, auth_headers):
    with patch('google_ai.provide_automotive_security_assistance') as mock_ai:
        mock_ai.return_value = "Automotive security response"
        response = client.post('/api/v1/automotive/security',
                               json={'prompt': 'test automotive security prompt'},
                               headers=auth_headers)
        assert response.status_code == 200
        assert response.json['message'] == "Automotive security response"

def test_automotive_security_prompt_required(client, auth_headers):
    response = client.post('/api/v1/automotive/security',
                           json={},
                           headers=auth_headers)
    assert response.status_code == 400
