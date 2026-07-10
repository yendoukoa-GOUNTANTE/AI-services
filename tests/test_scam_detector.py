import pytest
from unittest.mock import patch, MagicMock
from app import app, db

def test_scam_detector_endpoint(client, auth_headers):
    # Mock Google AI assistance using patch decorator/context manager
    with patch('google_ai.provide_scam_detection_assistance') as mock_provide:
        mock_provide.return_value = "This is a 419 scam."

        # Call the scam detector endpoint
        response = client.post('/api/v1/security/scam-detector',
                               json={'prompt': 'I am a prince and I need money.'},
                               headers=auth_headers)

        assert response.status_code == 200
        assert "This is a 419 scam." in response.get_json()['message']
        mock_provide.assert_called_once_with('I am a prince and I need money.')
