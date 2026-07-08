import pytest
from unittest.mock import patch, MagicMock
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        # Create a test user
        user = User(username='testuser', api_key='test_key')
        db.session.add(user)
        db.session.commit()
        yield app.test_client()
        db.drop_all()

def test_perplexity_assistance_guidance(client):
    """Test the guidance/strategy mode of Perplexity assistance."""
    with patch('google_ai._provide_gemini_assistance') as mock_gemini:
        mock_gemini.return_value = "Guidance on using Perplexity AI."

        response = client.post('/api/v1/perplexity/assistance',
                               json={'prompt': 'How to use Perplexity?'},
                               headers={'X-API-Key': 'test_key'})

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert "Guidance" in data['message']
        mock_gemini.assert_called_once()

def test_perplexity_assistance_execution(client):
    """Test the direct execution mode of Perplexity assistance."""
    with patch('perplexity_service.get_completion') as mock_perplexity:
        mock_perplexity.return_value = {
            'choices': [{'message': {'content': 'Real-time search results from Perplexity.'}}]
        }

        response = client.post('/api/v1/perplexity/assistance',
                               json={'prompt': 'What is the current price of Bitcoin?', 'execute': True},
                               headers={'X-API-Key': 'test_key'})

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert "Real-time" in data['message']
        mock_perplexity.assert_called_once()

def test_perplexity_assistance_no_api_key(client):
    """Test that API key is required."""
    response = client.post('/api/v1/perplexity/assistance',
                           json={'prompt': 'Test prompt'})
    assert response.status_code == 401
