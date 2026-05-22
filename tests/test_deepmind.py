import unittest
from unittest.mock import patch, MagicMock
import sys
import json

# Mocking all external dependencies to ensure the test can run in this environment
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

from app import app, db, User

class DeepMindIntegrationTestCase(unittest.TestCase):
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

    @patch('google_ai.generate_deepmind_image')
    def test_deepmind_image_endpoint(self, mock_gen_image):
        mock_gen_image.return_value = "fake_base64_data"
        response = self.app.post('/api/v1/deepmind/image',
                                 data=json.dumps({'prompt': 'a beautiful sunset'}),
                                 content_type='application/json',
                                 headers={'X-API-Key': self.api_key})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['image_data'], 'fake_base64_data')

    @patch('google_ai.generate_deepmind_video_content')
    def test_deepmind_video_endpoint(self, mock_gen_video):
        mock_gen_video.return_value = "DeepMind Video Script Content"
        response = self.app.post('/api/v1/deepmind/video',
                                 data=json.dumps({'prompt': 'a sci-fi movie about AI'}),
                                 content_type='application/json',
                                 headers={'X-API-Key': self.api_key})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'DeepMind Video Script Content')

if __name__ == '__main__':
    unittest.main()
