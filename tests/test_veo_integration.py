import pytest
from unittest.mock import patch, MagicMock
from app import app, db, User
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create a test user
            user = User(username='testuser', api_key='testkey')
            db.session.add(user)
            db.session.commit()
        yield client

def test_marketing_video_endpoint(client):
    """Test the Google Veo video generation endpoint."""
    with patch('google_ai.genai.Client') as mock_client:
        mock_genai_instance = mock_client.return_value
        mock_operation = MagicMock()
        mock_operation.name = "test-operation-id"
        mock_genai_instance.models.generate_videos.return_value = mock_operation

        response = client.post('/api/v1/marketing/video',
                               data=json.dumps({'prompt': 'A high-end cinematic coffee commercial.'}),
                               content_type='application/json',
                               headers={'X-API-Key': 'testkey'})

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert "Google Veo 3.1" in data['message']
        assert "test-operation-id" in data['message']

        mock_genai_instance.models.generate_videos.assert_called_once_with(
            model="veo-3.1-generate-preview",
            prompt='A high-end cinematic coffee commercial.'
        )
