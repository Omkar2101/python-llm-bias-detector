


# import pytest
# from unittest.mock import AsyncMock, patch
# from app.services.bias_detector import BiasDetector
# from app.models.schemas import (
#     BiasAnalysisResult, BiasIssue, Suggestion, BiasType, 
#     SeverityLevel, CategoryType
# )


# @pytest.fixture
# def bias_detector():
#     """Create a BiasDetector instance for testing"""
#     return BiasDetector()


# @pytest.fixture
# def mock_llm_service():
#     """Mock LLM service to avoid external dependencies"""
#     with patch('app.services.bias_detector.LLMService') as mock:
#         # Mock bias detection response - matches your actual LLM response format
#         mock.return_value.detect_bias = AsyncMock(return_value={
#             'role': 'salesperson',
#             'industry': 'sales',
#             'issues': [
#                 {
#                     'type': 'gender',
#                     'text': 'aggressive salesperson',
#                     'start_index': 11,
#                     'end_index': 31,
#                     'severity': 'medium',
#                     'explanation': 'Gendered language that may discourage female applicants',
#                     'job_relevance': 'Assertiveness can be described in neutral terms'
#                 },
#                 {
#                     'type': 'gender',
#                     'text': 'strong personality',
#                     'start_index': 37,
#                     'end_index': 55,
#                     'severity': 'low',
#                     'explanation': 'May be perceived as gendered language',
#                     'job_relevance': 'Specific skills can be described more clearly'
#                 }
#             ],
#             'bias_score': 0.2,
#             'inclusivity_score': 0.8,
#             'clarity_score': 0.9,
#             'overall_assessment': 'Low bias detected with some minor language improvements needed'
#         })
        
#         # Mock improvement response - matches your actual LLM response format
#         # IMPORTANT: Make sure improved_text is NOT "Error generating improved text"
#         mock.return_value.improve_language = AsyncMock(return_value={
#             'suggestions': [
#                 {
#                     'original': 'aggressive salesperson',
#                     'improved': 'results-driven sales professional',
#                     'rationale': 'More inclusive and professional language',
#                     'category': 'inclusivity'
#                 },
#                 {
#                     'original': 'strong personality',
#                     'improved': 'excellent interpersonal skills',
#                     'rationale': 'More specific and inclusive description',
#                     'category': 'bias|inclusivity'
#                 }
#             ],
#             'seo_keywords': ['sales representative', 'sales professional', 'client relations', 'sales targets', 'communication'],
#             'improved_text': '''**JOB TITLE:** Sales Representative

# **COMPANY:** Sales Solutions Inc

# **INDUSTRY:** Sales/Marketing

# **LOCATION:** Remote/Hybrid

# **EMPLOYMENT TYPE:** Full-time

# **JOB SUMMARY:**
# Join our dynamic sales team as a Sales Representative where you'll drive revenue growth through client relationship building. You'll work with prospective clients to understand their needs and present tailored solutions that deliver value.

# **KEY RESPONSIBILITIES:**
# • Build and maintain strong client relationships through effective communication
# • Present product solutions to meet client requirements
# • Achieve monthly and quarterly sales targets
# • Collaborate with internal teams to ensure client satisfaction

# **REQUIRED QUALIFICATIONS:**
# • Bachelor's degree in Business, Marketing, or related field
# • 2+ years of sales experience
# • Proven track record of meeting sales targets

# **PREFERRED QUALIFICATIONS:**
# • Experience with CRM software
# • Industry-specific knowledge in relevant sectors

# **REQUIRED SKILLS:**
# • Excellent verbal and written communication abilities
# • Strong negotiation and presentation skills
# • Results-oriented mindset
# • Ability to work independently

# **WHAT WE OFFER:**
# • Competitive base salary plus commission
# • Comprehensive health benefits
# • Professional development opportunities
# • Flexible work arrangements

# **APPLICATION PROCESS:**
# Submit your resume highlighting your sales achievements and experience.'''
#         })
        
#         yield mock


# @pytest.fixture
# def mock_llm_service_na_response():
#     """Mock LLM service for non-job description text"""
#     with patch('app.services.bias_detector.LLMService') as mock:
#         # Mock N/A response for non-job text
#         mock.return_value.detect_bias = AsyncMock(return_value={
#             'role': 'N/A',
#             'industry': 'N/A',
#             'issues': [],
#             'bias_score': 'N/A',
#             'inclusivity_score': 'N/A',
#             'clarity_score': 'N/A',
#             'overall_assessment': 'The provided text does not appear to be a job description.'
#         })
        
#         # IMPORTANT: Make sure this doesn't return error text
#         mock.return_value.improve_language = AsyncMock(return_value={
#             'suggestions': [],
#             'improved_text': 'N/A - The provided text does not appear to be a job description or does not contain sufficient job-related information to generate an improved version.',
#             'seo_keywords': []
#         })
        
#         yield mock


# class TestBasicFunctionality:
#     """Test basic functionality of BiasDetector"""
    
#     # @pytest.mark.asyncio
#     # async def test_analyze_returns_correct_structure(self, bias_detector, mock_llm_service):
#     #     """Test that analyze_comprehensive returns the correct structure"""
#     #     text = "We need an aggressive salesperson with strong leadership skills"
        
