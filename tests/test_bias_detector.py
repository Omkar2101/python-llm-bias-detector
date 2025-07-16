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
        
        # Check score types and ranges
        assert isinstance(result.bias_score, float)
        assert isinstance(result.inclusivity_score, float)
        assert isinstance(result.clarity_score, float)
        
        assert 0.0 <= result.bias_score <= 1.0
        assert 0.0 <= result.inclusivity_score <= 1.0
        assert 0.0 <= result.clarity_score <= 1.0


class TestRuleBasedBiasDetection:
    """Test rule-based bias detection (doesn't need LLM)"""
    
    def test_detect_gender_coded_words(self, bias_detector):
        """Test detection of gender-coded words"""
        text = "We need an aggressive and competitive candidate"
        
        issues = bias_detector._detect_rule_based_bias(text)
        
        # Should find gender-coded words
        assert len(issues) > 0
        
        # Check issue properties
        gender_issues = [issue for issue in issues if issue.type == BiasType.GENDER]
        assert len(gender_issues) > 0
        
        # Check specific word detection
        found_words = [issue.text for issue in gender_issues]
        assert 'aggressive' in found_words
        assert 'competitive' in found_words
    
    
    def test_detect_explicit_gender_terms(self, bias_detector):
        """Test detection of explicit gender terms"""
        text = "Looking for a male candidate for this position"
        
        issues = bias_detector._detect_rule_based_bias(text)
        
        # Should detect 'male' as problematic
        assert len(issues) > 0
        male_issues = [issue for issue in issues if 'male' in issue.text]
        assert len(male_issues) > 0
    
    
    def test_detect_age_bias(self, bias_detector):
        """Test detection of age-related bias"""
        text = "Seeking young and energetic recent graduates"
        
        issues = bias_detector._detect_rule_based_bias(text)
        
        # Should detect age-related terms
        age_issues = [issue for issue in issues if issue.type == BiasType.AGE]
        assert len(age_issues) > 0
        
        # Check specific terms
        found_terms = [issue.text for issue in age_issues]
        assert any('young' in term for term in found_terms)
        assert any('energetic' in term for term in found_terms)
    
    
    def test_no_bias_in_neutral_text(self, bias_detector):
        """Test that neutral text doesn't trigger bias detection"""
        text = "We are seeking a qualified professional with relevant experience"
        
        issues = bias_detector._detect_rule_based_bias(text)
        
        # Should not detect any bias
        assert len(issues) == 0
    
    
    def test_severity_assignment(self, bias_detector):
        """Test that severity levels are assigned correctly"""
        text = "females need not apply for this position"
        
        issues = bias_detector._detect_rule_based_bias(text)
        
        # Should detect high severity for discriminatory language
        assert len(issues) > 0
        high_severity_issues = [issue for issue in issues if issue.severity == SeverityLevel.HIGH]
        assert len(high_severity_issues) > 0


class TestScoreCalculation:
    """Test score calculation methods"""
    
    def test_clarity_score_calculation(self, bias_detector):
        """Test clarity score calculation"""
        # Simple, clear text
        clear_text = "We need a qualified person for this job."
        clarity_score = bias_detector._calculate_clarity_score(clear_text)
        
        assert isinstance(clarity_score, float)
        assert 0.0 <= clarity_score <= 1.0
    
    
    def test_inclusivity_score_calculation(self, bias_detector):
        """Test inclusivity score calculation"""
        # Text with bias terms
        biased_text = "Looking for aggressive male candidates"
        inclusivity_score = bias_detector._calculate_inclusivity_score(biased_text)
        
        # Text without bias terms
        neutral_text = "Seeking qualified professionals"
        neutral_score = bias_detector._calculate_inclusivity_score(neutral_text)
        
        assert isinstance(inclusivity_score, float)
        assert isinstance(neutral_score, float)
        assert 0.0 <= inclusivity_score <= 1.0
        assert 0.0 <= neutral_score <= 1.0
        
        # Neutral text should have higher inclusivity score
        assert neutral_score >= inclusivity_score
    
    
    def test_bias_score_calculation(self, bias_detector):
        """Test bias score calculation"""
        # Text with multiple bias issues
        biased_text = "Looking for young aggressive males"
        bias_score = bias_detector._calculate_bias_score(biased_text)
        
        # Neutral text
        neutral_text = "Seeking qualified professionals"
        neutral_score = bias_detector._calculate_bias_score(neutral_text)
        
        assert isinstance(bias_score, float)
        assert isinstance(neutral_score, float)
        assert 0.0 <= bias_score <= 1.0
        assert 0.0 <= neutral_score <= 1.0
        
        # Biased text should have higher bias score
        assert bias_score >= neutral_score


