import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Mock dependencies before importing app
sys.modules['elevenlabs'] = MagicMock()
sys.modules['elevenlabs.client'] = MagicMock()
sys.modules['cloudinary'] = MagicMock()
sys.modules['cloudinary.uploader'] = MagicMock()
sys.modules['cloudinary.utils'] = MagicMock()
sys.modules['runwayml'] = MagicMock()
sys.modules['google.genai'] = MagicMock()
sys.modules['google.genai.types'] = MagicMock()
sys.modules['azure.ai.inference'] = MagicMock()
sys.modules['azure.core.credentials'] = MagicMock()
sys.modules['firebase_admin'] = MagicMock()
sys.modules['firebase_admin.credentials'] = MagicMock()
sys.modules['firebase_admin.messaging'] = MagicMock()
sys.modules['mailchimp_marketing'] = MagicMock()
sys.modules['mailchimp_marketing.api_client'] = MagicMock()

from app import app, db, User

class TestNewIntegrations(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            self.test_user = User(username='testuser', api_key='testkey')
            db.session.add(self.test_user)
            db.session.commit()
            self.api_key = 'testkey'

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    @patch('google_ai._provide_gemini_assistance')
    def test_elevenlabs_endpoint(self, mock_gemini):
        mock_gemini.return_value = "ElevenLabs assistance response"
        response = self.client.post('/api/v1/voice/elevenlabs',
                                    json={'prompt': 'test prompt'},
                                    headers={'X-API-Key': self.api_key})
        self.assertEqual(response.status_code, 200)
        self.assertIn("ElevenLabs assistance response", response.get_json()['message'])

    @patch('elevenlabs_service.text_to_speech')
    def test_elevenlabs_execution(self, mock_tts):
        mock_tts.return_value = {
            "status": "success",
            "message": "Audio generated successfully",
            "filename": "test.mp3",
            "filepath": "uploads/test.mp3"
        }
        response = self.client.post('/api/v1/voice/elevenlabs',
                                  json={'prompt': 'Hello world', 'execute': True},
                                  headers={'X-API-Key': self.api_key})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('file_id', data)

    @patch('google_ai._provide_gemini_assistance')
    def test_tiktok_endpoint(self, mock_gemini):
        mock_gemini.return_value = "TikTok assistance response"
        response = self.client.post('/api/v1/market/tiktok',
                                    json={'prompt': 'test prompt'},
                                    headers={'X-API-Key': self.api_key})
        self.assertEqual(response.status_code, 200)
        self.assertIn("TikTok assistance response", response.get_json()['message'])

    @patch('google_ai._provide_gemini_assistance')
    def test_whatsapp_endpoint(self, mock_gemini):
        mock_gemini.return_value = "WhatsApp assistance response"
        response = self.client.post('/api/v1/mobile/whatsapp',
                                    json={'prompt': 'test prompt'},
                                    headers={'X-API-Key': self.api_key})
        self.assertEqual(response.status_code, 200)
        self.assertIn("WhatsApp assistance response", response.get_json()['message'])

    @patch('google_ai._provide_gemini_assistance')
    def test_cloudinary_endpoint(self, mock_gemini):
        mock_gemini.return_value = "Cloudinary assistance response"
        response = self.client.post('/api/v1/media/cloudinary',
                                    json={'prompt': 'test prompt'},
                                    headers={'X-API-Key': self.api_key})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Cloudinary assistance response", response.get_json()['message'])

    @patch('google_ai._provide_gemini_assistance')
    def test_runway_endpoint(self, mock_gemini):
        mock_gemini.return_value = "Runway assistance response"
        response = self.client.post('/api/v1/video/runway',
                                    json={'prompt': 'test prompt'},
                                    headers={'X-API-Key': self.api_key})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Runway assistance response", response.get_json()['message'])

    @patch('elevenlabs_service.get_voices')
    def test_elevenlabs_voices(self, mock_voices):
        mock_voices.return_value = {"status": "success", "voices": [{"id": "1", "name": "Test"}]}
        response = self.client.get('/api/v1/voice/elevenlabs/voices',
                                   headers={'X-API-Key': self.api_key})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()['voices']), 1)

    @patch('tiktok_service.get_tiktok_user_info')
    def test_tiktok_me(self, mock_me):
        mock_me.return_value = {"status": "success", "username": "testuser"}
        response = self.client.get('/api/v1/market/tiktok/me',
                                   headers={'X-API-Key': self.api_key})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['username'], 'testuser')

    @patch('whatsapp_service.send_whatsapp_template')
    def test_whatsapp_template_execution(self, mock_template):
        mock_template.return_value = {"status": "success", "message_id": "123"}
        response = self.client.post('/api/v1/mobile/whatsapp',
                                    json={'template_name': 'test_template', 'to_number': '123456', 'execute': True},
                                    headers={'X-API-Key': self.api_key})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message_id'], '123')

    @patch('runway_service.get_task_status')
    def test_runway_status(self, mock_status):
        mock_status.return_value = {"status": "success", "task_status": "COMPLETED"}
        response = self.client.get('/api/v1/video/runway/status/task123',
                                   headers={'X-API-Key': self.api_key})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['task_status'], 'COMPLETED')

if __name__ == '__main__':
    unittest.main()
