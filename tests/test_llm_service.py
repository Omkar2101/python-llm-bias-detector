
import pytest
from unittest.mock import Mock, patch, AsyncMock
import json
from fastapi import HTTPException
from app.services.llm_service import LLMService


@pytest.fixture
def llm_service():
    """Create LLMService instance for testing"""
    with patch.dict('os.environ', {'GOOGLE_GEMINI_API_KEY': 'test-key'}):
        return LLMService()


@pytest.fixture
def mock_model():
    """Mock Gemini model for testing"""
    mock = Mock()
    mock.generate_content = Mock()
    return mock


class TestLLMServiceInitialization:
    """Test LLMService initialization"""
    
    def test_init_with_api_key(self):
        """Test initialization with API key"""
        with patch.dict('os.environ', {'GOOGLE_GEMINI_API_KEY': 'test-key'}):
            service = LLMService()
            assert service.model is not None
    
    def test_init_without_api_key(self):
        """Test initialization without API key"""
        with patch.dict('os.environ', {}, clear=True):
            # Should not raise exception during init
            service = LLMService()
            assert service.model is not None


class TestBiasDetection:
    """Test bias detection functionality"""
    
    @pytest.mark.asyncio
    async def test_detect_bias_success(self, llm_service):
        """Test successful bias detection"""
        # Mock response
        mock_response = Mock()
        mock_response.text = json.dumps({
            "role": "Software Engineer",
            "industry": "Technology",
            "issues": [
                {
                    "type": "gender",
                    "text": "aggressive",
                    "start_index": 10,
                    "end_index": 20,
                    "severity": "medium",
                    "explanation": "Gender-coded language",
                    "job_relevance": "This requirement is not necessary for software engineering tasks"
                }
            ],
            "bias_score": "0.3",
            "overall_assessment": "Low bias detected",
            "legitimate_requirements": ["Strong problem-solving skills", "Programming experience"]
        })
        
        with patch.object(llm_service.model, 'generate_content', return_value=mock_response):
            result = await llm_service.detect_bias("Test job description")
            
            assert isinstance(result, dict)
            assert "issues" in result
            assert "bias_score" in result
            assert "overall_assessment" in result
            assert "role" in result
            assert "industry" in result
            assert "legitimate_requirements" in result
            assert len(result["issues"]) == 1
            assert result["bias_score"] == "0.3"
            assert result["role"] == "Software Engineer"
            assert result["industry"] == "Technology"
    
    @pytest.mark.asyncio
    async def test_detect_bias_with_markdown_response(self, llm_service):
        """Test bias detection with markdown formatted response"""
        # Mock response with markdown
        mock_response = Mock()
        mock_response.text = '''```json
        {
            "role": "Data Analyst",
            "industry": "Analytics",
            "issues": [],
            "bias_score": "0.1",
            "overall_assessment": "No bias detected",
            "legitimate_requirements": ["Statistical analysis skills", "Data visualization experience"]
        }
        ```'''
        
        with patch.object(llm_service.model, 'generate_content', return_value=mock_response):
            result = await llm_service.detect_bias("Clean job description")
            
            assert isinstance(result, dict)
            assert "issues" in result
            assert result["bias_score"] == "0.1"
            assert len(result["issues"]) == 0
            assert result["role"] == "Data Analyst"
            assert result["industry"] == "Analytics"
    
    @pytest.mark.asyncio
    async def test_detect_bias_empty_text(self, llm_service):
        """Test bias detection with empty text"""
        mock_response = Mock()
        mock_response.text = json.dumps({
            "role": "N/A",
            "industry": "N/A",
            "issues": [],
            "bias_score": "0.0",
            "overall_assessment": "No content to analyze",
            "legitimate_requirements": []
        })
        
        with patch.object(llm_service.model, 'generate_content', return_value=mock_response):
            result = await llm_service.detect_bias("")
            
            assert isinstance(result, dict)
            assert len(result["issues"]) == 0
            assert result["role"] == "N/A"
            assert result["industry"] == "N/A"
    
    @pytest.mark.asyncio
    async def test_detect_bias_multiple_issues(self, llm_service):
        """Test bias detection with multiple issues"""
        mock_response = Mock()
        mock_response.text = json.dumps({
            "role": "Sales Representative", 
            "industry": "Sales",
            "issues": [
                {
                    "type": "gender",
                    "text": "aggressive",
                    "start_index": 10,
                    "end_index": 20,
                    "severity": "medium",
                    "explanation": "Gender-coded language",
                    "job_relevance": "Aggressiveness is not required for effective sales"
                },
                {
                    "type": "age",
                    "text": "young",
                    "start_index": 30,
                    "end_index": 35,
                    "severity": "high",
                    "explanation": "Age discrimination",
                    "job_relevance": "Age is not relevant to sales performance"
                }
            ],
            "bias_score": "0.7",
            "overall_assessment": "Multiple bias issues detected",
            "legitimate_requirements": ["Communication skills", "Customer service experience"]
        })
        
        with patch.object(llm_service.model, 'generate_content', return_value=mock_response):
            result = await llm_service.detect_bias("Looking for young aggressive candidates")
            
            assert len(result["issues"]) == 2
            assert result["bias_score"] == "0.7"
            assert result["role"] == "Sales Representative"
            assert result["industry"] == "Sales"
            
            # Check issue types
            issue_types = [issue["type"] for issue in result["issues"]]
            assert "gender" in issue_types
            assert "age" in issue_types

    @pytest.mark.asyncio
    async def test_detect_bias_non_job_description(self, llm_service):
        """Test bias detection with non-job description text"""
        mock_response = Mock()
        mock_response.text = json.dumps({
            "role": "N/A",
            "industry": "N/A", 
            "issues": [],
            "bias_score": "N/A",
            "overall_assessment": "The provided text does not appear to be a job description and therefore cannot be analyzed for employment-related bias.",
            "legitimate_requirements": "N/A"
        })
        
        with patch.object(llm_service.model, 'generate_content', return_value=mock_response):
            result = await llm_service.detect_bias("This is just a random paragraph about weather.")
            
            assert result["role"] == "N/A"
            assert result["industry"] == "N/A"
            assert result["bias_score"] == "N/A"
            assert result["legitimate_requirements"] == "N/A"
            assert len(result["issues"]) == 0


