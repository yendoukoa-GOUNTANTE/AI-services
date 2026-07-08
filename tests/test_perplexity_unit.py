import pytest
import perplexity_service
from unittest.mock import patch, MagicMock

def test_get_completion_no_api_key(monkeypatch):
    monkeypatch.delenv("PERPLEXITY_API_KEY", raising=False)
    result = perplexity_service.get_completion("test prompt")
    assert "error" in result
    assert "PERPLEXITY_API_KEY not configured" in result["error"]

@patch("requests.post")
def test_get_completion_success(mock_post, monkeypatch):
    monkeypatch.setenv("PERPLEXITY_API_KEY", "test_key")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Perplexity response"}}]
    }
    mock_post.return_value = mock_response

    result = perplexity_service.get_completion("test prompt")
    assert "choices" in result
    assert result["choices"][0]["message"]["content"] == "Perplexity response"
    mock_post.assert_called_once()
