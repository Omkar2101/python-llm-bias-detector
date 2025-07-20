

import pytest
from unittest.mock import AsyncMock, patch
from app.services.bias_detector import BiasDetector
from app.models.schemas import BiasAnalysisResult, BiasIssue, BiasType, SeverityLevel, CategoryType


@pytest.fixture
def bias_detector():
    """Create a BiasDetector instance for testing"""
    return BiasDetector()


@pytest.fixture
def mock_llm_service():
    """Mock LLM service to avoid external dependencies"""
    with patch('app.services.bias_detector.LLMService') as mock:
        # Mock bias detection response
        mock.return_value.detect_bias = AsyncMock(return_value={
            'issues': [],
            'bias_score': 0.2,
            'role': 'Software Engineer',
            'industry': 'Technology',
            'overall_assessment': 'Low bias detected'
        })
        
        # Mock improvement response
        mock.return_value.improve_language = AsyncMock(return_value={
            'suggestions': [],
            'clarity_score': 0.8,
            'inclusivity_score': 0.9,
            'seo_keywords': ['professional', 'qualified'],
            'improved_text': 'Improved version of text'
        })
        
        yield mock


class TestBasicFunctionality:
    """Test basic functionality of BiasDetector"""
    
    @pytest.mark.asyncio
    async def test_analyze_returns_correct_structure(self, bias_detector, mock_llm_service):
        """Test that analyze_comprehensive returns the correct structure"""
        text = "We need a qualified professional"
        
        result = await bias_detector.analyze_comprehensive(text)
        
        # Check return type
        assert isinstance(result, BiasAnalysisResult)
        
        # Check all required fields exist
        assert hasattr(result, 'role')
        assert hasattr(result, 'industry')
        assert hasattr(result, 'bias_score')
        assert hasattr(result, 'inclusivity_score')
        assert hasattr(result, 'clarity_score')
        assert hasattr(result, 'issues')
        assert hasattr(result, 'suggestions')
        assert hasattr(result, 'seo_keywords')
        assert hasattr(result, 'improved_text')
        assert hasattr(result, 'overall_assessment')
    
    
    @pytest.mark.asyncio
    async def test_scores_are_valid_floats(self, bias_detector, mock_llm_service):
        """Test that all scores are valid floats between 0 and 1"""
        text = "Looking for a team member"
        
        result = await bias_detector.analyze_comprehensive(text)
        
        # Check score types and ranges (scores can be str or float per schema)
        assert isinstance(result.bias_score, (str, float))
        assert isinstance(result.inclusivity_score, (str, float))
        assert isinstance(result.clarity_score, (str, float))
        
        # Convert to float for range checking
        bias_score = float(result.bias_score)
        inclusivity_score = float(result.inclusivity_score)
        clarity_score = float(result.clarity_score)
        
        assert 0.0 <= bias_score <= 1.0
        assert 0.0 <= inclusivity_score <= 1.0
        assert 0.0 <= clarity_score <= 1.0

    @pytest.mark.asyncio
    async def test_handles_string_scores_from_llm(self, bias_detector):
        """Test handling of string scores from LLM responses"""
        with patch.object(bias_detector.llm_service, 'detect_bias', return_value={
            'issues': [],
            'bias_score': '0.3',  # String score
            'role': 'Developer',
            'industry': 'Tech',
            'overall_assessment': 'Test assessment'
        }):
            with patch.object(bias_detector.llm_service, 'improve_language', return_value={
                'suggestions': [],
                'clarity_score': '0.7',  # String score
                'inclusivity_score': '0.8',  # String score
                'seo_keywords': [],
                'improved_text': None
            }):
                text = "Test text"
                result = await bias_detector.analyze_comprehensive(text)
                
                # Should convert string scores to float
                assert isinstance(result.bias_score, float)
                assert isinstance(result.clarity_score, float)
                assert isinstance(result.inclusivity_score, float)
                assert result.bias_score == 0.3
                assert result.clarity_score == 0.7
                assert result.inclusivity_score == 0.8