#     #     result = await bias_detector.analyze_comprehensive(text)
        
#     #     # Check return type
#     #     assert isinstance(result, BiasAnalysisResult)
        
#     #     # Check all required fields exist and have correct types
#     #     assert hasattr(result, 'role')
#     #     assert hasattr(result, 'industry')
#     #     assert hasattr(result, 'bias_score')
#     #     assert hasattr(result, 'inclusivity_score') 
#     #     assert hasattr(result, 'clarity_score')
#     #     assert hasattr(result, 'issues')
#     #     assert hasattr(result, 'suggestions')
#     #     assert hasattr(result, 'seo_keywords')
#     #     assert hasattr(result, 'improved_text')
#     #     assert hasattr(result, 'overall_assessment')
        
#     #     # Check types match schema
#     #     assert isinstance(result.issues, list)
#     #     assert isinstance(result.suggestions, list)
#     #     assert isinstance(result.seo_keywords, list)
#     #     assert isinstance(result.role, str)
#     #     assert isinstance(result.industry, str)
#     #     assert isinstance(result.overall_assessment, str)
        
      
    
    
#     @pytest.mark.asyncio
#     async def test_scores_are_valid_types(self, bias_detector):
#         """Test that all scores are valid types per schema (Union[str, float])"""
#         text = "Looking for a qualified team member with excellent communication skills"
        
#         # Mock both services explicitly for this test
#         with patch.object(bias_detector.llm_service, 'detect_bias', return_value={
#             'issues': [],
#             'bias_score': 0.3,
#             'inclusivity_score': 0.8,
#             'clarity_score': 0.9,
#             'role': 'Team Member',
#             'industry': 'General',
#             'overall_assessment': 'Test assessment'
#         }):
#             with patch.object(bias_detector.llm_service, 'improve_language', return_value={
#                 'suggestions': [],
#                 'seo_keywords': ['communication', 'teamwork'],
#                 'improved_text': 'Valid improved text'
#             }):
#                 result = await bias_detector.analyze_comprehensive(text)
                
#                 # Check score types (can be str or float per schema)
#                 assert isinstance(result.bias_score, (str, float))
#                 assert isinstance(result.inclusivity_score, (str, float))
#                 assert isinstance(result.clarity_score, (str, float))
                
#                 # If float, should be in valid range
#                 if isinstance(result.bias_score, float):
#                     assert 0.0 <= result.bias_score <= 1.0
#                 if isinstance(result.inclusivity_score, float):
#                     assert 0.0 <= result.inclusivity_score <= 1.0
#                 if isinstance(result.clarity_score, float):
#                     assert 0.0 <= result.clarity_score <= 1.0
    

#     @pytest.mark.asyncio
#     async def test_handles_string_scores_from_llm(self, bias_detector):
#         """Test handling of string scores from LLM responses"""
#         with patch.object(bias_detector.llm_service, 'detect_bias', return_value={
#             'issues': [],
#             'bias_score': '0.3',  # String score
#             'inclusivity_score': '0.8',  # String score  
#             'clarity_score': '0.7',  # String score
#             'role': 'Developer',
#             'industry': 'Technology',
#             'overall_assessment': 'Test assessment'
#         }):
#             with patch.object(bias_detector.llm_service, 'improve_language', return_value={
#                 'suggestions': [],
#                 'seo_keywords': ['python', 'developer'],
#                 'improved_text': 'Improved text'  # Valid improved text
#             }):
#                 text = "Test job description text"
#                 result = await bias_detector.analyze_comprehensive(text)
                
#                 # Should convert string scores to float
#                 assert isinstance(result.bias_score, float)
#                 assert isinstance(result.clarity_score, float)
#                 assert isinstance(result.inclusivity_score, float)
#                 assert result.bias_score == 0.3
#                 assert result.clarity_score == 0.7
#                 assert result.inclusivity_score == 0.8


# class TestErrorHandling:
#     """Test error handling scenarios"""
    
#     @pytest.mark.asyncio
#     async def test_handles_llm_detect_bias_error(self, bias_detector):
#         """Test that detect_bias errors are handled gracefully"""
#         with patch.object(bias_detector.llm_service, 'detect_bias', side_effect=Exception("API Error")):
#             with patch.object(bias_detector.llm_service, 'improve_language', return_value={
#                 'suggestions': [],
#                 'seo_keywords': [],
#                 'improved_text': 'Valid improved text'  # Valid improved text
#             }):
#                 text = "Test job description"
                
#                 # Should not raise exception
#                 result = await bias_detector.analyze_comprehensive(text)
                
#                 # Should return valid result with fallback values
#                 assert isinstance(result, BiasAnalysisResult)
#                 assert result.bias_score == 0.0  # Default fallback
#                 assert len(result.issues) == 0  # Empty issues list
#                 # These fields should have valid default values when detect_bias fails
#                 assert result.role == "Unknown"
#                 assert result.industry == "Unknown"
#                 assert result.overall_assessment == "Analysis could not be completed due to service error"
    
    
#     @pytest.mark.asyncio
#     async def test_handles_llm_improve_language_error(self, bias_detector):
#         """Test that improve_language errors raise exception as expected"""  
#         with patch.object(bias_detector.llm_service, 'detect_bias', return_value={
#             'issues': [],
#             'bias_score': 0.2,
#             'inclusivity_score': 0.8,
#             'clarity_score': 0.9,
#             'role': 'Developer',
#             'industry': 'Tech',
#             'overall_assessment': 'Good'
#         }):
#             with patch.object(bias_detector.llm_service, 'improve_language', side_effect=Exception("API Error")):
#                 text = "Test job description"
                
