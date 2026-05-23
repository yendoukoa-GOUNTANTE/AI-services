import pytest
import os
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
import google_ai

@pytest.mark.asyncio
async def test_provide_copilot_coding_assistance():
    # Patch the class in the module where it's used
    with patch('google_ai.ChatCompletionsClient') as mock_client_class:
        # Mocking the GITHUB_TOKEN
        with patch.dict(os.environ, {"GITHUB_TOKEN": "mock-token"}):
            # Setup mock client and its async context manager
            mock_client = AsyncMock()
            mock_client_class.return_value.__aenter__.return_value = mock_client

            # Mock response
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Mocked Code Response"
            mock_client.complete.return_value = mock_response

            result = await google_ai.provide_copilot_coding_assistance("test prompt")

            assert result == "Mocked Code Response"
            mock_client.complete.assert_called_once()

def test_provide_mistral_intelligence():
    with patch('google_ai.ChatMistralAI') as mock_mistral_class:
        mock_mistral = MagicMock()
        # Mock the result of the entire chain
        with patch('google_ai.ChatPromptTemplate.from_messages') as mock_prompt:
            mock_chain = MagicMock()
            mock_chain.invoke.return_value = "Mocked Mistral Response"
            mock_prompt.return_value.__or__.return_value.__or__.return_value = mock_chain

            result = google_ai.provide_mistral_intelligence("test prompt")
            assert result == "Mocked Mistral Response"
