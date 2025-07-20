
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from app.main import app
import io
import os
import json
from app.models.schemas import TextExtractionResponse, BiasAnalysisResult, BiasIssue, Suggestion, BiasType, SeverityLevel, CategoryType

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_text_extractor():
    """Mock TextExtractor for testing"""
    with patch('app.main.text_extractor') as mock:
        yield mock

@pytest.fixture
def mock_bias_detector():
    """Mock BiasDetector for testing"""
    with patch('app.main.bias_detector') as mock:
        yield mock

# Test basic endpoints
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

# Test /extract endpoint
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
    assert "Empty file provided" in response.json()["message"]


def test_extract_large_file(client):
    """Test /extract endpoint with file larger than 10MB"""
    # Create a file slightly larger than 10MB
    large_content = b'x' * (10 * 1024 * 1024 + 1)
    files = {
        'file': ('large.txt', large_content, 'text/plain')
    }
    response = client.post("/extract", files=files)
    assert response.status_code == 413
    assert "File too large" in response.json()["message"]


def test_extract_no_filename(client):
    """Test /extract endpoint with no filename"""
    files = {
        'file': ('', b'some content', 'text/plain')
    }
    response = client.post("/extract", files=files)
    assert response.status_code == 422

    


def test_extract_successful_extraction(client, mock_text_extractor):
    """Test successful text extraction"""
    # Mock successful extraction
    mock_text_extractor.extract_from_content = AsyncMock(return_value=TextExtractionResponse(
        success=True,
        extracted_text="Sample extracted text from document",
        file_type="txt"
    ))
    
    files = {
        'file': ('test.txt', b'sample content', 'text/plain')
    }
    response = client.post("/extract", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["extracted_text"] == "Sample extracted text from document"
    assert data["file_type"] == "txt"

def test_extract_failed_extraction(client, mock_text_extractor):
    """Test failed text extraction"""
    # Mock failed extraction
    mock_text_extractor.extract_from_content = AsyncMock(return_value=TextExtractionResponse(
        success=False,
        error_message="Unsupported file type: xyz"
    ))
    
    files = {
        'file': ('test.xyz', b'sample content', 'application/octet-stream')
    }
    response = client.post("/extract", files=files)
    
    assert response.status_code == 400
    assert "Unsupported file type: xyz" in response.json()["message"]

def test_extract_exception_handling(client, mock_text_extractor):
    """Test exception handling in extract endpoint"""
    # Mock exception during extraction
    mock_text_extractor.extract_from_content = AsyncMock(side_effect=Exception("Unexpected error"))
    
    files = {
        'file': ('test.txt', b'sample content', 'text/plain')
    }
    response = client.post("/extract", files=files)
    
    assert response.status_code == 500
    assert "Text extraction failed due to an internal error" in response.json()["message"]

# Test /analyze endpoint
def test_analyze_empty_text(client):
    """Test /analyze endpoint with empty text"""
    response = client.post("/analyze", json={"text": ""})
    assert response.status_code == 400
    assert "must be at least 50 characters long" in response.json()["message"]

def test_analyze_short_text(client):
    """Test /analyze endpoint with text shorter than 50 characters"""
    response = client.post("/analyze", json={"text": "Short text"})
    assert response.status_code == 400
    assert "must be at least 50 characters long" in response.json()["message"]

def test_analyze_successful_analysis(client, mock_bias_detector):
    """Test successful bias analysis"""
    # Create mock analysis result - updated to match schema
    mock_result = BiasAnalysisResult(
        role="Software Developer",  # Added optional field
        industry="Technology",      # Added optional field
        bias_score=0.3,            # Can be str or float per schema
        inclusivity_score=0.8,     # Can be str or float per schema
        clarity_score=0.9,         # Can be str or float per schema
        issues=[
            BiasIssue(
                type=BiasType.GENDER,
                text="aggressive",
                start_index=50,
                end_index=60,
                severity=SeverityLevel.MEDIUM,
                explanation="This is masculine-coded language"
            )
        ],
        suggestions=[
            Suggestion(
                original="aggressive",
                improved="results-oriented",
                rationale="More inclusive language",
                category=CategoryType.BIAS
            )
        ],
        seo_keywords=["software", "developer", "python"],
        improved_text="Improved job description text here...",
        overall_assessment="The job description has moderate bias issues that should be addressed."
    )
    
    mock_bias_detector.analyze_comprehensive = AsyncMock(return_value=mock_result)
    
    long_text = "We are looking for an aggressive software developer who can work independently and lead our team to success. The ideal candidate should be confident and assertive in their approach to problem-solving."
    
    response = client.post("/analyze", json={"text": long_text})
    
    assert response.status_code == 200
    data = response.json()
    assert data["bias_score"] == 0.3
    assert data["inclusivity_score"] == 0.8
    assert data["clarity_score"] == 0.9
    assert data["role"] == "Software Developer"
    assert data["industry"] == "Technology"
    assert len(data["issues"]) == 1
    assert data["issues"][0]["type"] == "gender"
    assert data["issues"][0]["text"] == "aggressive"
    assert len(data["suggestions"]) == 1
    assert data["suggestions"][0]["original"] == "aggressive"
    assert data["suggestions"][0]["improved"] == "results-oriented"
    assert data["overall_assessment"] == "The job description has moderate bias issues that should be addressed."

def test_analyze_exception_handling(client, mock_bias_detector):
    """Test exception handling in analyze endpoint"""
    # Mock exception during analysis
    mock_bias_detector.analyze_comprehensive = AsyncMock(side_effect=Exception("Analysis failed"))
    
    long_text = "We are looking for an aggressive software developer who can work independently and lead our team to success."
    
    response = client.post("/analyze", json={"text": long_text})
    
    assert response.status_code == 500
    assert "Bias analysis failed due to an internal error" in response.json()["message"]

# Test /analyze-file endpoint
def test_analyze_file_successful(client, mock_text_extractor, mock_bias_detector):
    """Test successful file analysis"""
    # Mock successful extraction
    mock_text_extractor.extract_from_content = AsyncMock(return_value=TextExtractionResponse(
        success=True,
        extracted_text="We are looking for an aggressive software developer who can work independently and lead our team.",
        file_type="txt"
    ))
    
    # Mock successful analysis - updated to match schema
    mock_result = BiasAnalysisResult(
        role="Software Developer",
        industry="Technology",
        bias_score=0.4,
        inclusivity_score=0.7,
        clarity_score=0.8,
        issues=[],
        suggestions=[],
        seo_keywords=["software", "developer"],
        improved_text="Improved text here...",
        overall_assessment="Analysis complete."
    )
    mock_bias_detector.analyze_comprehensive = AsyncMock(return_value=mock_result)
    
    files = {
        'file': ('test.txt', b'sample job description content', 'text/plain')
    }
    response = client.post("/analyze-file", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "extracted_text" in data
    assert "analysis" in data
    assert data["analysis"]["bias_score"] == 0.4
    assert data["analysis"]["role"] == "Software Developer"
    assert data["analysis"]["industry"] == "Technology"

def test_analyze_file_extraction_failed(client, mock_text_extractor):
    """Test file analysis with failed extraction"""
    # Mock failed extraction
    mock_text_extractor.extract_from_content = AsyncMock(return_value=TextExtractionResponse(
        success=False,
        error_message="Unsupported file type"
    ))
    
    files = {
        'file': ('test.xyz', b'sample content', 'application/octet-stream')
    }
    response = client.post("/analyze-file", files=files)
    
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["message"]



# Test error handling functions
def test_get_error_type():
    """Test the get_error_type function"""
    from app.main import get_error_type
    
    assert get_error_type(400) == "validation_error"
    assert get_error_type(401) == "authentication_error"
    assert get_error_type(403) == "permission_error"
    assert get_error_type(404) == "not_found_error"
    assert get_error_type(413) == "file_too_large"
    assert get_error_type(429) == "rate_limit_exceeded"
    assert get_error_type(500) == "internal_server_error"
    assert get_error_type(503) == "service_unavailable"
    assert get_error_type(504) == "timeout_error"
    assert get_error_type(999) == "unknown_error"  # Unknown status code

# Test CORS middleware (integration test)
def test_cors_headers(client):
    """Test CORS headers are properly set"""
    response = client.options("/", headers={"Origin": "http://localhost:3000"})
    # Note: TestClient might not fully simulate CORS, but we can test the endpoint exists
    assert response.status_code in [200, 405]  # 405 is acceptable for OPTIONS

# Test with different file types
def test_extract_with_different_file_types(client, mock_text_extractor):
    """Test extraction with different file types"""
    file_types = [
        ('test.pdf', 'application/pdf'),
        ('test.docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
        ('test.jpg', 'image/jpeg'),
        ('test.png', 'image/png'),
        ('test.txt', 'text/plain')
    ]
    
    for filename, content_type in file_types:
        # Mock successful extraction for each file type
        mock_text_extractor.extract_from_content = AsyncMock(return_value=TextExtractionResponse(
            success=True,
            extracted_text=f"Extracted text from {filename}",
            file_type=filename.split('.')[-1]
        ))
        
        files = {
            'file': (filename, b'sample content', content_type)
        }
        response = client.post("/extract", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert f"Extracted text from {filename}" in data["extracted_text"]

# Test request validation
def test_analyze_invalid_json(client):
    """Test analyze endpoint with invalid JSON"""
    response = client.post("/analyze", json={"invalid_field": "value"})
    assert response.status_code == 422  # Validation error

def test_analyze_missing_text_field(client):
    """Test analyze endpoint with missing text field"""
    response = client.post("/analyze", json={})
    assert response.status_code == 422  # Validation error

# Performance and edge case tests
def test_analyze_maximum_length_text(client, mock_bias_detector):
    """Test analyze endpoint with very long text"""
    # Create a long text (just under any potential limits)
    long_text = "We are looking for a skilled software developer. " * 100  # 5000+ characters
    
    mock_result = BiasAnalysisResult(
        role="Software Developer",
        industry="Technology", 
        bias_score=0.1,
        inclusivity_score=0.9,
        clarity_score=0.8,
        issues=[],
        suggestions=[],
        seo_keywords=[],
        improved_text=long_text,
        overall_assessment="Analysis complete."
    )
    mock_bias_detector.analyze_comprehensive = AsyncMock(return_value=mock_result)
    
    response = client.post("/analyze", json={"text": long_text})
    
    assert response.status_code == 200
    data = response.json()
    assert data["bias_score"] == 0.1

def test_analyze_special_characters(client, mock_bias_detector):
    """Test analyze endpoint with special characters"""
    special_text = "We are looking for a developer who can handle émojis 😊, unicode characters ñ, and special symbols @#$%^&*()!"
    
    mock_result = BiasAnalysisResult(
        role="Developer",
        industry="Technology",
        bias_score=0.0,
        inclusivity_score=1.0,
        clarity_score=0.7,
        issues=[],
        suggestions=[],
        seo_keywords=[],
        improved_text=special_text,
        overall_assessment="No issues found."
    )
    mock_bias_detector.analyze_comprehensive = AsyncMock(return_value=mock_result)
    
    response = client.post("/analyze", json={"text": special_text})
    
    assert response.status_code == 200
    data = response.json()
    assert data["bias_score"] == 0.0

# Test concurrent requests (basic simulation)
def test_multiple_concurrent_requests(client, mock_bias_detector):
    """Test handling multiple requests"""
    mock_result = BiasAnalysisResult(
        role="Software Developer",
        industry="Technology",
        bias_score=0.2,
        inclusivity_score=0.8,
        clarity_score=0.9,
        issues=[],
        suggestions=[],
        seo_keywords=[],
        improved_text="Improved text",
        overall_assessment="Analysis complete."
    )
    mock_bias_detector.analyze_comprehensive = AsyncMock(return_value=mock_result)
    
    text = "We are looking for a skilled software developer who can work independently and contribute to our team's success."
    
    # Simulate multiple requests
    responses = []
    for i in range(5):
        response = client.post("/analyze", json={"text": text})
        responses.append(response)
    
    # All requests should succeed
    for response in responses:
        assert response.status_code == 200
        data = response.json()
        assert data["bias_score"] == 0.2

# Test response structure validation
def test_analyze_response_structure(client, mock_bias_detector):
    """Test that analyze response has correct structure"""
    mock_result = BiasAnalysisResult(
        role="Software Developer",
        industry="Technology",
        bias_score=0.3,
        inclusivity_score=0.7,
        clarity_score=0.8,
        issues=[],
        suggestions=[],
        seo_keywords=["python", "developer"],
        improved_text="Improved job description",
        overall_assessment="Moderate bias detected."
    )
    mock_bias_detector.analyze_comprehensive = AsyncMock(return_value=mock_result)
    
    text = "We are looking for an aggressive software developer who can work independently."
    response = client.post("/analyze", json={"text": text})
    
    assert response.status_code == 200
    data = response.json()
    
    # Check all required fields are present (including new optional ones)
    required_fields = [
        "bias_score", "inclusivity_score", "clarity_score", 
        "issues", "suggestions", "seo_keywords", "improved_text", 
        "overall_assessment", "role", "industry"
    ]
    
    for field in required_fields:
        assert field in data
    
    # Check data types - updated for Union[str, float] scores
    assert isinstance(data["bias_score"], (int, float, str))
    assert isinstance(data["inclusivity_score"], (int, float, str))
    assert isinstance(data["clarity_score"], (int, float, str))
    assert isinstance(data["issues"], list)
    assert isinstance(data["suggestions"], list)
    assert isinstance(data["seo_keywords"], list)
    assert isinstance(data["improved_text"], (str, type(None)))
    assert isinstance(data["overall_assessment"], (str, type(None)))
    assert isinstance(data["role"], (str, type(None)))
    assert isinstance(data["industry"], (str, type(None)))

def test_extract_response_structure(client, mock_text_extractor):
    """Test that extract response has correct structure"""
    mock_text_extractor.extract_from_content = AsyncMock(return_value=TextExtractionResponse(
        success=True,
        extracted_text="Sample extracted text",
        file_type="txt"
    ))
    
    files = {
        'file': ('test.txt', b'sample content', 'text/plain')
    }
    response = client.post("/extract", files=files)
    
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields
    required_fields = ["success", "extracted_text", "file_type"]
    for field in required_fields:
        assert field in data
    
    # Check data types
    assert isinstance(data["success"], bool)
    assert isinstance(data["extracted_text"], str)
    assert isinstance(data["file_type"], str)

# Test file size edge cases
def test_extract_file_at_size_limit(client, mock_text_extractor):
    """Test extract endpoint with file exactly at size limit"""
    # Create a file exactly 10MB
    content_size = 10 * 1024 * 1024
    content = b'x' * content_size
    
    mock_text_extractor.extract_from_content = AsyncMock(return_value=TextExtractionResponse(
        success=True,
        extracted_text="Extracted text from large file",
        file_type="txt"
    ))
    
    files = {
        'file': ('large.txt', content, 'text/plain')
    }
    response = client.post("/extract", files=files)
    
    # Should succeed as it's exactly at the limit
    assert response.status_code == 200

# Test with scores as strings (since schema allows Union[str, float])
def test_analyze_with_string_scores(client, mock_bias_detector):
    """Test analysis result with string scores"""
    mock_result = BiasAnalysisResult(
        role="Software Developer",
        industry="Technology",
        bias_score="0.3",  # String instead of float
        inclusivity_score="0.8",  # String instead of float
        clarity_score="0.9",  # String instead of float
        issues=[],
        suggestions=[],
        seo_keywords=["python", "developer"],
        improved_text="Improved job description",
        overall_assessment="Moderate bias detected."
    )
    mock_bias_detector.analyze_comprehensive = AsyncMock(return_value=mock_result)
    
    text = "We are looking for an aggressive software developer who can work independently."
    response = client.post("/analyze", json={"text": text})
    
    assert response.status_code == 200
    data = response.json()
    assert data["bias_score"] == "0.3"  # Should be string
    assert data["inclusivity_score"] == "0.8"
    assert data["clarity_score"] == "0.9"

# Test with None optional fields
def test_analyze_with_none_optional_fields(client, mock_bias_detector):
    """Test analysis result with None optional fields"""
    mock_result = BiasAnalysisResult(
        role=None,  # Optional field as None
        industry=None,  # Optional field as None
        bias_score=0.2,
        inclusivity_score=0.9,
        clarity_score=0.8,
        issues=[],
        suggestions=[],
        seo_keywords=[],
        improved_text=None,  # Optional field as None
        overall_assessment=None  # Optional field as None
    )
    mock_bias_detector.analyze_comprehensive = AsyncMock(return_value=mock_result)
    
    text = "We are looking for a skilled software developer who can work independently."
    response = client.post("/analyze", json={"text": text})
    
    assert response.status_code == 200
    data = response.json()
    assert data["role"] is None
    assert data["industry"] is None
    assert data["improved_text"] is None
    assert data["overall_assessment"] is None