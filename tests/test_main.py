import pytest
from fastapi.testclient import TestClient
from app.main import app
import io
import os

@pytest.fixture
def client():
    return TestClient(app)

def test_root_endpoint(client):
    """Test the root endpoint returns correct welcome message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Job Description Bias Detection API",
        "status": "running"
    }

def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "python-llm-bias-detector"
    }

def test_extract_no_file(client):
    """Test /extract endpoint with no file"""
    response = client.post("/extract")
    assert response.status_code == 422  # FastAPI validation error

def test_extract_empty_file(client):
    """Test /extract endpoint with empty file"""
    files = {
        'file': ('empty.txt', b'', 'text/plain')
    }
    response = client.post("/extract", files=files)
    assert response.status_code == 400
    assert "Empty file provided" in response.json()["detail"]

def test_extract_large_file(client):
    """Test /extract endpoint with file larger than 10MB"""
    # Create a file slightly larger than 10MB
    large_content = b'x' * (10 * 1024 * 1024 + 1)
    files = {
        'file': ('large.txt', large_content, 'text/plain')
    }
    response = client.post("/extract", files=files)
    assert response.status_code == 413
    assert "File too large" in response.json()["detail"]



def test_extract_invalid_file_type(client):
    """Test /extract endpoint with unsupported file type"""
    files = {
        'file': ('test.xyz', b'some content', 'application/octet-stream')
    }
    response = client.post("/extract", files=files)
    assert response.status_code == 400
    # assert "Unsupported file type" in response.json()["detail"].lower()

# Commented out as these might need mocking or real PDF/DOCX files
# def test_extract_pdf_file(client):
#     """Test /extract endpoint with PDF file"""
#     pass

# def test_extract_docx_file(client):
#     """Test /extract endpoint with DOCX file"""
#     pass

# def test_extract_image_file(client):
#     """Test /extract endpoint with image file"""
#     pass
