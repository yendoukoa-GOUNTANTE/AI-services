import pytest
from app import app, db, User, TrainingData
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        # Create a test user
        user = User(username='testuser', api_key='testkey')
        db.session.add(user)
        # Add sample training data
        td = TrainingData(prompt='test prompt', completion='test completion', category='Test')
        db.session.add(td)
        db.session.commit()
    yield app.test_client()
    with app.app_context():
        db.drop_all()

def test_get_dataset(client):
    response = client.get('/api/v1/research/dataset')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) > 0
    assert data[0]['prompt'] == 'test prompt'

def test_dataset_architect_endpoint(client, mocker):
    # Mock google_ai.provide_dataset_architect_assistance
    mocker.patch('google_ai.provide_dataset_architect_assistance', return_value="Mocked Architect Response")

    response = client.post('/api/v1/research/dataset-architect',
                           json={'prompt': 'Help me with data'},
                           headers={'X-API-Key': 'testkey'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == "Mocked Architect Response"

def test_training_strategist_endpoint(client, mocker):
    # Mock google_ai.provide_ai_training_strategist_assistance
    mocker.patch('google_ai.provide_ai_training_strategist_assistance', return_value="Mocked Strategist Response")

    response = client.post('/api/v1/research/training-strategist',
                           json={'prompt': 'Training plan'},
                           headers={'X-API-Key': 'testkey'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == "Mocked Strategist Response"
