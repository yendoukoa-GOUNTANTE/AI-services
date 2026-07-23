import pytest
import json
from unittest.mock import patch

def test_marketing_assistance_no_api_key(client):
    response = client.post('/api/v1/marketing/assistance',
                           data=json.dumps({'prompt': 'test prompt'}),
                           content_type='application/json')
    assert response.status_code == 401

@patch('google_ai.provide_marketing_bot_assistance')
def test_marketing_assistance_with_api_key(mock_gen, client, auth_headers):
    mock_gen.return_value = "Mock response for: How to do e-mail marketing?"
    response = client.post('/api/v1/marketing/assistance',
                           headers=auth_headers,
                           data=json.dumps({'prompt': 'How to do e-mail marketing?'}),
                           content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['message'] == "Mock response for: How to do e-mail marketing?"

@patch('google_ai.provide_marketing_bot_assistance')
def test_marketing_assistance_gtm_with_api_key(mock_gen, client, auth_headers):
    mock_gen.return_value = "Mock GTM response: Google Tag Manager container verified."
    response = client.post('/api/v1/marketing/assistance',
                           headers=auth_headers,
                           data=json.dumps({'prompt': 'Set up a GTM container for tracking purchases'}),
                           content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['message'] == "Mock GTM response: Google Tag Manager container verified."
    mock_gen.assert_called_once_with('Set up a GTM container for tracking purchases')

@patch('google_ai.provide_marketing_bot_assistance')
def test_marketing_assistance_campaigns_with_api_key(mock_gen, client, auth_headers):
    mock_gen.return_value = "Mock Campaign response: Campaigns Tool ROI optimized."
    response = client.post('/api/v1/marketing/assistance',
                           headers=auth_headers,
                           data=json.dumps({'prompt': 'Optimize my ad campaign budgets across Meta and Google'}),
                           content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['message'] == "Mock Campaign response: Campaigns Tool ROI optimized."
    mock_gen.assert_called_once_with('Optimize my ad campaign budgets across Meta and Google')

@patch('google_ai.get_model')
def test_google_ai_provide_marketing_bot_assistance_logic(mock_get_model):
    from google_ai import provide_marketing_bot_assistance
    from unittest.mock import MagicMock

    # Mock the LangChain chain invoke process
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = "AI response including GTM and campaigns"

    # We mock the get_model and prompt_template chain creation by mocking invoke
    # In google_ai.py: chain = prompt_template | model | StrOutputParser()
    # A simple mock is to patch the ChatVertexAI or the invoke on the chain.
    # Actually, we can patch StrOutputParser or the prompt template chain invoke.
    with patch('google_ai.ChatPromptTemplate.from_messages') as mock_from_messages:
        mock_prompt_template = MagicMock()
        mock_from_messages.return_value = mock_prompt_template
        # mock prompt_template | model | parser
        # In Python, the | operator calls __or__
        mock_prompt_template.__or__.return_value = mock_prompt_template
        mock_prompt_template.invoke.return_value = "Mocked chain output"

        res = provide_marketing_bot_assistance("My campaign tag query")
        assert res == "Mocked chain output"

        # Verify from_messages was called with expected prompt templates
        args, _ = mock_from_messages.call_args
        messages = args[0]
        system_msg_type, system_msg_content = messages[0]
        user_msg_type, user_msg_content = messages[1]

        assert system_msg_type == "system"
        assert "Google Tag Manager (GTM)" in system_msg_content
        assert "Campaigns Tool" in system_msg_content
        assert "Google Veo 3.1" in system_msg_content

        assert user_msg_type == "user"
        assert "GTM configurations" in user_msg_content
        assert "campaign tools" in user_msg_content

def test_marketing_twin_no_api_key(client):
    response = client.post('/api/v1/marketing/twin',
                           data=json.dumps({'prompt': 'test twin prompt'}),
                           content_type='application/json')
    assert response.status_code == 401

@patch('google_ai.provide_marketing_twin_assistance')
def test_marketing_twin_with_api_key(mock_gen, client, auth_headers):
    mock_gen.return_value = "Mock digital twin response: Simulated Buyer Persona active."
    response = client.post('/api/v1/marketing/twin',
                           headers=auth_headers,
                           data=json.dumps({'prompt': 'Simulate target audience for organic coffee'}),
                           content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['message'] == "Mock digital twin response: Simulated Buyer Persona active."
