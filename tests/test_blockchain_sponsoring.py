import pytest
from unittest.mock import patch, MagicMock

def test_blockchain_sponsoring_endpoint(client, auth_headers):
    with patch('google_ai.provide_blockchain_sponsoring_assistance') as mock_ai:
        mock_ai.return_value = "Blockchain sponsoring advice"
        response = client.post('/api/v1/blockchain/sponsoring', json={'prompt': 'How to get sponsored in USDC?'}, headers=auth_headers)
        assert response.status_code == 200
        assert response.json['message'] == "Blockchain sponsoring advice"