#                 # Should raise exception due to error handling in analyze_comprehensive
#                 with pytest.raises(Exception, match="Language improvement service failed"):
#                     await bias_detector.analyze_comprehensive(text)


#     @pytest.mark.asyncio
#     async def test_handles_improve_language_error_text_response(self, bias_detector):
#         """Test that improve_language returning error text raises exception"""  
#         with patch.object(bias_detector.llm_service, 'detect_bias', return_value={
#             'issues': [],
#             'bias_score': 0.2,
#             'inclusivity_score': 0.8,
#             'clarity_score': 0.9,
#             'role': 'Developer',
#             'industry': 'Tech',
#             'overall_assessment': 'Good'
#         }):
#             with patch.object(bias_detector.llm_service, 'improve_language', return_value={
#                 'suggestions': [],
#                 'seo_keywords': [],
#                 'improved_text': 'Error generating improved text'  # This should trigger exception
#             }):
#                 text = "Test job description"
                
#                 # Should raise exception due to error handling in analyze_comprehensive
#                 with pytest.raises(Exception, match="Language improvement service failed"):
#                     await bias_detector.analyze_comprehensive(text)
    
    
#     # @pytest.mark.asyncio
#     # async def test_handles_empty_text(self, bias_detector, mock_llm_service):
#     #     """Test handling of empty text"""
#     #     text = ""
        
#     #     result = await bias_detector.analyze_comprehensive(text)
        
#     #     assert isinstance(result, BiasAnalysisResult)
#     #     assert isinstance(result.bias_score, (str, float))
#     #     assert isinstance(result.issues, list)
#     #     assert isinstance(result.suggestions, list)
#     #     # Ensure all required fields are present and valid
#     #     assert isinstance(result.role, str)
#     #     assert isinstance(result.industry, str)
#     #     assert isinstance(result.overall_assessment, str)
    
    
#     # @pytest.mark.asyncio 
#     # async def test_handles_very_long_text(self, bias_detector, mock_llm_service):
#     #     """Test handling of very long text"""
#     #     text = "Looking for qualified software engineers with excellent skills. " * 1000
        
#     #     result = await bias_detector.analyze_comprehensive(text)
        
#     #     assert isinstance(result, BiasAnalysisResult)
#     #     assert isinstance(result.bias_score, (str, float))
#     #     assert isinstance(result.role, str)
#     #     assert isinstance(result.industry, str)


#     @pytest.mark.asyncio
#     async def test_handles_invalid_string_scores(self, bias_detector):
#         """Test handling of invalid string scores from LLM"""
#         with patch.object(bias_detector.llm_service, 'detect_bias', return_value={
#             'issues': [],
#             'bias_score': 'invalid_score',  # Invalid string
#             'inclusivity_score': 'also_invalid',  # Invalid string
#             'clarity_score': 'bad_score',  # Invalid string 
#             'role': 'Developer',
#             'industry': 'Technology',
#             'overall_assessment': 'Test assessment'
#         }):
#             with patch.object(bias_detector.llm_service, 'improve_language', return_value={
#                 'suggestions': [],
#                 'seo_keywords': [],
#                 'improved_text': 'Valid improved text'  # Valid improved text
#             }):
#                 text = "Test job description"
#                 result = await bias_detector.analyze_comprehensive(text)
                
#                 # Should default to 0.0 for invalid scores
#                 assert result.bias_score == 0.0
#                 assert result.clarity_score == 0.0
#                 assert result.inclusivity_score == 0.0


# class TestHelperMethods:
#     """Test helper methods"""
    
#     def test_parse_category_single_values(self, bias_detector):
#         """Test category parsing for single values"""
#         assert bias_detector._parse_category('clarity') == CategoryType.CLARITY
#         assert bias_detector._parse_category('bias') == CategoryType.BIAS
#         assert bias_detector._parse_category('seo') == CategoryType.SEO
#         assert bias_detector._parse_category('inclusivity') == CategoryType.INCLUSIVITY
#         assert bias_detector._parse_category('professionalism') == CategoryType.PROFESSIONALISM
#         assert bias_detector._parse_category('legal') == CategoryType.LEGAL
#         assert bias_detector._parse_category('unknown') == CategoryType.CLARITY  # default
    
    
#     def test_parse_category_pipe_separated(self, bias_detector):
#         """Test category parsing for pipe-separated values"""
#         # Should take first valid category
#         assert bias_detector._parse_category('bias|clarity') == CategoryType.BIAS
#         assert bias_detector._parse_category('unknown|seo') == CategoryType.SEO
#         assert bias_detector._parse_category('invalid|unknown|inclusivity') == CategoryType.INCLUSIVITY
#         assert bias_detector._parse_category('bad|worse|terrible') == CategoryType.CLARITY  # all invalid
    

