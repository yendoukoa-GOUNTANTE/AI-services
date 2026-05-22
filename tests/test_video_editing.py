import pytest
from unittest.mock import patch

def test_video_editing_assistance(client, auth_headers):
    with patch('google_ai.provide_video_editing_assistance') as mock_assist:
        mock_assist.return_value = "Test video editing advice"

        response = client.post('/api/v1/video-editing/assistance',
                               json={'prompt': 'How to edit a vlog?'},
                               headers=auth_headers)

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == "Test video editing advice"
        mock_assist.assert_called_once_with('How to edit a vlog?')

def test_video_editing_assistance_no_prompt(client, auth_headers):
    response = client.post('/api/v1/video-editing/assistance',
                           json={},
                           headers=auth_headers)
    assert response.status_code == 400
    assert 'Prompt is required' in response.json['error']