class TestLanguageImprovement:
    """Test language improvement functionality"""
    
    @pytest.mark.asyncio
    async def test_improve_language_success(self, llm_service):
        """Test successful language improvement"""
        mock_response = Mock()
        mock_response.text = json.dumps({
            "suggestions": [
                {
                    "original": "aggressive candidate",
                    "improved": "proactive candidate",
                    "rationale": "More inclusive language",
                    "category": "inclusivity"
                }
            ],
            "improved_text": "We seek a proactive professional for this role.",
            "clarity_score": 0.8,
            "inclusivity_score": 0.9,
            "seo_keywords": ["professional", "role", "candidate"]
        })
        
        with patch.object(llm_service.model, 'generate_content', return_value=mock_response):
            result = await llm_service.improve_language("We need aggressive candidate")
            
            assert isinstance(result, dict)
            assert "suggestions" in result
            assert "improved_text" in result
            assert "clarity_score" in result
            assert "inclusivity_score" in result
            assert "seo_keywords" in result
            
            assert len(result["suggestions"]) == 1
            assert result["clarity_score"] == 0.8
            assert result["inclusivity_score"] == 0.9
            assert len(result["seo_keywords"]) == 3
    
    @pytest.mark.asyncio
    async def test_improve_language_no_suggestions(self, llm_service):
        """Test language improvement with no suggestions needed"""
        mock_response = Mock()
        mock_response.text = json.dumps({
            "suggestions": [],
            "improved_text": "We seek a qualified professional for this role.",
            "clarity_score": 0.95,
            "inclusivity_score": 0.95,
            "seo_keywords": ["qualified", "professional", "role"]
        })
        
        with patch.object(llm_service.model, 'generate_content', return_value=mock_response):
            result = await llm_service.improve_language("We seek a qualified professional for this role.")
            
            assert len(result["suggestions"]) == 0
            assert result["clarity_score"] == 0.95
            assert result["inclusivity_score"] == 0.95
    
    @pytest.mark.asyncio
    async def test_improve_language_multiple_suggestions(self, llm_service):
        """Test language improvement with multiple suggestions"""
        mock_response = Mock()
        mock_response.text = json.dumps({
            "suggestions": [
                {
                    "original": "guys",
                    "improved": "team members",
                    "rationale": "Gender-neutral language",
                    "category": "inclusivity"
                },
                {
                    "original": "must be young",
                    "improved": "energetic approach preferred",
                    "rationale": "Removes age discrimination",
                    "category": "bias"
                }
            ],
            "improved_text": "We need team members with an energetic approach.",
            "clarity_score": 0.7,
            "inclusivity_score": 0.8,
            "seo_keywords": ["team", "members", "energetic"]
        })
        
        with patch.object(llm_service.model, 'generate_content', return_value=mock_response):
            result = await llm_service.improve_language("We need guys who must be young")
            
            assert len(result["suggestions"]) == 2
            
            # Check suggestion categories
            categories = [suggestion["category"] for suggestion in result["suggestions"]]
            assert "inclusivity" in categories
            assert "bias" in categories

    @pytest.mark.asyncio
    async def test_improve_language_non_job_description(self, llm_service):
        """Test language improvement with non-job description text"""
        mock_response = Mock()
        mock_response.text = json.dumps({
            "suggestions": [],
            "improved_text": "N/A",
            "clarity_score": "N/A",
            "inclusivity_score": "N/A",
            "seo_keywords": []
        })
        
        with patch.object(llm_service.model, 'generate_content', return_value=mock_response):
            result = await llm_service.improve_language("This is just a random paragraph about weather.")
            
            assert len(result["suggestions"]) == 0
            assert result["improved_text"] == "N/A"
            assert result["clarity_score"] == "N/A"
            assert result["inclusivity_score"] == "N/A"
            assert len(result["seo_keywords"]) == 0


