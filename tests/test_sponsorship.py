import pytest
from unittest.mock import patch, MagicMock

def test_open_collective_assistance(client, auth_headers):
    with patch('google_ai.provide_open_collective_assistance') as mock_ai:
        mock_ai.return_value = "Open Collective advice"
        response = client.post('/api/v1/sponsorship/open-collective', json={'prompt': 'test prompt'}, headers=auth_headers)
        assert response.status_code == 200
        assert response.json['message'] == "Open Collective advice"

def test_patreon_assistance(client, auth_headers):
    with patch('google_ai.provide_patreon_assistance') as mock_ai:
        mock_ai.return_value = "Patreon advice"
        response = client.post('/api/v1/sponsorship/patreon', json={'prompt': 'test prompt'}, headers=auth_headers)
        assert response.status_code == 200
        assert response.json['message'] == "Patreon advice"
