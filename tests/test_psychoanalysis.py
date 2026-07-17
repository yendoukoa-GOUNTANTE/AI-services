import pytest
from unittest.mock import patch, MagicMock, ANY
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Seed a test user
            user = User(username='test_psycho_user', api_key='test_psycho_key')
            db.session.add(user)
            db.session.commit()
            yield client
            db.session.remove()
            db.drop_all()

@patch('google_ai._provide_gemini_assistance')
def test_psychoanalysis_endpoint_success(mock_gemini, client):
    # Mock the response from Google AI
    mock_gemini.return_value = "As a Psychoanalyst, your dream suggests unconscious desires for achievement. Here is my psychological advice..."

    response = client.post(
        '/api/v1/psychoanalysis/assistance',
        headers={'X-API-Key': 'test_psycho_key'},
        json={'prompt': 'I dreamt I was flying high over a mountain.'}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert "dream suggests unconscious desires" in data['message']
    mock_gemini.assert_called_once_with(
        'I dreamt I was flying high over a mountain.',
        ANY,
        'Psychoanalysis AI Error'
    )

def test_psychoanalysis_endpoint_missing_prompt(client):
    response = client.post(
        '/api/v1/psychoanalysis/assistance',
        headers={'X-API-Key': 'test_psycho_key'},
        json={}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data['error'] == "Prompt is required"

def test_psychoanalysis_endpoint_unauthorized(client):
    response = client.post(
        '/api/v1/psychoanalysis/assistance',
        headers={'X-API-Key': 'wrong_key'},
        json={'prompt': 'I am stressed.'}
    )

    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
