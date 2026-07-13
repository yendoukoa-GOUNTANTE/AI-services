import pytest
from unittest.mock import patch

def test_cloud_infrastructure_assistance_endpoint_no_api_key(client):
    response = client.post('/api/v1/cloud-infrastructure/assistance', json={'prompt': 'How to create a secure IP?'})
    assert response.status_code == 401

@patch('google_ai.provide_cloud_infrastructure_assistance')
def test_cloud_infrastructure_assistance_endpoint_with_api_key(mock_gen, client, auth_headers):
    # Mocking the AI service call
    mock_gen.return_value = 'Mocked AI response'

    response = client.post('/api/v1/cloud-infrastructure/assistance',
                           json={'prompt': 'How to create a secure IP?'},
                           headers=auth_headers)

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['message'] == 'Mocked AI response'

def test_cloud_infrastructure_assistance_endpoint_missing_prompt(client, auth_headers):
    response = client.post('/api/v1/cloud-infrastructure/assistance',
                           json={},
                           headers=auth_headers)

    assert response.status_code == 400
    assert 'error' in response.json

@patch('google_ai.provide_cloud_infrastructure_assistance')
def test_cloud_infrastructure_with_aws_prompts(mock_gen, client, auth_headers):
    mock_gen.return_value = "Mock AWS SaaS Monetization Architect Response"
    response = client.post('/api/v1/cloud-infrastructure/assistance',
                           json={'prompt': 'Design an AWS architecture for SaaS hosting with automatic Stripe monetization.'},
                           headers=auth_headers)
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert "Mock AWS" in response.json['message']
