import pytest
from app import app, db, User

@pytest.fixture(autouse=True)
def setup_db():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_user():
    with app.app_context():
        user = User(username='testuser', api_key='testkey')
        db.session.add(user)
        db.session.commit()
        return user

def test_zendesk_assistance_no_api_key(client):
    response = client.post('/api/v1/support/zendesk', json={'prompt': 'test'})
    assert response.status_code == 401

def test_zendesk_assistance_with_api_key(client, test_user, mocker):
    mocker.patch('google_ai.provide_zendesk_assistance', return_value='Zendesk AI response')
    response = client.post('/api/v1/support/zendesk',
                           json={'prompt': 'How to create a ticket?'},
                           headers={'X-API-Key': 'testkey'})
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Zendesk AI response'

def test_zendesk_execution_success(client, test_user, mocker):
    mocker.patch('google_ai.generate_zendesk_ticket_data', return_value={
        'subject': 'Test Subject',
        'comment_body': 'Test Body'
    })
    mocker.patch('zendesk_service.create_ticket', return_value={
        'status': 'success',
        'ticket': {'id': 123, 'subject': 'Test Subject'}
    })

    response = client.post('/api/v1/support/zendesk',
                           json={'prompt': 'Create a ticket about login issues', 'execute': True},
                           headers={'X-API-Key': 'testkey'})

    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'Ticket \'Test Subject\' created' in data['message']
    assert data['ticket']['id'] == 123