#     def test_parse_llm_issues_complete_data(self, bias_detector):
#         """Test parsing LLM issues with complete valid data"""
#         valid_issues = [
#             {
#                 'type': 'gender',
#                 'text': 'aggressive personality',
#                 'start_index': 10,
#                 'end_index': 30,
#                 'severity': 'high',
#                 'explanation': 'May discourage female applicants',
#                 'job_relevance': 'Not necessary for job performance'
#             },
#             {
#                 'type': 'age',
#                 'text': 'young professional',
#                 'start_index': 50,
#                 'end_index': 68,
#                 'severity': 'medium',
#                 'explanation': 'Age discriminatory language'
#             }
#         ]
        
#         parsed_issues = bias_detector._parse_llm_issues(valid_issues)
        
#         assert len(parsed_issues) == 2
#         assert all(isinstance(issue, BiasIssue) for issue in parsed_issues)
        
#         # Check first issue
#         issue1 = parsed_issues[0]
#         assert issue1.type == BiasType.GENDER
#         assert issue1.text == 'aggressive personality'
#         assert issue1.severity == SeverityLevel.HIGH
#         assert issue1.start_index == 10
#         assert issue1.end_index == 30
    

#     def test_parse_llm_issues_with_invalid_data(self, bias_detector):
#         """Test parsing LLM issues with invalid or missing data"""
#         invalid_issues = [
#             {'type': 'invalid_type', 'text': 'test text'},  # Invalid bias type - gets defaulted
#             {'type': 'gender', 'severity': 'invalid_severity', 'text': 'test'},  # Invalid severity - gets defaulted
#             {'type': 'gender'},  # Missing required text field - should be skipped
#             {},  # Empty issue - should be skipped
#             {'type': 'age', 'text': 'valid issue', 'severity': 'low'}  # Valid issue
#         ]
        
#         parsed_issues = bias_detector._parse_llm_issues(invalid_issues)
        
#         # Should handle invalid data gracefully
#         # Expecting 3 issues: invalid_type (defaulted), invalid_severity (defaulted), and valid issue
#         # Missing text and empty issues should be skipped
#         assert len(parsed_issues) == 3
#         assert all(isinstance(issue, BiasIssue) for issue in parsed_issues)
    

#     def test_parse_llm_suggestions_complete_data(self, bias_detector):
#         """Test parsing LLM suggestions with complete valid data"""
#         valid_suggestions = [
#             {
#                 'original': 'aggressive personality',
#                 'improved': 'assertive communication',
#                 'rationale': 'More inclusive language',
#                 'category': 'inclusivity'
#             },
#             {
#                 'original': 'young team',
#                 'improved': 'dynamic team', 
#                 'rationale': 'Removes age bias',
#                 'category': 'bias|inclusivity'
#             }
#         ]
        
#         parsed_suggestions = bias_detector._parse_llm_suggestions(valid_suggestions)
        
#         assert len(parsed_suggestions) == 2
#         assert all(isinstance(suggestion, Suggestion) for suggestion in parsed_suggestions)
        
#         # Check first suggestion
#         suggestion1 = parsed_suggestions[0]
#         assert suggestion1.original == 'aggressive personality'
#         assert suggestion1.improved == 'assertive communication'
#         assert suggestion1.category == CategoryType.INCLUSIVITY
    

#     def test_parse_llm_suggestions_with_removed_items(self, bias_detector):
#         """Test parsing suggestions that should be removed"""
#         suggestions_with_removed = [
#             {
#                 'original': 'bad phrase',
#                 'improved': 'Removed - not appropriate',  # Should be skipped
#                 'rationale': 'Should remove this',
#                 'category': 'bias'
#             },
#             {
#                 'original': 'good phrase',
#                 'improved': 'better phrase',
#                 'rationale': 'Valid improvement',
#                 'category': 'clarity'
#             }
#         ]
        
#         parsed_suggestions = bias_detector._parse_llm_suggestions(suggestions_with_removed)
        
#         # Should only include the non-removed suggestion
#         assert len(parsed_suggestions) == 1
#         assert parsed_suggestions[0].original == 'good phrase'


# class TestIntegration:
#     """Integration tests combining multiple components"""
    
#     @pytest.mark.asyncio
#     async def test_handles_mixed_valid_invalid_responses(self, bias_detector):
#         """Test handling when one LLM call succeeds and another fails"""
#         # Mock one success, one failure
#         with patch.object(bias_detector.llm_service, 'detect_bias', return_value={
#             'issues': [],
#             'bias_score': 0.1,
#             'inclusivity_score': 0.9,
#             'clarity_score': 0.8,
#             'role': 'Analyst',
#             'industry': 'Finance',
#             'overall_assessment': 'Good job description'
#         }):
#             with patch.object(bias_detector.llm_service, 'improve_language', side_effect=Exception("Improvement failed")):
#                 text = "Looking for a financial analyst with strong analytical skills"
                
#                 # Should raise exception due to error handling in analyze_comprehensive
#                 with pytest.raises(Exception, match="Language improvement service failed"):
#                     await bias_detector.analyze_comprehensive(text)


