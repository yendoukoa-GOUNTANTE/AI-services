import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Mock external modules before importing app
mock_google = MagicMock()
mock_google.__path__ = []
sys.modules['vertexai'] = MagicMock()
sys.modules['vertexai.generative_models'] = MagicMock()
sys.modules['vertexai.preview.vision_models'] = MagicMock()
sys.modules['google'] = mock_google
sys.modules['google.genai'] = MagicMock()
sys.modules['google.genai.types'] = MagicMock()
sys.modules['google.cloud'] = MagicMock()
sys.modules['google.cloud.aiplatform_v1beta1'] = MagicMock()
sys.modules['google.cloud.aiplatform_v1beta1.types'] = MagicMock()
sys.modules['facebook_business'] = MagicMock()
sys.modules['facebook_business.api'] = MagicMock()
sys.modules['facebook_business.adobjects.adaccount'] = MagicMock()
sys.modules['firebase_admin'] = MagicMock()
sys.modules['firebase_admin.credentials'] = MagicMock()
sys.modules['firebase_admin.messaging'] = MagicMock()
sys.modules['mailchimp_marketing'] = MagicMock()
sys.modules['elevenlabs'] = MagicMock()
sys.modules['cloudinary'] = MagicMock()
sys.modules['runwayml'] = MagicMock()
mock_twilio = MagicMock()
mock_twilio.__path__ = []
sys.modules['twilio'] = mock_twilio
sys.modules['twilio.rest'] = MagicMock()
sys.modules['httpx'] = MagicMock()
# Don't mock Flask extensions if possible, as they might be needed for the app to function correctly in tests
# or mock them very carefully.
sys.modules['facebook_business'] = MagicMock()
sys.modules['facebook_business.api'] = MagicMock()
sys.modules['facebook_business.adobjects.adaccount'] = MagicMock()
sys.modules['facebook_business.exceptions'] = MagicMock()
sys.modules['stripe'] = MagicMock()
sys.modules['langchain_google_vertexai'] = MagicMock()
sys.modules['langchain_openai'] = MagicMock()
sys.modules['langchain_anthropic'] = MagicMock()
sys.modules['langchain_nvidia_ai_endpoints'] = MagicMock()
sys.modules['langchain_mistralai'] = MagicMock()
sys.modules['llama_index'] = MagicMock()
sys.modules['llama_index.llms.nvidia'] = MagicMock()
sys.modules['llama_index.core'] = MagicMock()
sys.modules['azure.ai.inference'] = MagicMock()
sys.modules['azure.core.credentials'] = MagicMock()
sys.modules['firebase_admin'] = MagicMock()
sys.modules['firebase_admin.credentials'] = MagicMock()
sys.modules['firebase_admin.messaging'] = MagicMock()

import app

class TestNewAPIs(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.app.test_client()
        self.ctx = app.app.app_context()
        self.ctx.push()
        app.db.create_all()
        # Create a test user
        self.test_user = app.User(username="testuser", api_key="testkey")
        app.db.session.add(self.test_user)
        app.db.session.commit()
        self.headers = {"X-API-Key": "testkey"}

    def tearDown(self):
        app.db.session.remove()
        app.db.drop_all()
        self.ctx.pop()

    @patch('google_ai.provide_flutterwave_assistance')
    def test_flutterwave_assistance(self, mock_ai):
        mock_ai.return_value = "Flutterwave guidance"
        response = self.client.post('/api/v1/finance/flutterwave',
                                    json={"prompt": "How to use Flutterwave?"},
                                    headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Flutterwave guidance", response.get_json()['message'])

    @patch('flutterwave_service.initialize_transaction')
    def test_flutterwave_execution(self, mock_service):
        mock_service.return_value = {"status": "success", "data": {"link": "https://checkout.flutterwave.com/v3/hosted/pay/123"}}
        response = self.client.post('/api/v1/finance/flutterwave',
                                    json={"execute": True, "email": "test@example.com", "amount": 100},
                                    headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], "success")

    @patch('google_ai.provide_notion_assistance')
    def test_notion_assistance(self, mock_ai):
        mock_ai.return_value = "Notion guidance"
        response = self.client.post('/api/v1/productivity/notion',
                                    json={"prompt": "How to use Notion?"},
                                    headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Notion guidance", response.get_json()['message'])

    @patch('notion_service.create_page')
    def test_notion_execution(self, mock_service):
        mock_service.return_value = {"id": "page_123", "object": "page"}
        response = self.client.post('/api/v1/productivity/notion',
                                    json={"execute": True, "page_id": "parent_123", "title": "Test Page"},
                                    headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['id'], "page_123")

    @patch('google_ai.provide_quickbooks_assistance')
    def test_quickbooks_assistance(self, mock_ai):
        mock_ai.return_value = "QuickBooks guidance"
        response = self.client.post('/api/v1/business/quickbooks',
                                    json={"prompt": "How to use QuickBooks?"},
                                    headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("QuickBooks guidance", response.get_json()['message'])

    @patch('quickbooks_service.get_quickbooks_info')
    def test_quickbooks_execution(self, mock_service):
        mock_service.return_value = {"status": "Configured"}
        response = self.client.post('/api/v1/business/quickbooks',
                                    json={"execute": True},
                                    headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], "Configured")

    @patch('google_ai.provide_twilio_assistance')
    def test_twilio_assistance(self, mock_ai):
        mock_ai.return_value = "Twilio guidance"
        response = self.client.post('/api/v1/communication/twilio',
                                    json={"prompt": "How to use Twilio?"},
                                    headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Twilio guidance", response.get_json()['message'])

    @patch('twilio_service.send_sms')
    def test_twilio_execution(self, mock_service):
        mock_service.return_value = {"status": "success", "sid": "SM123"}
        response = self.client.post('/api/v1/communication/twilio',
                                    json={"execute": True, "to_number": "+1234567890", "prompt": "Hello"},
                                    headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], "success")

if __name__ == '__main__':
    unittest.main()
