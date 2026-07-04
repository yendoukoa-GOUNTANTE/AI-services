import pytest
from unittest.mock import patch, MagicMock

@patch('devrev_service.get_self')
def test_devrev_assistance(mock_get_self, client, auth_headers):
    mock_get_self.return_value = {"status": "success", "user": {"display_name": "Test User"}}

    with patch('google_ai._provide_gemini_assistance') as mock_gemini:
        mock_gemini.return_value = "DevRev guidance content"

        response = client.post('/api/v1/support/devrev',
                               json={"prompt": "How to use DevRev?"},
                               headers=auth_headers)

        assert response.status_code == 200
        assert response.json['status'] == "success"
        assert "DevRev guidance content" in response.json['message']

@patch('devrev_service.create_work')
def test_devrev_execution(mock_create_work, client, auth_headers):
    mock_create_work.return_value = {"status": "success", "work": {"id": "work-123"}}

    with patch('google_ai.generate_devrev_work_data') as mock_data_gen:
        mock_data_gen.return_value = {
            "title": "Bug in login",
            "body": "Users cannot login with keys",
            "type": "issue"
        }

        response = client.post('/api/v1/support/devrev',
                               json={"prompt": "Create an issue for login bug", "execute": True},
                               headers=auth_headers)

        assert response.status_code == 200
        assert response.json['status'] == "success"
        assert "Issue 'Bug in login' created" in response.json['message']
        assert response.json['work']['id'] == "work-123"
