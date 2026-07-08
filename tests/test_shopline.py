import pytest
from unittest.mock import patch, MagicMock
import os
from shopline_service import create_product

@patch.dict(os.environ, {"SHOPLINE_STORE_HANDLE": "test-store"})
@patch('shopline_service.requests.post')
def test_create_product_success(mock_post):
    # Mock response
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"product": {"id": 123, "title": "Test Product"}}
    mock_post.return_value = mock_response

    # Call function
    result = create_product("Test Product", price="19.99")

    # Assertions
    assert "product" in result
    assert result["product"]["title"] == "Test Product"
    mock_post.assert_called_once()

@patch.dict(os.environ, {"SHOPLINE_STORE_HANDLE": "test-store"})
@patch('shopline_service.requests.post')
def test_create_product_failure(mock_post):
    # Mock failure
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_post.return_value = mock_response

    result = create_product("Fail Product")

    assert "error" in result
    assert "Bad Request" in result["error"]