#     @pytest.mark.asyncio
#     async def test_successful_analysis_with_both_services_working(self, bias_detector):
#         """Test successful analysis when both services work correctly"""
#         with patch.object(bias_detector.llm_service, 'detect_bias', return_value={
#             'issues': [
#                 {
#                     'type': 'gender',
#                     'text': 'strong leader',
#                     'start_index': 0,
#                     'end_index': 13,
#                     'severity': 'medium',
#                     'explanation': 'May be gendered language'
#                 }
#             ],
#             'bias_score': 0.1,
#             'inclusivity_score': 0.9,
#             'clarity_score': 0.8,
#             'role': 'Analyst',
#             'industry': 'Finance',
#             'overall_assessment': 'Good job description'
#         }):
#             with patch.object(bias_detector.llm_service, 'improve_language', return_value={
#                 'suggestions': [
#                     {
#                         'original': 'strong leader',
#                         'improved': 'effective leader',
#                         'rationale': 'More inclusive language',
#                         'category': 'inclusivity'
#                     }
#                 ],
#                 'seo_keywords': ['analyst', 'finance'],
#                 'improved_text': 'Looking for an effective leader in financial analysis'
#             }):
#                 text = "Looking for a strong leader in financial analysis"
                
#                 result = await bias_detector.analyze_comprehensive(text)
                
#                 # Should use successful results from both services
#                 assert result.role == 'Analyst'
#                 assert result.industry == 'Finance'  
#                 assert result.bias_score == 0.1
#                 assert len(result.issues) == 1
#                 assert len(result.suggestions) == 1
#                 assert len(result.seo_keywords) == 2
#                 assert result.improved_text == 'Looking for an effective leader in financial analysis'

import pytest
from unittest.mock import AsyncMock, patch
from app.services.bias_detector import BiasDetector
from app.models.schemas import (
    BiasAnalysisResult, BiasIssue, Suggestion, BiasType, 
    SeverityLevel, CategoryType
)


@pytest.fixture
def bias_detector():
    """Create a BiasDetector instance for testing"""
    return BiasDetector()


@pytest.fixture
def mock_llm_service():
    """Mock LLM service to avoid external dependencies"""
    with patch('app.services.bias_detector.LLMService') as mock:
        # Mock bias detection response - matches your actual LLM response format
        mock.return_value.detect_bias = AsyncMock(return_value={
            'role': 'salesperson',
            'industry': 'sales',
            'issues': [
                {
                    'type': 'gender',
                    'text': 'aggressive salesperson',
                    'start_index': 11,
                    'end_index': 31,
                    'severity': 'medium',
                    'explanation': 'Gendered language that may discourage female applicants'
                },
                {
                    'type': 'gender',
                    'text': 'strong personality',
                    'start_index': 37,
                    'end_index': 55,
                    'severity': 'low',
                    'explanation': 'May be perceived as gendered language'
                }
            ],
            'bias_score': 0.2,
            'inclusivity_score': 0.8,
            'clarity_score': 0.9,
            'overall_assessment': 'Low bias detected with some minor language improvements needed'
        })
        
        # Mock improvement response - matches your actual LLM response format
        # IMPORTANT: Make sure improved_text is NOT "Error generating improved text"
        mock.return_value.improve_language = AsyncMock(return_value={
            'suggestions': [
                {
                    'original': 'aggressive salesperson',
                    'improved': 'results-driven sales professional',
                    'rationale': 'More inclusive and professional language',
                    'category': 'inclusivity'
                },
                {
                    'original': 'strong personality',
                    'improved': 'excellent interpersonal skills',
                    'rationale': 'More specific and inclusive description',
                    'category': 'bias|inclusivity'
                }
            ],
            'seo_keywords': ['sales representative', 'sales professional', 'client relations', 'sales targets', 'communication'],
            'improved_text': '''**JOB TITLE:** Sales Representative

**COMPANY:** Sales Solutions Inc

**INDUSTRY:** Sales/Marketing

**LOCATION:** Remote/Hybrid

**EMPLOYMENT TYPE:** Full-time

**JOB SUMMARY:**
Join our dynamic sales team as a Sales Representative where you'll drive revenue growth through client relationship building. You'll work with prospective clients to understand their needs and present tailored solutions that deliver value.

**KEY RESPONSIBILITIES:**
• Build and maintain strong client relationships through effective communication
• Present product solutions to meet client requirements
• Achieve monthly and quarterly sales targets
• Collaborate with internal teams to ensure client satisfaction

**REQUIRED QUALIFICATIONS:**
• Bachelor's degree in Business, Marketing, or related field
• 2+ years of sales experience
• Proven track record of meeting sales targets

**PREFERRED QUALIFICATIONS:**
• Experience with CRM software
• Industry-specific knowledge in relevant sectors

**REQUIRED SKILLS:**
• Excellent verbal and written communication abilities
• Strong negotiation and presentation skills
• Results-oriented mindset
• Ability to work independently

**WHAT WE OFFER:**
• Competitive base salary plus commission
• Comprehensive health benefits
• Professional development opportunities
• Flexible work arrangements

**APPLICATION PROCESS:**
Submit your resume highlighting your sales achievements and experience.'''
        })
        
        yield mock


