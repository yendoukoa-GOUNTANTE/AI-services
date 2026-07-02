import pytest
from unittest.mock import patch, MagicMock

def test_emergent_assistance_endpoint(client, auth_headers):
    with patch('google_ai.provide_emergent_assistance') as mock_assist:
        mock_assist.return_value = "Emergent advice"

        # Test strategy call
        response = client.post('/api/v1/emergent/assistance',
                               json={'prompt': 'test prompt'},
                               headers=auth_headers)

        assert response.status_code == 200
        assert response.json['message'] == "Emergent advice"
        mock_assist.assert_called_once_with('test prompt')

def test_emergent_execution_endpoint(client, auth_headers):
    with patch('google_ai.generate_emergent_completion') as mock_exec:
        mock_exec.return_value = "Emergent result"

        # Test execution call
        response = client.post('/api/v1/emergent/assistance',
                               json={'prompt': 'test prompt', 'execute': True, 'model_name': 'gpt-4o'},
                               headers=auth_headers)

        assert response.status_code == 200
        assert response.json['message'] == "Emergent result"
        mock_exec.assert_called_once_with('test prompt', 'gpt-4o')

def test_emergent_service_get_completion():
    from emergent_service import get_completion
    import os

    with patch('requests.post') as mock_post:
        os.environ["EMERGENT_API_KEY"] = "fake_key"
        mock_response = MagicMock()
        mock_response.json.return_value = {"choices": [{"message": {"content": "Hello"}}]}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = get_completion("Hi")
        assert result["choices"][0]["message"]["content"] == "Hello"
        mock_post.assert_called_once()

        # Test missing API key
        del os.environ["EMERGENT_API_KEY"]
        result = get_completion("Hi")
        assert "error" in result
        assert "EMERGENT_API_KEY not configured" in result["error"]
