import pytest
from unittest.mock import patch, ANY

@patch('google_ai._provide_gemini_assistance')
def test_offshore_endpoint_success(mock_gemini, client):
    # Mock the response from Google AI
    mock_gemini.return_value = "As an Offshore Company Specialist, the best jurisdiction for an e-commerce company is Singapore or Cayman Islands due to friendly tax laws..."

    response = client.post(
        '/api/v1/business/offshore',
        headers={'X-API-Key': 'testkey'},
        json={'prompt': 'What is the best jurisdiction for a new e-commerce business?'}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert "best jurisdiction for an e-commerce company" in data['message']
    mock_gemini.assert_called_once_with(
        'What is the best jurisdiction for a new e-commerce business?',
        ANY,
        'Offshore Business AI Error'
    )

def test_offshore_endpoint_missing_prompt(client):
    response = client.post(
        '/api/v1/business/offshore',
        headers={'X-API-Key': 'testkey'},
        json={}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data['error'] == "Prompt is required"

def test_offshore_endpoint_unauthorized(client):
    response = client.post(
        '/api/v1/business/offshore',
        headers={'X-API-Key': 'wrong_key'},
        json={'prompt': 'Tell me about BVI LLC.'}
    )

    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
