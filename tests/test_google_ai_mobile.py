import unittest
from unittest.mock import patch, MagicMock
import sys

# Mock google.genai BEFORE importing google_ai
sys.modules['google.genai'] = MagicMock()

import google_ai

class TestGoogleAIIntegration(unittest.TestCase):

    @patch('google_ai._provide_gemini_assistance')
    def test_android_dev_assistance(self, mock_generate):
        mock_generate.return_value = "Android Assist"
        result = google_ai.provide_android_dev_assistance("test prompt")
        self.assertEqual(result, "Android Assist")
        mock_generate.assert_called_once()
        args, _ = mock_generate.call_args
        self.assertIn("Android", args[1]) # Check if persona is passed

    @patch('google_ai._provide_gemini_assistance')
    def test_ios_dev_assistance(self, mock_generate):
        mock_generate.return_value = "iOS Assist"
        result = google_ai.provide_ios_dev_assistance("test prompt")
        self.assertEqual(result, "iOS Assist")
        mock_generate.assert_called_once()
        args, _ = mock_generate.call_args
        self.assertIn("iOS", args[1])

    @patch('google_ai._provide_gemini_assistance')
    def test_mobile_sdk_integration_assistance(self, mock_generate):
        mock_generate.return_value = "SDK Assist"
        result = google_ai.provide_mobile_sdk_integration_assistance("test prompt")
        self.assertEqual(result, "SDK Assist")
        mock_generate.assert_called_once()
        args, _ = mock_generate.call_args
        self.assertIn("SDK", args[1])

if __name__ == "__main__":
    unittest.main()