class TestErrorHandling:
    """Test error handling scenarios"""
    
    @pytest.mark.asyncio
    async def test_detect_bias_invalid_json(self, llm_service):
        """Test bias detection with invalid JSON response"""
        mock_response = Mock()
        mock_response.text = "Invalid JSON response"
        
        with patch.object(llm_service.model, 'generate_content', return_value=mock_response):
            with pytest.raises(HTTPException) as exc_info:
                await llm_service.detect_bias("Test text")
            
            assert exc_info.value.status_code == 500
            assert "AI analysis failed" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_detect_bias_503_error(self, llm_service):
        """Test bias detection with 503 service overloaded error"""
        with patch.object(llm_service.model, 'generate_content', side_effect=Exception("503 Service overloaded")):
            with pytest.raises(HTTPException) as exc_info:
                await llm_service.detect_bias("Test text")
            
            assert exc_info.value.status_code == 503
            assert "temporarily overloaded" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_detect_bias_timeout_error(self, llm_service):
        """Test bias detection with timeout error"""
        with patch.object(llm_service.model, 'generate_content', side_effect=Exception("Request timeout exceeded")):
            with pytest.raises(HTTPException) as exc_info:
                await llm_service.detect_bias("Test text")
            
            assert exc_info.value.status_code == 504
            assert "Request timed out" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_detect_bias_quota_error(self, llm_service):
        """Test bias detection with quota exceeded error"""
        with patch.object(llm_service.model, 'generate_content', side_effect=Exception("quota exceeded")):
            with pytest.raises(HTTPException) as exc_info:
                await llm_service.detect_bias("Test text")
            
            assert exc_info.value.status_code == 429
            assert "quota exceeded" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_detect_bias_limit_error(self, llm_service):
        """Test bias detection with limit error"""
        with patch.object(llm_service.model, 'generate_content', side_effect=Exception("rate limit reached")):
            with pytest.raises(HTTPException) as exc_info:
                await llm_service.detect_bias("Test text")
            
            assert exc_info.value.status_code == 429
            assert "quota exceeded" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_error_handling_priority(self, llm_service):
        """Test that error handling follows the correct priority order"""
        # Test that 'exceeded' in timeout context gets 504
        with patch.object(llm_service.model, 'generate_content', side_effect=Exception("timeout exceeded")):
            with pytest.raises(HTTPException) as exc_info:
                await llm_service.detect_bias("Test text")
            assert exc_info.value.status_code == 504
        
        # Test that 'quota' gets 429 even with 'exceeded' in message  
        with patch.object(llm_service.model, 'generate_content', side_effect=Exception("quota limit reached")):
            with pytest.raises(HTTPException) as exc_info:
                await llm_service.detect_bias("Test text")
            assert exc_info.value.status_code == 429
    
    @pytest.mark.asyncio
    async def test_detect_bias_auth_error(self, llm_service):
        """Test bias detection with authentication error"""
        with patch.object(llm_service.model, 'generate_content', side_effect=Exception("Invalid API key")):
            with pytest.raises(HTTPException) as exc_info:
                await llm_service.detect_bias("Test text")
            
            assert exc_info.value.status_code == 500
            assert "Service configuration error" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_improve_language_error_handling(self, llm_service):
        """Test language improvement error handling"""
        with patch.object(llm_service.model, 'generate_content', side_effect=Exception("Service unavailable")):
            with pytest.raises(HTTPException) as exc_info:
                await llm_service.improve_language("Test text")
            
            assert exc_info.value.status_code == 500
            assert "AI analysis failed" in str(exc_info.value.detail)


