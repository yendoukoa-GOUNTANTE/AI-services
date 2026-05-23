import pytest
import json
from unittest.mock import patch, AsyncMock

@patch('google_ai.provide_mistral_intelligence')
def test_mistral_intelligence(mock_gen, client, auth_headers):
    mock_gen.return_value = 'Mock Mistral response'
    response = client.post('/api/v1/mistral/intelligence',
                           data=json.dumps({'prompt': 'Hello Mistral'}),
                           headers=auth_headers,
                           content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['message'] == 'Mock Mistral response'

@patch('google_ai.provide_copilot_coding_assistance', new_callable=AsyncMock)
def test_copilot_coding(mock_gen, client, auth_headers):
    mock_gen.return_value = 'Mock Copilot response'
    response = client.post('/api/v1/copilot/coding',
                           data=json.dumps({'prompt': 'Write a Python script'}),
                           headers=auth_headers,
                           content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['message'] == 'Mock Copilot response'
