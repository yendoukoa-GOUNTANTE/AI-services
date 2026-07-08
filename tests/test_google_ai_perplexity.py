import pytest
import google_ai
from unittest.mock import patch

@patch("google_ai._provide_gemini_assistance")
def test_provide_perplexity_assistance(mock_gemini):
    mock_gemini.return_value = "Gemini strategy for Perplexity"
    result = google_ai.provide_perplexity_assistance("search help")
    assert result == "Gemini strategy for Perplexity"
    mock_gemini.assert_called_once()

@patch("perplexity_service.get_completion")
def test_generate_perplexity_completion(mock_perplexity):
    mock_perplexity.return_value = {
        "choices": [{"message": {"content": "Direct Perplexity response"}}]
    }
    result = google_ai.generate_perplexity_completion("search query")
    assert result == "Direct Perplexity response"
    mock_perplexity.assert_called_once_with("search query", model="sonar-pro")
