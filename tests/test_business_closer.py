import pytest
import json
from unittest.mock import patch

@patch('google_ai.provide_business_closer_assistance')
def test_business_closer_success(mock_gen, client, auth_headers):
    mock_gen.return_value = 'Mock business closer response'
    response = client.post('/api/v1/business/closer',
                           data=json.dumps({'prompt': 'How do I close a $50k SaaS contract?'}),
                           content_type='application/json',
                           headers=auth_headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['message'] == 'Mock business closer response'
    mock_gen.assert_called_once_with('How do I close a $50k SaaS contract?')

def test_business_closer_missing_prompt(client, auth_headers):
    response = client.post('/api/v1/business/closer',
                           data=json.dumps({}),
                           content_type='application/json',
                           headers=auth_headers)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_business_closer_unauthorized(client):
    response = client.post('/api/v1/business/closer',
                           data=json.dumps({'prompt': 'How do I close a $50k SaaS contract?'}),
                           content_type='application/json')
    assert response.status_code == 401
