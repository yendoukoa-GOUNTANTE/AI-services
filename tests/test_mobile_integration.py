import unittest
import json
import sys
import uuid
from unittest.mock import patch, MagicMock

# Mock external dependencies that might be missing
mock_mods = [
    'google.genai', 'google.genai.types', 'firebase_admin', 'firebase_admin.messaging',
    'stripe', 'facebook_business', 'facebook_business.api',
    'facebook_business.adobjects', 'facebook_business.adobjects.adaccount',
    'facebook_business.exceptions', 'google.cloud', 'google.api_core', 'langchain',
    'langchain_google_vertexai', 'langchain_openai',
    'langchain_anthropic', 'langchain_nvidia_ai_endpoints',
    'langchain_mistralai', 'langflow', 'llama_index',
    'llama_index.llms.nvidia', 'llama_index.core', 'vertexai',
    'vertexai.generative_models', 'vertexai.preview', 'vertexai.preview.vision_models',
    'google.oauth2', 'google.oauth2.service_account',
    'azure.ai.inference', 'azure.core.credentials', 'xero_python'
]
for mod in mock_mods:
    if mod not in sys.modules:
        m = MagicMock()
        if '.' not in mod: # Only add __path__ for top-level packages
            m.__path__ = []
        sys.modules[mod] = m

# Mock before importing app
with patch('app.initialize_firebase_sdk', return_value=None):
    from app import app, db, User

class TestMobileIntegration(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            # Create a test user with a unique name/key each time
            uid = str(uuid.uuid4())[:8]
            self.test_user = User(username=f'user_{uid}', api_key=f'key_{uid}')
            db.session.add(self.test_user)
            db.session.commit()
            self.auth_headers = {'X-API-Key': f'key_{uid}'}

    @patch('google_ai.provide_android_dev_assistance')
    def test_android_endpoint(self, mock_assist):
        mock_assist.return_value = "Android Response"
        response = self.client.post('/api/v1/develop/android',
                               json={'prompt': 'How to create a Fragment?'},
                               headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Android Response', response.get_data(as_text=True))

    @patch('google_ai.provide_ios_dev_assistance')
    def test_ios_endpoint(self, mock_assist):
        mock_assist.return_value = "iOS Response"
        response = self.client.post('/api/v1/develop/ios',
                               json={'prompt': 'How to use SwiftUI?'},
                               headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('iOS Response', response.get_data(as_text=True))

    @patch('google_ai.provide_mobile_sdk_integration_assistance')
    def test_sdk_integration_endpoint(self, mock_assist):
        mock_assist.return_value = "SDK Response"
        response = self.client.post('/api/v1/mobile/sdk-integration',
                               json={'prompt': 'How to integrate Firebase?'},
                               headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('SDK Response', response.get_data(as_text=True))

    def test_push_endpoint_initialization_error(self):
        with patch('firebase_admin._apps', []):
            response = self.client.post('/api/v1/mobile/push',
                                   json={'token': 'test', 'title': 'test', 'body': 'test'},
                                   headers=self.auth_headers)
            self.assertEqual(response.status_code, 500)
            self.assertIn('Firebase SDK not initialized', response.get_data(as_text=True))

if __name__ == "__main__":
    unittest.main()
