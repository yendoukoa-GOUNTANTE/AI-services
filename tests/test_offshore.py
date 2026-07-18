import pytest
import json
from unittest.mock import patch

@patch('google_ai.provide_offshore_assistance')
def test_offshore_assistance_success(mock_gen, client, auth_headers):
    mock_gen.return_value = 'Mock offshore assistance response'
    response = client.post('/api/v1/offshore/assistance',
                           data=json.dumps({'prompt': 'How do I start a company in the Seychelles?'}),
                           content_type='application/json',
                           headers=auth_headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['message'] == 'Mock offshore assistance response'
    mock_gen.assert_called_once_with('How do I start a company in the Seychelles?')

def test_offshore_assistance_missing_prompt(client, auth_headers):
    response = client.post('/api/v1/offshore/assistance',
                           data=json.dumps({}),
                           content_type='application/json',
                           headers=auth_headers)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_offshore_assistance_unauthorized(client):
    response = client.post('/api/v1/offshore/assistance',
                           data=json.dumps({'prompt': 'How do I start a company in the Seychelles?'}),
                           content_type='application/json')
    assert response.status_code == 401