class TestErrorHandling:
    """Test error handling scenarios"""
    
    @pytest.mark.asyncio
    async def test_handles_llm_service_error(self, bias_detector):
        """Test that LLM service errors are handled gracefully"""
        with patch.object(bias_detector.llm_service, 'detect_bias', side_effect=Exception("LLM Error")):
            text = "Test text"
            
            # Should not raise exception
            result = await bias_detector.analyze_comprehensive(text)
            
            # Should still return valid result
            assert isinstance(result, BiasAnalysisResult)
            assert isinstance(result.bias_score, float)
    
    
    @pytest.mark.asyncio
    async def test_handles_empty_text(self, bias_detector, mock_llm_service):
        """Test handling of empty text"""
        text = ""
        
        result = await bias_detector.analyze_comprehensive(text)
        
        assert isinstance(result, BiasAnalysisResult)
        assert isinstance(result.bias_score, float)
        assert isinstance(result.issues, list)
    
    
    @pytest.mark.asyncio
    async def test_handles_very_long_text(self, bias_detector, mock_llm_service):
        """Test handling of very long text"""
        text = "Looking for qualified professionals. " * 1000
        
        result = await bias_detector.analyze_comprehensive(text)
        
        assert isinstance(result, BiasAnalysisResult)
        assert isinstance(result.bias_score, float)


class TestHelperMethods:
    """Test helper methods"""
    
    def test_map_category_to_bias_type(self, bias_detector):
        """Test category to bias type mapping"""
        assert bias_detector._map_category_to_bias_type('gender_bias') == BiasType.GENDER
        assert bias_detector._map_category_to_bias_type('age_bias') == BiasType.AGE
        assert bias_detector._map_category_to_bias_type('race_bias') == BiasType.RACIAL
        assert bias_detector._map_category_to_bias_type('unknown_bias') == BiasType.GENDER  # default
    
    
    def test_parse_category(self, bias_detector):
        """Test category parsing"""
        assert bias_detector._parse_category('clarity') == CategoryType.CLARITY
        assert bias_detector._parse_category('bias') == CategoryType.BIAS
        assert bias_detector._parse_category('seo') == CategoryType.SEO
        assert bias_detector._parse_category('unknown') == CategoryType.CLARITY  # default
        
        # Test pipe-separated categories
        assert bias_detector._parse_category('bias|clarity') == CategoryType.BIAS  # first valid
        assert bias_detector._parse_category('unknown|seo') == CategoryType.SEO  # second valid


class TestRealWorldExamples:
    """Test with real-world examples"""
    
    @pytest.mark.asyncio
    async def test_job_posting_example(self, bias_detector, mock_llm_service):
        """Test with a typical job posting"""
        text = """
        We are seeking a dynamic team player to join our growing company.
        The ideal candidate should have strong communication skills and
        be able to work collaboratively with diverse teams.
        """
        
        result = await bias_detector.analyze_comprehensive(text)
        
        assert isinstance(result, BiasAnalysisResult)
        # This text should have relatively low bias
        assert result.bias_score <= 0.5
    
    
    @pytest.mark.asyncio
    async def test_biased_job_posting_example(self, bias_detector, mock_llm_service):
        """Test with a biased job posting"""
        text = """
        Looking for a young, aggressive male salesperson to join our brotherhood.
        Must be energetic and have a masculine presence. Recent graduates preferred.
        """
        
        result = await bias_detector.analyze_comprehensive(text)
        
        assert isinstance(result, BiasAnalysisResult)
        # This text should have multiple bias issues
        assert len(result.issues) > 0
        
        # Should detect multiple types of bias
        bias_types = {issue.type for issue in result.issues}
        assert len(bias_types) >= 2  # At least gender and age bias