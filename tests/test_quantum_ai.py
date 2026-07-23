import pytest
from unittest.mock import patch
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create a mock user
            user = User(username="test_quantum_user", api_key="quantum_test_key", credits=1000)
            db.session.add(user)
            db.session.commit()
            yield client
            db.session.remove()
            db.drop_all()

@patch('google_ai.provide_quantum_ai_assistance')
def test_quantum_assistance_endpoint_no_api_key(mock_quantum, client):
    response = client.post('/api/v1/quantum/assistance', json={"prompt": "How to design a QML model?"})
    assert response.status_code == 401
    assert "API key is missing" in response.get_json()["error"]

@patch('google_ai.provide_quantum_ai_assistance')
def test_quantum_assistance_endpoint_with_api_key(mock_quantum, client):
    mock_quantum.return_value = "Mocked Quantum AI response: Quantum Neural Network configured successfully."
    response = client.post(
        '/api/v1/quantum/assistance',
        headers={"X-API-Key": "quantum_test_key"},
        json={"prompt": "How to design a QML model?"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "Mocked Quantum AI response" in data["message"]
    mock_quantum.assert_called_once_with("How to design a QML model?")

@patch('google_ai.provide_quantum_ai_assistance')
def test_quantum_assistance_endpoint_missing_prompt(mock_quantum, client):
    response = client.post(
        '/api/v1/quantum/assistance',
        headers={"X-API-Key": "quantum_test_key"},
        json={}
    )
    assert response.status_code == 400
    assert "Prompt is required" in response.get_json()["error"]
