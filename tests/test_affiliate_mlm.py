import pytest
import json
from unittest.mock import patch
import google_ai

@patch('google_ai.provide_affiliate_mlm_assistance')
def test_affiliate_mlm_assistance_success(mock_gen, client, auth_headers):
    mock_gen.return_value = 'Mock affiliate and MLM strategic advice response'
    response = client.post('/api/v1/marketing/affiliate-mlm',
                           data=json.dumps({'prompt': 'How to design a binary compensation plan?'}),
                           content_type='application/json',
                           headers=auth_headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['message'] == 'Mock affiliate and MLM strategic advice response'
    mock_gen.assert_called_once_with('How to design a binary compensation plan?')

def test_affiliate_mlm_assistance_missing_prompt(client, auth_headers):
    response = client.post('/api/v1/marketing/affiliate-mlm',
                           data=json.dumps({}),
                           content_type='application/json',
                           headers=auth_headers)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_affiliate_mlm_assistance_unauthorized(client):
    response = client.post('/api/v1/marketing/affiliate-mlm',
                           data=json.dumps({'prompt': 'How to design a binary compensation plan?'}),
                           content_type='application/json')
    assert response.status_code == 401

@patch('google_ai._provide_gemini_assistance')
def test_provide_affiliate_mlm_assistance_helper(mock_assistance):
    mock_assistance.return_value = "Helper response"
    res = google_ai.provide_affiliate_mlm_assistance("Test prompt")
    assert res == "Helper response"
    mock_assistance.assert_called_once()
    args, kwargs = mock_assistance.call_args
    assert args[0] == "Test prompt"
    assert "Affiliate" in args[1]
    assert "MLM" in args[1]
    assert args[2] == "Affiliate MLM AI Error"
