
import pytest
from unittest.mock import patch, MagicMock
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client

def test_scam_detector_endpoint(client):
    # Mock Google AI assistance using patch decorator/context manager
    with patch('google_ai.provide_scam_detection_assistance') as mock_provide:
        mock_provide.return_value = "This is a 419 scam."

        # Register a user
        resp = client.post('/api/v1/register', json={'username': 'testuser'})
        json_data = resp.get_json()
        assert json_data is not None
        api_key = json_data['api_key']

        # Call the scam detector endpoint
        response = client.post('/api/v1/security/scam-detector',
                               json={'prompt': 'I am a prince and I need money.'},
                               headers={'X-API-Key': api_key})

        assert response.status_code == 200
        assert "This is a 419 scam." in response.get_json()['message']
        mock_provide.assert_called_once_with('I am a prince and I need money.')
