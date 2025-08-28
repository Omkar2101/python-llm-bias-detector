
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import json
from fastapi import HTTPException
from app.services.llm_service import LLMService


@pytest.fixture
def llm_service():
    """Create an LLMService instance for testing"""
    with patch('app.services.llm_service.genai.configure'):
        with patch('app.services.llm_service.genai.GenerativeModel'):
            return LLMService()


@pytest.fixture
def mock_gemini_response():
    """Mock Gemini API response with candidates structure"""
    mock_response = MagicMock()
    mock_candidate = MagicMock()
    mock_content = MagicMock()
    mock_part = MagicMock()
    mock_part.text = '''
    {
        "role": "Software Engineer",
        "industry": "Technology",
        "issues": [
            {
                "type": "gender",
                "text": "aggressive personality",
                "start_index": 50,
                "end_index": 71,
                "severity": "medium",
                "explanation": "This violates NYHRL (New York Human Rights Law) Section 296(1)(a) which prohibits gender-based discrimination in employment"
            }
        ],
        "bias_score": 0.2,
        "inclusivity_score": 0.8,
        "clarity_score": 0.9,
        "overall_assessment": "Low bias detected with minor language improvements needed"
    }
    '''
    mock_content.parts = [mock_part]
    mock_candidate.content = mock_content
    mock_response.candidates = [mock_candidate]
    return mock_response


@pytest.fixture
def mock_gemini_na_response():
    """Mock Gemini API N/A response for non-job text"""
    mock_response = MagicMock()
    mock_candidate = MagicMock()
    mock_content = MagicMock()
    mock_part = MagicMock()
    mock_part.text = '''
    {
        "role": "N/A",
        "industry": "N/A",
        "issues": [],
        "bias_score": "N/A",
        "inclusivity_score": "N/A",
        "clarity_score": "N/A",
        "overall_assessment": "The provided text does not appear to be a job description."
    }
    '''
    mock_content.parts = [mock_part]
    mock_candidate.content = mock_content
    mock_response.candidates = [mock_candidate]
    return mock_response


@pytest.fixture
def mock_improvement_response():
    """Mock Gemini API improvement response"""
    mock_response = MagicMock()
    mock_candidate = MagicMock()
    mock_content = MagicMock()
    mock_part = MagicMock()
    mock_part.text = '''
    {
        "suggestions": [
            {
                "original": "aggressive personality",
                "improved": "assertive communication skills",
                "rationale": "More inclusive and professional language",
                "category": "inclusivity"
            },
            {
                "original": "young team",
                "improved": "dynamic team",
                "rationale": "Removes age bias while maintaining positive tone",
                "category": "inclusivity"
            }
        ],
        "seo_keywords": ["software engineer", "python developer", "remote work", "tech stack", "agile"],
        "improved_text": "**JOB TITLE:** Senior Software Engineer\\n\\n**COMPANY:** Tech Solutions Inc\\n\\n**INDUSTRY:** Technology/Software Development\\n\\n**LOCATION:** Remote/Hybrid\\n\\n**EMPLOYMENT TYPE:** Full-time\\n\\n**JOB SUMMARY:**\\nJoin our dynamic team as a Senior Software Engineer where you'll develop cutting-edge applications."
    }
    '''
    mock_content.parts = [mock_part]
    mock_candidate.content = mock_content
    mock_response.candidates = [mock_candidate]
    return mock_response


@pytest.fixture
def mock_improvement_na_response():
    """Mock Gemini API N/A improvement response"""
    mock_response = MagicMock()
    mock_candidate = MagicMock()
    mock_content = MagicMock()
    mock_part = MagicMock()
    mock_part.text = '''
    {
        "suggestions": [],
        "improved_text": "N/A - The provided text does not appear to be a job description or does not contain sufficient job-related information to generate an improved version.",
        "seo_keywords": []
    }
    '''
    mock_content.parts = [mock_part]
    mock_candidate.content = mock_content
    mock_response.candidates = [mock_candidate]
    return mock_response


@pytest.fixture
def mock_empty_response():
    """Mock empty response from Gemini API"""
    mock_response = MagicMock()
    mock_response.candidates = []
    return mock_response


