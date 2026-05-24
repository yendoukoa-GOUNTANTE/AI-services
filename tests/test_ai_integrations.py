import unittest
from unittest.mock import patch, MagicMock
import sys
import json
import os

# Mocking all external dependencies
sys.modules['langchain_google_vertexai'] = MagicMock()
sys.modules['langchain_openai'] = MagicMock()
sys.modules['langchain_anthropic'] = MagicMock()
sys.modules['langchain_nvidia_ai_endpoints'] = MagicMock()
sys.modules['langchain_core'] = MagicMock()
sys.modules['langchain_core.prompts'] = MagicMock()
sys.modules['langchain_core.output_parsers'] = MagicMock()
sys.modules['llama_index'] = MagicMock()
sys.modules['llama_index.llms.nvidia'] = MagicMock()
sys.modules['llama_index.core'] = MagicMock()
sys.modules['langflow'] = MagicMock()
sys.modules['facebook_business'] = MagicMock()
sys.modules['facebook_business.api'] = MagicMock()
sys.modules['facebook_business.adobjects.adaccount'] = MagicMock()
sys.modules['facebook_business.exceptions'] = MagicMock()

# Set dummy environment variables for testing
os.environ["STRIPE_SECRET_KEY"] = "test_stripe_key"
os.environ["GOOGLE_CLOUD_PROJECT"] = "test-project"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

from app import app, db, User

class AIIntegrationsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        with app.app_context():
            db.create_all()
            self.test_user = User(username='testuser', api_key='testkey')
            db.session.add(self.test_user)
            db.session.commit()
            self.api_key = 'testkey'

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    @patch('google_ai.provide_antigravity_agent_assistance')
    def test_antigravity_agent_endpoint(self, mock_assistance):
        mock_assistance.return_value = "Antigravity insight"
        response = self.app.post('/api/v1/antigravity/agent',
                                 data=json.dumps({'prompt': 'test prompt'}),
                                 content_type='application/json',
                                 headers={'X-API-Key': self.api_key})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Antigravity insight')

    @patch('google_ai.provide_gemini_spark_assistance')
    def test_gemini_spark_endpoint(self, mock_assistance):
        mock_assistance.return_value = "Spark insight"
        response = self.app.post('/api/v1/gemini/spark',
                                 data=json.dumps({'prompt': 'test prompt'}),
                                 content_type='application/json',
                                 headers={'X-API-Key': self.api_key})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Spark insight')

if __name__ == '__main__':
    unittest.main()
