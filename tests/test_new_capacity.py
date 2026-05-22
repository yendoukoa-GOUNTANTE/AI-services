import unittest
from unittest.mock import patch, MagicMock
from app import app, db, User
import json

class TestNewCapacity(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            self.test_user = User(username='testuser', api_key='testkey')
            db.session.add(self.test_user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    @patch('google_ai.provide_fine_tuning_assistance')
    def test_fine_tuner_endpoint(self, mock_fine_tune):
        mock_fine_tune.return_value = "Mocked fine tuning response"
        response = self.client.post('/api/v1/fine-tuner/assistance',
                                    data=json.dumps({'prompt': 'How to fine tune?'}),
                                    content_type='application/json',
                                    headers={'X-API-Key': 'testkey'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], "Mocked fine tuning response")

    @patch('google_ai.provide_router_capacity_assistance')
    def test_router_endpoint(self, mock_router):
        mock_router.return_value = "Mocked router response"
        response = self.client.post('/api/v1/router/assistance',
                                    data=json.dumps({'prompt': 'How to route?'}),
                                    content_type='application/json',
                                    headers={'X-API-Key': 'testkey'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], "Mocked router response")

if __name__ == '__main__':
    unittest.main()
