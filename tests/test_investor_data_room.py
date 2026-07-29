import json
from unittest.mock import patch


@patch('google_ai.provide_investor_data_room_assistance')
def test_founder_data_room_strategy_assistance(mock_gen, client, auth_headers):
    mock_gen.return_value = 'Mock investor data room response'
    response = client.post(
        '/api/v1/founder/data-room/assistance',
        data=json.dumps({'prompt': 'test strategy', 'execute': False}),
        content_type='application/json',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Mock investor data room response'


@patch('google_ai.generate_investor_checklist_data')
def test_founder_data_room_compile_assistance(mock_gen, client, auth_headers):
    mock_gen.return_value = {
        "title": "Mock Investor Due Diligence Checklist",
        "categories": [
            {
                "name": "1. Corporate Governance",
                "items": ["Bylaws", "Minutes"]
            }
        ]
    }
    response = client.post(
        '/api/v1/founder/data-room/assistance',
        data=json.dumps({'prompt': 'test compile', 'execute': True}),
        content_type='application/json',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'file_id' in data
    assert 'filename' in data
    assert 'compiled' in data['message'] or 'saved' in data['message']
