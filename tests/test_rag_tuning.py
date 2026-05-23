import unittest
from unittest.mock import patch, MagicMock
from app import app, db, User, File
import json

class RAGTuningTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            self.test_user = User(username='testuser', api_key='testkey')
            db.session.add(self.test_user)
            db.session.commit()

            self.test_file = File(
                user_id=self.test_user.id,
                filename='test_context.txt',
                file_type='document',
                content='This is a document about specialized fine-tuning for medical data.'
            )
            db.session.add(self.test_file)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    @patch('google_ai.provide_rag_tuning_assistance')
    def test_rag_tuning_assistance_endpoint(self, mock_assistance):
        mock_assistance.return_value = "Mocked RAG & Fine-Tuning Advice"

        response = self.client.post('/api/v1/rag-tuning/assistance',
                                   headers={'X-API-Key': 'testkey'},
                                   json={'prompt': 'How should I fine-tune my model?'},
                                   content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], "Mocked RAG & Fine-Tuning Advice")
        mock_assistance.assert_called_once()

if __name__ == '__main__':
    unittest.main()