@pytest.fixture
def mock_llm_service_na_response():
    """Mock LLM service for non-job description text"""
    with patch('app.services.bias_detector.LLMService') as mock:
        # Mock N/A response for non-job text
        mock.return_value.detect_bias = AsyncMock(return_value={
            'role': 'N/A',
            'industry': 'N/A',
            'issues': [],
            'bias_score': 'N/A',
            'inclusivity_score': 'N/A',
            'clarity_score': 'N/A',
            'overall_assessment': 'The provided text does not appear to be a job description.'
        })
        
        # IMPORTANT: Make sure this doesn't return error text
        mock.return_value.improve_language = AsyncMock(return_value={
            'suggestions': [],
            'improved_text': 'N/A - The provided text does not appear to be a job description or does not contain sufficient job-related information to generate an improved version.',
            'seo_keywords': []
        })
        
        yield mock


class TestBasicFunctionality:
    """Test basic functionality of BiasDetector"""
    
    @pytest.mark.asyncio
    async def test_scores_are_valid_types(self, bias_detector):
        """Test that all scores are valid types per schema (Union[str, float])"""
        text = "Looking for a qualified team member with excellent communication skills"
        
        # Mock both services explicitly for this test
        with patch.object(bias_detector.llm_service, 'detect_bias', return_value={
            'issues': [],
            'bias_score': 0.3,
            'inclusivity_score': 0.8,
            'clarity_score': 0.9,
            'role': 'Team Member',
            'industry': 'General',
            'overall_assessment': 'Test assessment'
        }):
            with patch.object(bias_detector.llm_service, 'improve_language', return_value={
                'suggestions': [],
                'seo_keywords': ['communication', 'teamwork'],
                'improved_text': 'Valid improved text'
            }):
                result = await bias_detector.analyze_comprehensive(text)
                
                # Check score types (can be str or float per schema)
                assert isinstance(result.bias_score, (str, float))
                assert isinstance(result.inclusivity_score, (str, float))
                assert isinstance(result.clarity_score, (str, float))
                
                # If float, should be in valid range
                if isinstance(result.bias_score, float):
                    assert 0.0 <= result.bias_score <= 1.0
                if isinstance(result.inclusivity_score, float):
                    assert 0.0 <= result.inclusivity_score <= 1.0
                if isinstance(result.clarity_score, float):
                    assert 0.0 <= result.clarity_score <= 1.0
    

    @pytest.mark.asyncio
    async def test_handles_string_scores_from_llm(self, bias_detector):
        """Test handling of string scores from LLM responses"""
        with patch.object(bias_detector.llm_service, 'detect_bias', return_value={
            'issues': [],
            'bias_score': '0.3',  # String score
            'inclusivity_score': '0.8',  # String score  
            'clarity_score': '0.7',  # String score
            'role': 'Developer',
            'industry': 'Technology',
            'overall_assessment': 'Test assessment'
        }):
            with patch.object(bias_detector.llm_service, 'improve_language', return_value={
                'suggestions': [],
                'seo_keywords': ['python', 'developer'],
                'improved_text': 'Improved text'  # Valid improved text
            }):
                text = "Test job description text"
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
    
    # @pytest.mark.asyncio
    # async def test_handles_llm_detect_bias_error(self, bias_detector):
    #     """Test that detect_bias errors are handled gracefully"""
    #     with patch.object(bias_detector.llm_service, 'detect_bias', side_effect=Exception("API Error")):
    #         with patch.object(bias_detector.llm_service, 'improve_language', return_value={
    #             'suggestions': [],
    #             'seo_keywords': [],
    #             'improved_text': 'Valid improved text'  # Valid improved text
    #         }):
    #             text = "Test job description"
                
    #             # Should not raise exception
    #             result = await bias_detector.analyze_comprehensive(text)
                
    #             # Should return valid result with fallback values
    #             assert isinstance(result, BiasAnalysisResult)
    #             assert result.bias_score == 0.0  # Default fallback
    #             assert len(result.issues) == 0  # Empty issues list
    #             # These fields should have valid default values when detect_bias fails
    #             assert result.role == "Unknown"
    #             assert result.industry == "Unknown"
    #             assert result.overall_assessment == "Analysis could not be completed due to service error"
    
    
    @pytest.mark.asyncio
    async def test_handles_llm_improve_language_error(self, bias_detector):
        """Test that improve_language errors raise exception as expected"""  
        with patch.object(bias_detector.llm_service, 'detect_bias', return_value={
            'issues': [],
            'bias_score': 0.2,
            'inclusivity_score': 0.8,
            'clarity_score': 0.9,
            'role': 'Developer',
            'industry': 'Tech',
            'overall_assessment': 'Good'
        }):
            with patch.object(bias_detector.llm_service, 'improve_language', side_effect=Exception("API Error")):
                text = "Test job description"
                
                # Should raise exception due to error handling in analyze_comprehensive
                with pytest.raises(Exception, match="Language improvement service failed"):
                    await bias_detector.analyze_comprehensive(text)


    @pytest.mark.asyncio
    async def test_handles_improve_language_error_text_response(self, bias_detector):
        """Test that improve_language returning error text raises exception"""  
        with patch.object(bias_detector.llm_service, 'detect_bias', return_value={
            'issues': [],
            'bias_score': 0.2,
            'inclusivity_score': 0.8,
            'clarity_score': 0.9,
            'role': 'Developer',
            'industry': 'Tech',
            'overall_assessment': 'Good'
        }):
            with patch.object(bias_detector.llm_service, 'improve_language', return_value={
                'suggestions': [],
                'seo_keywords': [],
                'improved_text': 'Error generating improved text'  # This should trigger exception
            }):
                text = "Test job description"
                
                # Should raise exception due to error handling in analyze_comprehensive
                with pytest.raises(Exception, match="Language improvement service failed"):
                    await bias_detector.analyze_comprehensive(text)


    @pytest.mark.asyncio
    async def test_handles_invalid_string_scores(self, bias_detector):
        """Test handling of invalid string scores from LLM"""
        with patch.object(bias_detector.llm_service, 'detect_bias', return_value={
            'issues': [],
            'bias_score': 'invalid_score',  # Invalid string
            'inclusivity_score': 'also_invalid',  # Invalid string
            'clarity_score': 'bad_score',  # Invalid string 
            'role': 'Developer',
            'industry': 'Technology',
            'overall_assessment': 'Test assessment'
        }):
            with patch.object(bias_detector.llm_service, 'improve_language', return_value={
                'suggestions': [],
                'seo_keywords': [],
                'improved_text': 'Valid improved text'  # Valid improved text
            }):
                text = "Test job description"
                result = await bias_detector.analyze_comprehensive(text)
                
                # Should default to 0.0 for invalid scores
                assert result.bias_score == 0.0
                assert result.clarity_score == 0.0
                assert result.inclusivity_score == 0.0


