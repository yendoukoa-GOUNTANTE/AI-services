import pytest
import json
from unittest.mock import patch

@patch('google_ai.provide_video_production_assistance')
def test_video_production_assistance(mock_gen, client, auth_headers):
    mock_gen.return_value = 'Mock video production response'
    response = client.post('/api/v1/video/assistance',
                           data=json.dumps({'prompt': 'test video production'}),
                           content_type='application/json',
                           headers=auth_headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Mock video production response'

@patch('google_ai.provide_podcast_assistance')
def test_podcast_assistance(mock_gen, client, auth_headers):
    mock_gen.return_value = 'Mock podcast response'
    response = client.post('/api/v1/podcast/assistance',
                           data=json.dumps({'prompt': 'test podcast'}),
                           content_type='application/json',
                           headers=auth_headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Mock podcast response'
