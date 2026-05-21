import pytest
from unittest.mock import patch

def test_gumloop_assistance(client):
    """Test Gumloop assistance endpoint."""
    with patch('google_ai.provide_gumloop_assistance') as mock_gumloop:
        mock_gumloop.return_value = "Gumloop automation advice"

        # We need an API key to access the endpoint
        # First register a user
        register_resp = client.post('/api/v1/register_public', json={'username': 'gumloop_tester'})
        api_key = register_resp.get_json()['api_key']

        response = client.post('/api/v1/gumloop/assistance',
                               json={'prompt': 'How to automate a login?'},
                               headers={'X-API-Key': api_key})

        assert response.status_code == 200
        assert response.get_json()['message'] == "Gumloop automation advice"
        mock_gumloop.assert_called_once_with('How to automate a login?')

def test_gumloop_execution(client):
    """Test Gumloop execution endpoint."""
    with patch('google_ai.run_gumloop_workflow') as mock_run:
        mock_run.return_value = {"run_id": "123"}

        register_resp = client.post('/api/v1/register_public', json={'username': 'gumloop_exec'})
        api_key = register_resp.get_json()['api_key']

        response = client.post('/api/v1/gumloop/assistance',
                               json={'execute': True, 'pipeline_id': 'pipe_1', 'inputs': {'a': 1}},
                               headers={'X-API-Key': api_key})

        assert response.status_code == 200
        assert "123" in response.get_json()['message']
        mock_run.assert_called_once_with('pipe_1', {'a': 1})

def test_n8n_assistance(client):
    """Test n8n assistance endpoint."""
    with patch('google_ai.provide_n8n_assistance') as mock_n8n:
        mock_n8n.return_value = "n8n workflow advice"

        register_resp = client.post('/api/v1/register_public', json={'username': 'n8n_tester'})
        api_key = register_resp.get_json()['api_key']

        response = client.post('/api/v1/n8n/assistance',
                               json={'prompt': 'How to connect to Discord?'},
                               headers={'X-API-Key': api_key})

        assert response.status_code == 200
        assert response.get_json()['message'] == "n8n workflow advice"
        mock_n8n.assert_called_once_with('How to connect to Discord?')

def test_n8n_execution(client):
    """Test n8n execution endpoint."""
    with patch('google_ai.trigger_n8n_webhook') as mock_trigger:
        mock_trigger.return_value = {"status": "ok"}

        register_resp = client.post('/api/v1/register_public', json={'username': 'n8n_exec'})
        api_key = register_resp.get_json()['api_key']

        response = client.post('/api/v1/n8n/assistance',
                               json={'execute': True, 'webhook_url': 'http://hook', 'payload': {'data': 'test'}},
                               headers={'X-API-Key': api_key})

        assert response.status_code == 200
        assert "ok" in response.get_json()['message']
        mock_trigger.assert_called_once_with('http://hook', {'data': 'test'})

def test_lamatic_assistance(client):
    """Test Lamatic.ai assistance endpoint."""
    with patch('google_ai.provide_lamatic_assistance') as mock_lamatic:
        mock_lamatic.return_value = "Lamatic.ai platform advice"

        register_resp = client.post('/api/v1/register_public', json={'username': 'lamatic_tester'})
        api_key = register_resp.get_json()['api_key']

        response = client.post('/api/v1/lamatic/assistance',
                               json={'prompt': 'How to build a RAG app?'},
                               headers={'X-API-Key': api_key})

        assert response.status_code == 200
        assert response.get_json()['message'] == "Lamatic.ai platform advice"
        mock_lamatic.assert_called_once_with('How to build a RAG app?')

def test_lamatic_execution(client):
    """Test Lamatic.ai execution endpoint."""
    with patch('google_ai.execute_lamatic_workflow') as mock_exec:
        mock_exec.return_value = {"response": "AI output"}

        register_resp = client.post('/api/v1/register_public', json={'username': 'lamatic_exec'})
        api_key = register_resp.get_json()['api_key']

        response = client.post('/api/v1/lamatic/assistance',
                               json={'execute': True, 'workflow_id': 'wf_1', 'prompt': 'test prompt'},
                               headers={'X-API-Key': api_key})

        assert response.status_code == 200
        assert "AI output" in response.get_json()['message']
        mock_exec.assert_called_once_with('wf_1', 'test prompt')