class TestDetectBias:
    """Test detect_bias method"""
    
    @pytest.mark.asyncio
    async def test_detect_bias_success(self, llm_service, mock_gemini_response):
        """Test successful bias detection"""
        llm_service.model.generate_content = MagicMock(return_value=mock_gemini_response)
        
        text = "We need an aggressive salesperson with strong leadership skills"
        result = await llm_service.detect_bias(text)
        
        # Verify the result structure matches expected format
        assert isinstance(result, dict)
        assert result["role"] == "Software Engineer"
        assert result["industry"] == "Technology"
        assert isinstance(result["issues"], list)
        assert len(result["issues"]) == 1
        assert result["bias_score"] == 0.2
        assert result["inclusivity_score"] == 0.8
        assert result["clarity_score"] == 0.9
        assert "Low bias detected" in result["overall_assessment"]
        
        # Verify issue structure
        issue = result["issues"][0]
        assert issue["type"] == "gender"
        assert issue["text"] == "aggressive personality"
        assert issue["severity"] == "medium"
        assert issue["start_index"] == 50
        assert issue["end_index"] == 71
        assert "NYHRL" in issue["explanation"]
    
    
    @pytest.mark.asyncio
    async def test_detect_bias_na_response(self, llm_service, mock_gemini_na_response):
        """Test N/A response for non-job description text"""
        llm_service.model.generate_content = MagicMock(return_value=mock_gemini_na_response)
        
        text = "This is just random text about weather and sports"
        result = await llm_service.detect_bias(text)
        
        # Verify N/A response structure
        assert result["role"] == "N/A"
        assert result["industry"] == "N/A"
        assert result["issues"] == []
        assert result["bias_score"] == "N/A"
        assert result["inclusivity_score"] == "N/A"
        assert result["clarity_score"] == "N/A"
        assert "does not appear to be a job description" in result["overall_assessment"]
    
    
    @pytest.mark.asyncio
    async def test_detect_bias_json_without_markdown(self, llm_service):
        """Test JSON response without markdown formatting"""
        mock_response = MagicMock()
        mock_candidate = MagicMock()
        mock_content = MagicMock()
        mock_part = MagicMock()
        mock_part.text = '''
        {
            "role": "Developer",
            "industry": "Tech",
            "issues": [],
            "bias_score": 0.1,
            "inclusivity_score": 0.9,
            "clarity_score": 0.8,
            "overall_assessment": "Clean job description"
        }
        '''
        mock_content.parts = [mock_part]
        mock_candidate.content = mock_content
        mock_response.candidates = [mock_candidate]
        llm_service.model.generate_content = MagicMock(return_value=mock_response)
        
        text = "Looking for a qualified developer"
        result = await llm_service.detect_bias(text)
        
        assert result["role"] == "Developer"
        assert result["industry"] == "Tech"
        assert result["bias_score"] == 0.1
    
    
    @pytest.mark.asyncio
    async def test_detect_bias_empty_response_error(self, llm_service, mock_empty_response):
        """Test handling of empty response"""
        llm_service.model.generate_content = MagicMock(return_value=mock_empty_response)
        
        text = "Test job description"
        
        with pytest.raises(HTTPException) as exc_info:
            await llm_service.detect_bias(text)
        
        assert exc_info.value.status_code == 500
        assert "AI analysis failed" in exc_info.value.detail


    @pytest.mark.asyncio
    async def test_detect_bias_malformed_json_error(self, llm_service):
        """Test handling of malformed JSON response"""
        mock_response = MagicMock()
        mock_candidate = MagicMock()
        mock_content = MagicMock()
        mock_part = MagicMock()
        mock_part.text = "This is not valid JSON"
        mock_content.parts = [mock_part]
        mock_candidate.content = mock_content
        mock_response.candidates = [mock_candidate]
        llm_service.model.generate_content = MagicMock(return_value=mock_response)
        
        text = "Test job description"
        
        with pytest.raises(HTTPException) as exc_info:
            await llm_service.detect_bias(text)
        
        assert exc_info.value.status_code == 500
        assert "AI analysis failed" in exc_info.value.detail
    
    
    @pytest.mark.asyncio
    async def test_detect_bias_api_503_error(self, llm_service):
        """Test handling of 503 service overloaded error"""
        llm_service.model.generate_content = MagicMock(side_effect=Exception("503 Service overloaded"))
        
        text = "Test job description"
        
        with pytest.raises(HTTPException) as exc_info:
            await llm_service.detect_bias(text)
        
        assert exc_info.value.status_code == 503
        assert "AI service is temporarily overloaded" in exc_info.value.detail
    
    
    @pytest.mark.asyncio
    async def test_detect_bias_quota_exceeded_error(self, llm_service):
        """Test handling of quota exceeded error"""
        llm_service.model.generate_content = MagicMock(side_effect=Exception("Quota limit exceeded"))
        
        text = "Test job description"
        
        with pytest.raises(HTTPException) as exc_info:
            await llm_service.detect_bias(text)
        
        assert exc_info.value.status_code == 429
        assert "API quota exceeded" in exc_info.value.detail
    
    
    @pytest.mark.asyncio
    async def test_detect_bias_timeout_error(self, llm_service):
        """Test handling of timeout error"""
        llm_service.model.generate_content = MagicMock(side_effect=Exception("Request timeout exceeded"))
        
        text = "Test job description"
        
        with pytest.raises(HTTPException) as exc_info:
            await llm_service.detect_bias(text)
        
        assert exc_info.value.status_code == 504
        assert "Request timed out" in exc_info.value.detail
    
    
    @pytest.mark.asyncio
    async def test_detect_bias_authentication_error(self, llm_service):
        """Test handling of authentication error"""
        llm_service.model.generate_content = MagicMock(side_effect=Exception("API key authentication failed"))
        
        text = "Test job description"
        
        with pytest.raises(HTTPException) as exc_info:
            await llm_service.detect_bias(text)
        
        assert exc_info.value.status_code == 500
        assert "Service configuration error" in exc_info.value.detail
    
    
    @pytest.mark.asyncio
    async def test_detect_bias_generic_error(self, llm_service):
        """Test handling of generic error"""
        llm_service.model.generate_content = MagicMock(side_effect=Exception("Some random error"))
        
        text = "Test job description"
        
        with pytest.raises(HTTPException) as exc_info:
            await llm_service.detect_bias(text)
        
        assert exc_info.value.status_code == 500
        assert "AI analysis failed: Some random error" in exc_info.value.detail