class TestJSONResponseCleaning:
    """Test JSON response cleaning functionality"""
    
    @pytest.mark.asyncio
    async def test_clean_markdown_json_response(self, llm_service):
        """Test cleaning markdown-formatted JSON response"""
        mock_response = Mock()
        mock_response.text = '''```json
        {
            "role": "Marketing Manager",
            "industry": "Marketing",
            "issues": [],
            "bias_score": "0.1",
            "overall_assessment": "Clean",
            "legitimate_requirements": ["Marketing experience", "Communication skills"]
        }
        ```'''
        
        with patch.object(llm_service.model, 'generate_content', return_value=mock_response):
            result = await llm_service.detect_bias("Test")
            
            assert isinstance(result, dict)
            assert "issues" in result
            assert result["bias_score"] == "0.1"
            assert result["role"] == "Marketing Manager"
    
    @pytest.mark.asyncio
    async def test_clean_json_with_whitespace(self, llm_service):
        """Test cleaning JSON response with extra whitespace"""
        mock_response = Mock()
        mock_response.text = '''
        
        {
            "role": "HR Specialist",
            "industry": "Human Resources",
            "issues": [],
            "bias_score": "0.0",
            "overall_assessment": "Clean",
            "legitimate_requirements": ["HR certification", "Employee relations experience"]
        }
        
        '''
        
        with patch.object(llm_service.model, 'generate_content', return_value=mock_response):
            result = await llm_service.detect_bias("Test")
            
            assert isinstance(result, dict)
            assert result["bias_score"] == "0.0"
            assert result["role"] == "HR Specialist"


class TestRealWorldScenarios:
    """Test with real-world scenarios"""
    
    @pytest.mark.asyncio
    async def test_typical_job_description_analysis(self, llm_service):
        """Test analysis of a typical job description"""
        job_description = """
        We are looking for a Software Engineer to join our team.
        The ideal candidate should have strong problem-solving skills
        and be able to work in a fast-paced environment.
        """
        
        mock_response = Mock()
        mock_response.text = json.dumps({
            "role": "Software Engineer",
            "industry": "Technology",
            "issues": [],
            "bias_score": "0.1",
            "overall_assessment": "Job description appears neutral with minimal bias",
            "legitimate_requirements": ["Strong problem-solving skills", "Fast-paced environment adaptability"]
        })
        
        with patch.object(llm_service.model, 'generate_content', return_value=mock_response):
            result = await llm_service.detect_bias(job_description)
            
            assert isinstance(result, dict)
            assert float(result["bias_score"]) < 0.5  # Should be low bias
            assert len(result["issues"]) == 0
            assert result["role"] == "Software Engineer"
            assert result["industry"] == "Technology"
    
    @pytest.mark.asyncio
    async def test_biased_job_description_analysis(self, llm_service):
        """Test analysis of a biased job description"""
        job_description = """
        We need a young, aggressive male salesperson to join our brotherhood.
        Must be energetic and have a strong masculine presence.
        """
        
        mock_response = Mock()
        mock_response.text = json.dumps({
            "role": "Salesperson",
            "industry": "Sales", 
            "issues": [
                {
                    "type": "gender",
                    "text": "male",
                    "start_index": 20,
                    "end_index": 24,
                    "severity": "high",
                    "explanation": "Gender-specific requirement",
                    "job_relevance": "Gender is not relevant to sales performance"
                },
                {
                    "type": "age",
                    "text": "young",
                    "start_index": 12,
                    "end_index": 17,
                    "severity": "high",
                    "explanation": "Age discrimination",
                    "job_relevance": "Age is not relevant to sales ability"
                }
            ],
            "bias_score": "0.8",
            "overall_assessment": "Multiple serious bias issues detected",
            "legitimate_requirements": ["Sales experience", "Communication skills"]
        })
        
        with patch.object(llm_service.model, 'generate_content', return_value=mock_response):
            result = await llm_service.detect_bias(job_description)
            
            assert isinstance(result, dict)
            assert float(result["bias_score"]) > 0.5  # Should be high bias
            assert len(result["issues"]) >= 2  # Should detect multiple issues
            assert result["role"] == "Salesperson"
            assert result["industry"] == "Sales"
    
    @pytest.mark.asyncio
    async def test_improvement_suggestions_realistic(self, llm_service):
        """Test realistic improvement suggestions"""
        job_description = "We need guys who are aggressive and competitive."
        
        mock_response = Mock()
        mock_response.text = json.dumps({
            "suggestions": [
                {
                    "original": "guys",
                    "improved": "team members",
                    "rationale": "Gender-neutral language",
                    "category": "inclusivity"
                },
                {
                    "original": "aggressive and competitive",
                    "improved": "proactive and results-driven",
                    "rationale": "More professional tone",
                    "category": "professionalism"
                }
            ],
            "improved_text": "We need team members who are proactive and results-driven.",
            "clarity_score": 0.8,
            "inclusivity_score": 0.9,
            "seo_keywords": ["team", "members", "proactive", "results-driven"]
        })
        
        with patch.object(llm_service.model, 'generate_content', return_value=mock_response):
            result = await llm_service.improve_language(job_description)
            
            assert len(result["suggestions"]) == 2
            assert result["clarity_score"] == 0.8
            assert result["inclusivity_score"] == 0.9
            assert "improved_text" in result
            assert len(result["seo_keywords"]) > 0
            
            # Check that categories are valid
            categories = [suggestion["category"] for suggestion in result["suggestions"]]
            assert "inclusivity" in categories
            assert "professionalism" in categories