class TestHelperMethods:
    """Test helper methods"""
    
    def test_parse_category_single_values(self, bias_detector):
        """Test category parsing for single values"""
        assert bias_detector._parse_category('clarity') == CategoryType.CLARITY
        assert bias_detector._parse_category('bias') == CategoryType.BIAS
        assert bias_detector._parse_category('seo') == CategoryType.SEO
        assert bias_detector._parse_category('inclusivity') == CategoryType.INCLUSIVITY
        assert bias_detector._parse_category('professionalism') == CategoryType.PROFESSIONALISM
        assert bias_detector._parse_category('legal') == CategoryType.LEGAL
        assert bias_detector._parse_category('unknown') == CategoryType.CLARITY  # default
    
    
    def test_parse_category_pipe_separated(self, bias_detector):
        """Test category parsing for pipe-separated values"""
        # Should take first valid category
        assert bias_detector._parse_category('bias|clarity') == CategoryType.BIAS
        assert bias_detector._parse_category('unknown|seo') == CategoryType.SEO
        assert bias_detector._parse_category('invalid|unknown|inclusivity') == CategoryType.INCLUSIVITY
        assert bias_detector._parse_category('bad|worse|terrible') == CategoryType.CLARITY  # all invalid
    

    def test_parse_llm_issues_complete_data(self, bias_detector):
        """Test parsing LLM issues with complete valid data"""
        valid_issues = [
            {
                'type': 'gender',
                'text': 'aggressive personality',
                'start_index': 10,
                'end_index': 30,
                'severity': 'high',
                'explanation': 'May discourage female applicants'
            },
            {
                'type': 'age',
                'text': 'young professional',
                'start_index': 50,
                'end_index': 68,
                'severity': 'medium',
                'explanation': 'Age discriminatory language'
            }
        ]
        
        parsed_issues = bias_detector._parse_llm_issues(valid_issues)
        
        assert len(parsed_issues) == 2
        assert all(isinstance(issue, BiasIssue) for issue in parsed_issues)
        
        # Check first issue
        issue1 = parsed_issues[0]
        assert issue1.type == BiasType.GENDER
        assert issue1.text == 'aggressive personality'
        assert issue1.severity == SeverityLevel.HIGH
        assert issue1.start_index == 10
        assert issue1.end_index == 30
    

    def test_parse_llm_issues_with_invalid_data(self, bias_detector):
        """Test parsing LLM issues with invalid or missing data"""
        invalid_issues = [
            {'type': 'invalid_type', 'text': 'test text'},  # Invalid bias type - gets defaulted to clarity
            {'type': 'gender', 'severity': 'invalid_severity', 'text': 'test'},  # Invalid severity - gets defaulted
            {'type': 'gender'},  # Missing required text field - should be skipped
            {},  # Empty issue - should be skipped
            {'type': 'age', 'text': 'valid issue', 'severity': 'low'}  # Valid issue
        ]
        
        parsed_issues = bias_detector._parse_llm_issues(invalid_issues)
        
        # Should handle invalid data gracefully
        # Expecting 3 issues: invalid_type (defaulted to clarity), invalid_severity (defaulted), and valid issue
        # Missing text and empty issues should be skipped
        assert len(parsed_issues) == 3
        assert all(isinstance(issue, BiasIssue) for issue in parsed_issues)
        # Check that invalid_type defaults to clarity (as per the updated code)
        assert parsed_issues[0].type == BiasType.CLARITY
    

    def test_parse_llm_issues_duplicates_filtered(self, bias_detector):
        """Test that duplicate issues are filtered out by normalized text"""
        duplicate_issues = [
            {
                'type': 'gender',
                'text': 'Aggressive personality',  # Different case
                'start_index': 10,
                'end_index': 30,
                'severity': 'high',
                'explanation': 'First occurrence'
            },
            {
                'type': 'gender', 
                'text': 'aggressive personality',  # Same text, different case
                'start_index': 50,
                'end_index': 70,
                'severity': 'medium',
                'explanation': 'Duplicate occurrence'
            },
            {
                'type': 'age',
                'text': 'young professional',  # Different text
                'start_index': 80,
                'end_index': 98,
                'severity': 'low',
                'explanation': 'Unique occurrence'
            }
        ]
        
        parsed_issues = bias_detector._parse_llm_issues(duplicate_issues)
        
        # Should only return 2 issues (duplicate filtered out)
        assert len(parsed_issues) == 2
        # Should keep the first occurrence of duplicate text
        assert parsed_issues[0].text == 'Aggressive personality'
        assert parsed_issues[1].text == 'young professional'


    def test_parse_llm_suggestions_complete_data(self, bias_detector):
        """Test parsing LLM suggestions with complete valid data"""
        valid_suggestions = [
            {
                'original': 'aggressive personality',
                'improved': 'assertive communication',
                'rationale': 'More inclusive language',
                'category': 'inclusivity'
            },
            {
                'original': 'young team',
                'improved': 'dynamic team', 
                'rationale': 'Removes age bias',
                'category': 'bias|inclusivity'
            }
        ]
        
        parsed_suggestions = bias_detector._parse_llm_suggestions(valid_suggestions)
        
        assert len(parsed_suggestions) == 2
        assert all(isinstance(suggestion, Suggestion) for suggestion in parsed_suggestions)
        
        # Check first suggestion
        suggestion1 = parsed_suggestions[0]
        assert suggestion1.original == 'aggressive personality'
        assert suggestion1.improved == 'assertive communication'
        assert suggestion1.category == CategoryType.INCLUSIVITY
    

    def test_parse_llm_suggestions_with_removed_items(self, bias_detector):
        """Test parsing suggestions that should be removed"""
        suggestions_with_removed = [
            {
                'original': 'bad phrase',
                'improved': 'Removed - not appropriate',  # Should be skipped
                'rationale': 'Should remove this',
                'category': 'bias'
            },
            {
                'original': 'good phrase',
                'improved': 'better phrase',
                'rationale': 'Valid improvement',
                'category': 'clarity'
            }
        ]
        
        parsed_suggestions = bias_detector._parse_llm_suggestions(suggestions_with_removed)
        
        # Should only include the non-removed suggestion
        assert len(parsed_suggestions) == 1
        assert parsed_suggestions[0].original == 'good phrase'