class TestImproveLanguage:
    """Test improve_language method"""
    
    @pytest.mark.asyncio
    async def test_improve_language_success(self, llm_service, mock_improvement_response):
        """Test successful language improvement"""
        llm_service.model.generate_content = MagicMock(return_value=mock_improvement_response)
        
        text = "We need aggressive young professionals for our team"
        detected_issues = [
            {"type": "gender", "text": "aggressive personality", "severity": "medium", "explanation": "Gendered language"}
        ]
        result = await llm_service.improve_language(text, detected_issues)
        
        # Verify the result structure matches expected format
        assert isinstance(result, dict)
        assert isinstance(result["suggestions"], list)
        assert len(result["suggestions"]) == 2
        assert isinstance(result["seo_keywords"], list)
        assert len(result["seo_keywords"]) == 5
        assert result["improved_text"].startswith("**JOB TITLE:** Senior Software Engineer")
        
        # Verify suggestions structure
        suggestion = result["suggestions"][0]
        assert suggestion["original"] == "aggressive personality"
        assert suggestion["improved"] == "assertive communication skills"
        assert suggestion["category"] == "inclusivity"
        assert "inclusive" in suggestion["rationale"].lower()
        
        # Verify SEO keywords
        assert "software engineer" in result["seo_keywords"]
        assert "python developer" in result["seo_keywords"]
    
    
    @pytest.mark.asyncio
    async def test_improve_language_na_response(self, llm_service, mock_improvement_na_response):
        """Test N/A response for non-job description text"""
        llm_service.model.generate_content = MagicMock(return_value=mock_improvement_na_response)
        
        text = "This is just random text about weather"
        result = await llm_service.improve_language(text)
        
        # Verify N/A response structure
        assert result["suggestions"] == []
        assert result["seo_keywords"] == []
        assert result["improved_text"].startswith("N/A - The provided text does not appear")
    
    
    @pytest.mark.asyncio
    async def test_improve_language_json_without_markdown(self, llm_service):
        """Test JSON response without markdown formatting"""
        mock_response = MagicMock()
        mock_candidate = MagicMock()
        mock_content = MagicMock()
        mock_part = MagicMock()
        mock_part.text = '''
        {
            "suggestions": [
                {
                    "original": "test phrase",
                    "improved": "better phrase",
                    "rationale": "clearer language",
                    "category": "clarity"
                }
            ],
            "seo_keywords": ["developer", "software"],
            "improved_text": "**JOB TITLE:** Software Developer"
        }
        '''
        mock_content.parts = [mock_part]
        mock_candidate.content = mock_content
        mock_response.candidates = [mock_candidate]
        llm_service.model.generate_content = MagicMock(return_value=mock_response)
        
        text = "Looking for a developer"
        result = await llm_service.improve_language(text)
        
        assert len(result["suggestions"]) == 1
        assert result["suggestions"][0]["original"] == "test phrase"
        assert len(result["seo_keywords"]) == 2
    
    
    @pytest.mark.asyncio
    async def test_improve_language_empty_response_error(self, llm_service, mock_empty_response):
        """Test handling of empty response"""
        llm_service.model.generate_content = MagicMock(return_value=mock_empty_response)
        
        text = "Test job description"
        
        with pytest.raises(HTTPException) as exc_info:
            await llm_service.improve_language(text)
        
        assert exc_info.value.status_code == 500
        assert "AI analysis failed" in exc_info.value.detail


    @pytest.mark.asyncio
    async def test_improve_language_malformed_json_error(self, llm_service):
        """Test handling of malformed JSON response"""
        mock_response = MagicMock()
        mock_candidate = MagicMock()
        mock_content = MagicMock()
        mock_part = MagicMock()
        mock_part.text = "Invalid JSON response"
        mock_content.parts = [mock_part]
        mock_candidate.content = mock_content
        mock_response.candidates = [mock_candidate]
        llm_service.model.generate_content = MagicMock(return_value=mock_response)
        
        text = "Test job description"
        
        with pytest.raises(HTTPException) as exc_info:
            await llm_service.improve_language(text)
        
        assert exc_info.value.status_code == 500
        assert "AI analysis failed" in exc_info.value.detail
    
    
    @pytest.mark.asyncio
    async def test_improve_language_api_503_error(self, llm_service):
        """Test handling of 503 service overloaded error"""
        llm_service.model.generate_content = MagicMock(side_effect=Exception("503 overloaded"))
        
        text = "Test job description"
        
        with pytest.raises(HTTPException) as exc_info:
            await llm_service.improve_language(text)
        
        assert exc_info.value.status_code == 503
        assert "AI service is temporarily overloaded" in exc_info.value.detail
    
    
    @pytest.mark.asyncio
    async def test_improve_language_quota_exceeded_error(self, llm_service):
        """Test handling of quota exceeded error"""
        llm_service.model.generate_content = MagicMock(side_effect=Exception("quota limit reached"))
        
        text = "Test job description"
        
        with pytest.raises(HTTPException) as exc_info:
            await llm_service.improve_language(text)
        
        assert exc_info.value.status_code == 429
        assert "API quota exceeded" in exc_info.value.detail
    
    
    @pytest.mark.asyncio
    async def test_improve_language_timeout_error(self, llm_service):
        """Test handling of timeout error"""
        llm_service.model.generate_content = MagicMock(side_effect=Exception("timeout exceeded"))
        
        text = "Test job description"
        
        with pytest.raises(HTTPException) as exc_info:
            await llm_service.improve_language(text)
        
        assert exc_info.value.status_code == 504
        assert "Request timed out" in exc_info.value.detail
    
    
    @pytest.mark.asyncio
    async def test_improve_language_authentication_error(self, llm_service):
        """Test handling of authentication error"""
        llm_service.model.generate_content = MagicMock(side_effect=Exception("authentication failed"))
        
        text = "Test job description"
        
        with pytest.raises(HTTPException) as exc_info:
            await llm_service.improve_language(text)
        
        assert exc_info.value.status_code == 500
        assert "Service configuration error" in exc_info.value.detail
    
    
    @pytest.mark.asyncio
    async def test_improve_language_generic_error(self, llm_service):
        """Test handling of generic error"""
        llm_service.model.generate_content = MagicMock(side_effect=Exception("Unknown error occurred"))
        
        text = "Test job description"
        
        with pytest.raises(HTTPException) as exc_info:
            await llm_service.improve_language(text)
        
        assert exc_info.value.status_code == 500
        assert "AI analysis failed: Unknown error occurred" in exc_info.value.detail


