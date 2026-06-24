import pytest
from unittest.mock import patch

def test_notion_assistance_endpoint(client, auth_headers):
    with patch('google_ai.provide_notion_assistance') as mock_ai:
        mock_ai.return_value = "Notion Mocked response"
        response = client.post('/api/v1/notion/assistance',
                               json={'prompt': 'test notion prompt'},
                               headers=auth_headers)
        assert response.status_code == 200
        assert response.json['message'] == "Notion Mocked response"

def test_notion_execute_endpoint(client, auth_headers):
    with patch('google_ai.provide_notion_assistance') as mock_ai:
        # Mocking the AI response for execution
        mock_ai.return_value = "Notion Execution Mocked response"

        # Mocking the structured data generation
        with patch('google_ai.generate_notion_page_data') as mock_data:
            mock_data.return_value = {'title': 'AI Page', 'content_blocks': []}

            # We also need to mock the notion service to avoid real API calls
            with patch('notion_service.create_page') as mock_create:
                mock_create.return_value = {'status': 'success', 'page': {'id': 'mock-page-id'}}

                response = client.post('/api/v1/notion/assistance',
                                       json={'prompt': 'create a page', 'execute': True, 'parent_page_id': 'test-parent'},
                                       headers=auth_headers)

                assert response.status_code == 200
                assert "Successfully executed Notion action" in response.json['message']
                mock_create.assert_called_once()
