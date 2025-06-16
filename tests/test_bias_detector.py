import pytest
from app.services.bias_detector import BiasDetector
from app.models.schemas import BiasAnalysisResult, BiasIssue, BiasType, SeverityLevel, CategoryType

@pytest.fixture
def bias_detector():
    return BiasDetector()

@pytest.mark.asyncio
async def test_gender_bias_detection(bias_detector):
    text = "We are looking for a strong male candidate who can be a great chairman."
    result = await bias_detector.analyze_comprehensive(text)
    
    assert isinstance(result, BiasAnalysisResult)
    assert len(result.issues) > 0
    
    # Check if gender bias is detected
    gender_issues = [issue for issue in result.issues if issue.type == BiasType.GENDER]
    assert len(gender_issues) > 0

@pytest.mark.asyncio
async def test_no_bias_text(bias_detector):
    text = "We are seeking a qualified professional with excellent communication skills."
    result = await bias_detector.analyze_comprehensive(text)
    
    assert isinstance(result, BiasAnalysisResult)
    assert len(result.issues) == 0

@pytest.mark.asyncio
async def test_multiple_bias_types(bias_detector):
    text = "Looking for young, energetic male graduates from top-tier universities."
    result = await bias_detector.analyze_comprehensive(text)
    
    assert isinstance(result, BiasAnalysisResult)
    
    # Should detect multiple types of bias
    bias_types = {issue.type for issue in result.issues}
    assert len(bias_types) >= 3  # Should detect gender, age, and educational bias

@pytest.mark.asyncio
async def test_severity_levels(bias_detector):
    text = "Seeking a masculine presence in our brotherhood of young professionals."
    result = await bias_detector.analyze_comprehensive(text)
    
    assert isinstance(result, BiasAnalysisResult)
    assert any(issue.severity == SeverityLevel.HIGH for issue in result.issues)

@pytest.mark.asyncio
async def test_suggestions_provided(bias_detector):
    text = "Looking for a chairman to lead our brotherhood."
    result = await bias_detector.analyze_comprehensive(text)
    
    assert isinstance(result, BiasAnalysisResult)
    assert any(len(issue.suggestions) > 0 for issue in result.issues)
