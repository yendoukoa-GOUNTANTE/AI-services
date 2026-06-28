import pytest
from unittest.mock import patch, MagicMock

def test_nuclear_assistance_endpoint(client):
    """Test the nuclear assistance endpoint."""
    # Mocking the AI service call
    with patch('google_ai._provide_gemini_assistance') as mock_ai:
        mock_ai.return_value = "Nuclear energy is a powerful source of clean energy."

        # We need a user with an API key to test the protected endpoint
        # The conftest.py usually provides a way to handle this or we can mock require_api_key
        with patch('app.User.query') as mock_query:
            mock_user = MagicMock()
            mock_user.api_key = 'test_key'
            mock_user.id = 1
            mock_query.filter_by.return_value.first.return_value = mock_user

            response = client.post('/api/v1/nuclear/assistance',
                                   json={'prompt': 'Tell me about SMRs'},
                                   headers={'X-API-Key': 'test_key'})

            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'success'
            assert "Nuclear energy" in data['message']

            mock_ai.assert_called_once()
            args, _ = mock_ai.call_args
            assert "SMRs" in args[0]
            assert "Nuclear Energy Strategist" in args[1]

def test_nuclear_assistance_no_prompt(client):
    """Test the nuclear assistance endpoint without a prompt."""
    with patch('app.User.query') as mock_query:
        mock_user = MagicMock()
        mock_user.api_key = 'test_key'
        mock_query.filter_by.return_value.first.return_value = mock_user

        response = client.post('/api/v1/nuclear/assistance',
                               json={},
                               headers={'X-API-Key': 'test_key'})

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
