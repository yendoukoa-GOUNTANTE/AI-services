import pytest
from unittest.mock import patch

@patch('google_ai.provide_ussd_blockchain_assistance')
def test_ussd_blockchain_assistance_endpoint(mock_ai, client, auth_headers):
    mock_ai.return_value = "Mock USSD Blockchain response"
    response = client.post('/api/v1/ussd-blockchain/assistance',
                           json={'prompt': 'How to build a USSD crypto wallet?'},
                           headers=auth_headers)
    assert response.status_code == 200
    assert response.json['message'] == "Mock USSD Blockchain response"

@patch('google_ai.provide_ussd_menu_design_assistance')
def test_ussd_design_endpoint(mock_ai, client, auth_headers):
    mock_ai.return_value = "Mock USSD Design response"
    response = client.post('/api/v1/ussd/design',
                           json={'prompt': 'Design a menu for a taxi service.'},
                           headers=auth_headers)
    assert response.status_code == 200
    assert response.json['message'] == "Mock USSD Design response"

@patch('google_ai.provide_ussd_monetization_assistance')
def test_ussd_monetization_endpoint(mock_ai, client, auth_headers):
    mock_ai.return_value = "Mock USSD Monetization response"
    response = client.post('/api/v1/ussd/monetization',
                           json={'prompt': 'How to monetize a USSD weather service?'},
                           headers=auth_headers)
    assert response.status_code == 200
    assert response.json['message'] == "Mock USSD Monetization response"
