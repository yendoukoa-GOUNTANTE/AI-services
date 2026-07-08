import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Create a more robust mock for vertexai to handle submodules
vertexai_mock = MagicMock()
sys.modules['vertexai'] = vertexai_mock
sys.modules['vertexai.generative_models'] = MagicMock()
sys.modules['vertexai.preview'] = MagicMock()
sys.modules['vertexai.preview.vision_models'] = MagicMock()

sys.modules['google'] = MagicMock()
sys.modules['google.genai'] = MagicMock()
sys.modules['google.genai.types'] = MagicMock()

sys.modules['langchain_google_vertexai'] = MagicMock()
sys.modules['langchain_openai'] = MagicMock()
sys.modules['langchain_anthropic'] = MagicMock()
sys.modules['langchain_nvidia_ai_endpoints'] = MagicMock()
sys.modules['langchain_core'] = MagicMock()
sys.modules['langchain_core.prompts'] = MagicMock()
sys.modules['langchain_core.output_parsers'] = MagicMock()

sys.modules['llama_index'] = MagicMock()
sys.modules['llama_index.llms'] = MagicMock()
sys.modules['llama_index.llms.nvidia'] = MagicMock()
sys.modules['llama_index.core'] = MagicMock()

sys.modules['emergent_service'] = MagicMock()

# Add current directory to path
sys.path.append(os.getcwd())

import google_ai

class TestGoogleAIPerplexity(unittest.TestCase):

    @patch('google_ai._provide_gemini_assistance')
    def test_provide_perplexity_assistance(self, mock_gemini):
        mock_gemini.return_value = "Gemini strategy for Perplexity"
        result = google_ai.provide_perplexity_assistance("search query")
        self.assertEqual(result, "Gemini strategy for Perplexity")
        mock_gemini.assert_called_once()

    @patch('perplexity_service.get_completion')
    def test_generate_perplexity_completion(self, mock_perplexity):
        mock_perplexity.return_value = {
            "choices": [{"message": {"content": "Perplexity result"}}]
        }
        result = google_ai.generate_perplexity_completion("search query")
        self.assertEqual(result, "Perplexity result")
        mock_perplexity.assert_called_once_with("search query", model="sonar-pro")

    @patch('perplexity_service.get_completion')
    def test_generate_perplexity_completion_error(self, mock_perplexity):
        mock_perplexity.return_value = {"error": "API Error"}
        result = google_ai.generate_perplexity_completion("search query")
        self.assertEqual(result, "Perplexity Execution Error: API Error")

if __name__ == '__main__':
    unittest.main()
