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

@patch('google_ai.provide_podcast_assistance')
def test_podcast_video_script_generation(mock_gen, client, auth_headers):
    mock_gen.return_value = 'Mock podcast video script with AV cues'
    response = client.post('/api/v1/podcast/assistance',
                           data=json.dumps({'prompt': 'Create a podcast video script with dual camera cues about machine learning'}),
                           content_type='application/json',
                           headers=auth_headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Mock podcast video script with AV cues'
    mock_gen.assert_called_with('Create a podcast video script with dual camera cues about machine learning')

@patch('google_ai.provide_podcast_assistance')
def test_other_scripts_improvement(mock_gen, client, auth_headers):
    mock_gen.return_value = 'Mock optimized YouTube script with an engaging hook'
    response = client.post('/api/v1/podcast/assistance',
                           data=json.dumps({'prompt': 'Improve this YouTube script to have a better hook: Hello guys welcome back today we talk about AI'}),
                           content_type='application/json',
                           headers=auth_headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Mock optimized YouTube script with an engaging hook'
    mock_gen.assert_called_with('Improve this YouTube script to have a better hook: Hello guys welcome back today we talk about AI')