class TestErrorHandling:
    """Test error handling scenarios"""
    
    @pytest.mark.asyncio
    async def test_handles_llm_service_error(self, bias_detector):
        """Test that LLM service errors are handled gracefully"""
        with patch.object(bias_detector.llm_service, 'detect_bias', side_effect=Exception("LLM Error")):
            with patch.object(bias_detector.llm_service, 'improve_language', side_effect=Exception("LLM Error")):
                text = "Test text"
                
                # Should not raise exception
                result = await bias_detector.analyze_comprehensive(text)
                
                # Should still return valid result with fallback values
                assert isinstance(result, BiasAnalysisResult)
                assert isinstance(result.bias_score, float)
                assert result.bias_score == 0.5  # Default fallback value
                assert isinstance(result.clarity_score, float)
                assert result.clarity_score == 0.0  # Default fallback value
    
    
    @pytest.mark.asyncio
    async def test_handles_empty_text(self, bias_detector, mock_llm_service):
        """Test handling of empty text"""
        text = ""
        
        result = await bias_detector.analyze_comprehensive(text)
        
        assert isinstance(result, BiasAnalysisResult)
        assert isinstance(result.bias_score, (str, float))
        assert isinstance(result.issues, list)
    
    
    @pytest.mark.asyncio
    async def test_handles_very_long_text(self, bias_detector, mock_llm_service):
        """Test handling of very long text"""
        text = "Looking for qualified professionals. " * 1000
        
        result = await bias_detector.analyze_comprehensive(text)
        
        assert isinstance(result, BiasAnalysisResult)
        assert isinstance(result.bias_score, (str, float))

    @pytest.mark.asyncio
    async def test_handles_invalid_string_scores(self, bias_detector):
        """Test handling of invalid string scores from LLM"""
        with patch.object(bias_detector.llm_service, 'detect_bias', return_value={
            'issues': [],
            'bias_score': 'invalid_score',  # Invalid string
            'role': 'Developer',
            'industry': 'Tech',
            'overall_assessment': 'Test'
        }):
            with patch.object(bias_detector.llm_service, 'improve_language', return_value={
                'suggestions': [],
                'clarity_score': 'bad_score',  # Invalid string
                'inclusivity_score': 'also_bad',  # Invalid string
                'seo_keywords': [],
                'improved_text': None
            }):
                text = "Test text"
                result = await bias_detector.analyze_comprehensive(text)
                
                # Should default to 0.0 for invalid scores
                assert result.bias_score == 0.0
                assert result.clarity_score == 0.0
                assert result.inclusivity_score == 0.0


class TestHelperMethods:
    """Test helper methods"""
    
    def test_parse_category(self, bias_detector):
        """Test category parsing"""
        assert bias_detector._parse_category('clarity') == CategoryType.CLARITY
        assert bias_detector._parse_category('bias') == CategoryType.BIAS
        assert bias_detector._parse_category('seo') == CategoryType.SEO
        assert bias_detector._parse_category('inclusivity') == CategoryType.INCLUSIVITY
        assert bias_detector._parse_category('professionalism') == CategoryType.PROFESSIONALISM
        assert bias_detector._parse_category('legal') == CategoryType.LEGAL
        assert bias_detector._parse_category('unknown') == CategoryType.CLARITY  # default
        
        # Test pipe-separated categories
        assert bias_detector._parse_category('bias|clarity') == CategoryType.BIAS  # first valid
        assert bias_detector._parse_category('unknown|seo') == CategoryType.SEO  # second valid

    def test_parse_llm_issues_with_invalid_data(self, bias_detector):
        """Test parsing LLM issues with invalid or missing data"""
        invalid_issues = [
            {'type': 'invalid_type', 'text': 'test'},  # Invalid bias type
            {'type': 'gender', 'severity': 'invalid_severity', 'text': 'test'},  # Invalid severity
            {'type': 'gender'},  # Missing required text field
            {}  # Empty issue
        ]
        
        parsed_issues = bias_detector._parse_llm_issues(invalid_issues)
        
        # Should handle invalid data gracefully
        assert len(parsed_issues) == 2  # Only valid issues should be parsed
        assert all(isinstance(issue, BiasIssue) for issue in parsed_issues)


