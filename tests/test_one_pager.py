import pytest

def test_download_one_pager_endpoint(client):
    """Test that GET /api/v1/download/one-pager returns a PDF successfully."""
    response = client.get('/api/v1/download/one-pager')
    assert response.status_code == 200
    assert response.headers.get('Content-Type') == 'application/pdf'
    # Check that it returns actual PDF binary content
    assert response.data.startswith(b'%PDF')

def test_download_one_pager_redirect_endpoint(client):
    """Test that GET /download-one-pager returns a PDF successfully."""
    response = client.get('/download-one-pager')
    assert response.status_code == 200
    assert response.headers.get('Content-Type') == 'application/pdf'
    assert response.data.startswith(b'%PDF')
