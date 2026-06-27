import pytest
import json

def test_gaming_monetization_endpoint(client, mocker):
    # Mock the AI service call
    mock_ai = mocker.patch('google_ai.provide_gaming_monetization_assistance')
    mock_ai.return_value = "Mocked AI Response for Gaming & Monetization"

    response = client.post('/api/v1/gaming/monetization',
                           data=json.dumps({'prompt': 'How to monetize my Unity game?'}),
                           content_type='application/json',
                           headers={'X-API-Key': 'testkey'})

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['message'] == "Mocked AI Response for Gaming & Monetization"
    mock_ai.assert_called_once_with('How to monetize my Unity game?')

def test_gaming_monetization_endpoint_no_prompt(client):
    response = client.post('/api/v1/gaming/monetization',
                           data=json.dumps({}),
                           content_type='application/json',
                           headers={'X-API-Key': 'testkey'})

    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
