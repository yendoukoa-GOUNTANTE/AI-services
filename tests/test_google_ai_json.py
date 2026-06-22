import unittest
import sys
from unittest.mock import MagicMock

# Mock langchain and other dependencies
sys.modules['langchain'] = MagicMock()
sys.modules['langchain.schema'] = MagicMock()
sys.modules['langchain_google_vertexai'] = MagicMock()
sys.modules['langchain_openai'] = MagicMock()
sys.modules['langchain_anthropic'] = MagicMock()
sys.modules['langchain_nvidia_ai_endpoints'] = MagicMock()
sys.modules['langchain_mistralai'] = MagicMock()

import google_ai

class GoogleAITestCase(unittest.TestCase):

    def test_json_extraction_plain(self):
        content = '{"key": "value"}'
        result = google_ai.extract_json(content)
        self.assertEqual(result, {"key": "value"})

    def test_json_extraction_markdown(self):
        content = 'Here is your JSON:\n```json\n{"key": "value"}\n```\nHope it helps!'
        result = google_ai.extract_json(content)
        self.assertEqual(result, {"key": "value"})

    def test_json_extraction_no_fences(self):
        content = 'Sure! {"key": "value"} is what you asked for.'
        result = google_ai.extract_json(content)
        self.assertEqual(result, {"key": "value"})

    def test_json_extraction_nested(self):
        content = 'Nested: {"a": {"b": 1}}'
        result = google_ai.extract_json(content)
        self.assertEqual(result, {"a": {"b": 1}})

    def test_json_extraction_invalid(self):
        content = 'This is not json { [ }'
        result = google_ai.extract_json(content)
        self.assertIsNone(result)

    def test_json_extraction_incomplete(self):
        content = '{"key": "value"'
        result = google_ai.extract_json(content)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