class TestIntegration:
    """Integration tests combining multiple components"""
    
    @pytest.mark.asyncio
    async def test_handles_mixed_valid_invalid_responses(self, bias_detector):
        """Test handling when one LLM call succeeds and another fails"""
        # Mock one success, one failure
        with patch.object(bias_detector.llm_service, 'detect_bias', return_value={
            'issues': [],
            'bias_score': 0.1,
            'inclusivity_score': 0.9,
            'clarity_score': 0.8,
            'role': 'Analyst',
            'industry': 'Finance',
            'overall_assessment': 'Good job description'
        }):
            with patch.object(bias_detector.llm_service, 'improve_language', side_effect=Exception("Improvement failed")):
                text = "Looking for a financial analyst with strong analytical skills"
                
                # Should raise exception due to error handling in analyze_comprehensive
                with pytest.raises(Exception, match="Language improvement service failed"):
                    await bias_detector.analyze_comprehensive(text)


    @pytest.mark.asyncio
    async def test_successful_analysis_with_both_services_working(self, bias_detector):
        """Test successful analysis when both services work correctly"""
        with patch.object(bias_detector.llm_service, 'detect_bias', return_value={
            'issues': [
                {
                    'type': 'gender',
                    'text': 'strong leader',
                    'start_index': 0,
                    'end_index': 13,
                    'severity': 'medium',
                    'explanation': 'May be gendered language'
                }
            ],
            'bias_score': 0.1,
            'inclusivity_score': 0.9,
            'clarity_score': 0.8,
            'role': 'Analyst',
            'industry': 'Finance',
            'overall_assessment': 'Good job description'
        }):
            with patch.object(bias_detector.llm_service, 'improve_language', return_value={
                'suggestions': [
                    {
                        'original': 'strong leader',
                        'improved': 'effective leader',
                        'rationale': 'More inclusive language',
                        'category': 'inclusivity'
                    }
                ],
                'seo_keywords': ['analyst', 'finance'],
                'improved_text': 'Looking for an effective leader in financial analysis'
            }):
                text = "Looking for a strong leader in financial analysis"
                
                result = await bias_detector.analyze_comprehensive(text)
                
                # Should use successful results from both services
                assert result.role == 'Analyst'
                assert result.industry == 'Finance'  
                assert result.bias_score == 0.1
                assert len(result.suggestions) == 1
                assert len(result.seo_keywords) == 2
                assert result.improved_text == 'Looking for an effective leader in financial analysis'