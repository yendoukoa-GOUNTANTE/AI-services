import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Mock dependencies
sys.modules['flask'] = MagicMock()
sys.modules['flask_sqlalchemy'] = MagicMock()
sys.modules['flask_babel'] = MagicMock()

# Add current directory to path
sys.path.append(os.getcwd())

import perplexity_service

class TestPerplexityService(unittest.TestCase):

    @patch('requests.post')
    def test_get_completion_success(self, mock_post):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello from Perplexity"}}]
        }
        mock_post.return_value = mock_response

        # Mock env var
        with patch.dict(os.environ, {"PERPLEXITY_API_KEY": "test-key"}):
            # Call the actual service
            result = perplexity_service.get_completion("Test prompt", model="sonar-pro")

        # Assertions
        self.assertEqual(result['choices'][0]['message']['content'], "Hello from Perplexity")
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "https://api.perplexity.ai/chat/completions")
        # In requests, headers are passed as a keyword argument 'headers'
        # Check if the dictionary contains the expected key-value pairs
        self.assertEqual(kwargs['json']['model'], "sonar-pro")

    @patch('requests.post')
    def test_get_completion_error(self, mock_post):
        # Setup mock response for error
        mock_post.side_effect = Exception("API Error")

        with patch.dict(os.environ, {"PERPLEXITY_API_KEY": "test-key"}):
            # Call the actual service
            result = perplexity_service.get_completion("Test prompt")

        self.assertIn('error', result)
        self.assertEqual(result['error'], "API Error")

    def test_get_completion_no_key(self):
        with patch.dict(os.environ, {}, clear=True):
            # Manually ensure it's gone
            if "PERPLEXITY_API_KEY" in os.environ:
                del os.environ["PERPLEXITY_API_KEY"]
            result = perplexity_service.get_completion("Test prompt")
            self.assertEqual(result['error'], "PERPLEXITY_API_KEY not configured")

if __name__ == '__main__':
    unittest.main()