class TestInitialization:
    """Test LLMService initialization"""
    
    @patch('app.services.llm_service.load_dotenv')
    @patch('app.services.llm_service.genai.configure')
    @patch('app.services.llm_service.genai.GenerativeModel')
    @patch('app.services.llm_service.os.getenv')
    def test_initialization_success(self, mock_getenv, mock_model, mock_configure, mock_load_dotenv):
        """Test successful initialization"""
        mock_getenv.side_effect = lambda key, default=None: {
            "GOOGLE_GEMINI_API_KEY": "test_api_key",
        }.get(key, default)
        
        service = LLMService()
        
        # Verify initialization calls
        mock_load_dotenv.assert_called_once()
        mock_configure.assert_called_once_with(api_key="test_api_key")
        assert service.model is not None
    
    
    

class TestJsonParsing:
    """Test JSON parsing edge cases"""
    
    @pytest.mark.asyncio
    async def test_detect_bias_json_with_extra_whitespace(self, llm_service):
        """Test JSON parsing with extra whitespace"""
        mock_response = MagicMock()
        mock_candidate = MagicMock()
        mock_content = MagicMock()
        mock_part = MagicMock()
        mock_part.text = '''   ```json
        
        {
            "role": "Engineer",
            "industry": "Technology",
            "issues": [],
            "bias_score": 0.0,
            "inclusivity_score": 1.0,
            "clarity_score": 1.0,
            "overall_assessment": "Good"
        }
        
        ```   '''
        mock_content.parts = [mock_part]
        mock_candidate.content = mock_content
        mock_response.candidates = [mock_candidate]
        llm_service.model.generate_content = MagicMock(return_value=mock_response)
        
        text = "Test job description"
        result = await llm_service.detect_bias(text)
        
        assert result["role"] == "Engineer"
        assert result["bias_score"] == 0.0
    
    
    @pytest.mark.asyncio
    async def test_improve_language_json_with_escaped_newlines(self, llm_service):
        """Test JSON parsing with escaped newlines in improved_text"""
        mock_response = MagicMock()
        mock_candidate = MagicMock()
        mock_content = MagicMock()
        mock_part = MagicMock()
        mock_part.text = '''```json
        {
            "suggestions": [],
            "seo_keywords": ["test"],
            "improved_text": "**JOB TITLE:** Test\\n\\n**COMPANY:** Test Corp\\n\\n**LOCATION:** Remote"
        }
        ```'''
        mock_content.parts = [mock_part]
        mock_candidate.content = mock_content
        mock_response.candidates = [mock_candidate]
        llm_service.model.generate_content = MagicMock(return_value=mock_response)
        
        text = "Test job description"
        result = await llm_service.improve_language(text)
        
        assert "**JOB TITLE:** Test" in result["improved_text"]
        assert "**COMPANY:** Test Corp" in result["improved_text"]


