import pytest
from unittest.mock import patch

def test_cyber_os_hardening_endpoint(client, auth_headers):
    with patch('google_ai.provide_cyber_os_hardening_assistance') as mock_ai:
        mock_ai.return_value = "OS hardening response"
        response = client.post('/api/v1/security/os-hardening',
                               json={'prompt': 'test hardening prompt'},
                               headers=auth_headers)
        assert response.status_code == 200
        assert response.json['message'] == "OS hardening response"