class TestRegexFallback:
    """Test regex fallback for JSON parsing"""
    
    @pytest.mark.asyncio
    async def test_detect_bias_regex_fallback(self, llm_service):
        """Test regex fallback when JSON parsing fails initially"""
        mock_response = MagicMock()
        mock_candidate = MagicMock()
        mock_content = MagicMock()
        mock_part = MagicMock()
        mock_part.text = '''Some text before JSON
        {
            "role": "Engineer",
            "industry": "Tech",
            "issues": [],
            "bias_score": 0.0,
            "inclusivity_score": 1.0,
            "clarity_score": 1.0,
            "overall_assessment": "Clean"
        }
        Some text after JSON'''
        mock_content.parts = [mock_part]
        mock_candidate.content = mock_content
        mock_response.candidates = [mock_candidate]
        llm_service.model.generate_content = MagicMock(return_value=mock_response)
        
        text = "Test job description"
        result = await llm_service.detect_bias(text)
        
        assert result["role"] == "Engineer"
        assert result["industry"] == "Tech"
        assert result["bias_score"] == 0.0
    
    
    @pytest.mark.asyncio
    async def test_improve_language_regex_fallback(self, llm_service):
        """Test regex fallback for improve_language method"""
        mock_response = MagicMock()
        mock_candidate = MagicMock()
        mock_content = MagicMock()
        mock_part = MagicMock()
        mock_part.text = '''Text before
        {
            "suggestions": [{"original": "test", "improved": "better", "rationale": "clearer", "category": "clarity"}],
            "seo_keywords": ["keyword1"],
            "improved_text": "**JOB TITLE:** Test Job"
        }
        Text after'''
        mock_content.parts = [mock_part]
        mock_candidate.content = mock_content
        mock_response.candidates = [mock_candidate]
        llm_service.model.generate_content = MagicMock(return_value=mock_response)
        
        text = "Test job description"
        result = await llm_service.improve_language(text)
        
        assert len(result["suggestions"]) == 1
        assert result["suggestions"][0]["original"] == "test"
        assert len(result["seo_keywords"]) == 1
        assert result["improved_text"] == "**JOB TITLE:** Test Job"