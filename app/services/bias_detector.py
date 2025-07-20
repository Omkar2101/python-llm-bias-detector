
import re
from typing import List, Dict, Tuple
from app.models.schemas import BiasIssue, Suggestion, BiasType, SeverityLevel, CategoryType, BiasAnalysisResult
from app.services.llm_service import LLMService
import textstat

class BiasDetector:
    def __init__(self):
        self.llm_service = LLMService()
        
        # Predefined bias patterns (as fallback to LLM)
        # self.gender_coded_words = {
        #     'masculine': ['aggressive', 'ambitious', 'assertive', 'competitive', 'confident', 
        #                  'decisive', 'determined', 'dominant', 'independent', 'leader',
        #                  'outspoken', 'self-reliant', 'strong', 'superior'],
        #     'feminine': ['collaborative', 'cooperative', 'dependable', 'honest', 
        #                 'interpersonal', 'loyal', 'pleasant', 'polite', 'quiet',
        #                 'responsible', 'supportive', 'sympathetic', 'team player', 'trustworthy']
        # }
        
        # self.problematic_phrases = {
        #     'gender_bias': [
        #         'male preferred', 'females need not apply', 'masculine presence',
        #         'male salesperson', 'female salesperson', 'guys', 'brotherhood',
        #         'male', 'female', 'masculine', 'feminine'
        #     ],
        #     'race_bias': [
        #         'european descent', 'caucasian background', 'classic american look',
        #         'white clientele', 'traditional appearance'
        #     ],
        #     'age_bias': [
        #         'young and energetic', 'recent graduate', 'digital native',
        #         'fresh thinking', 'up-and-coming', 'mature', 'experienced professional',
        #         'young', 'energetic', 'graduates', 'recent grad'
        #     ],
        #     'cultural_bias': [
        #         'native english speaker', 'american accent', 'u.s.-born',
        #         'cultural fit', 'traditional values', 'western european'
        #     ],
        #     'religious_bias': [
        #         'no accommodations', 'religious attire', 'christian values'
        #     ],
        #     'educational_bias': [
        #         'ivy league', 'top-tier schools', 'elite university'
        #     ]
        # }
    
    async def analyze_comprehensive(self, text: str) -> BiasAnalysisResult:
        print(f"Analyzing text: {text[:100]}...")  # Debug log
        """Comprehensive bias analysis using both LLM and rule-based detection"""
        
        try:
            # Get LLM analysis for bias detection
            llm_bias_result = await self.llm_service.detect_bias(text)
            
            print(f"LLM bias result: {llm_bias_result}")  # Debug log

            
        except Exception as e:
            print(f"Error in LLM bias detection: {e}")
            llm_bias_result = {'issues': [], 'bias_score': 0.5}
        
        try:
            # Get LLM analysis for language improvement
            llm_improvement_result = await self.llm_service.improve_language(text)
            print(f"LLM improve result: {llm_improvement_result}")  # Debug log
        except Exception as e:
            print(f"Error in LLM improvement: {e}")
            llm_improvement_result = {
                'suggestions': [], 
                'clarity_score': 0.0, 
                'inclusivity_score': 0.0,
                'seo_keywords': [],
                'improved_text': None
            }
        
        # Combine rule-based and LLM results
        all_issues = self._parse_llm_issues(llm_bias_result.get('issues', []))
        # rule_based_issues = self._detect_rule_based_bias(text)
        # all_issues.extend(rule_based_issues)
        
        # Parse suggestions
        suggestions = self._parse_llm_suggestions(llm_improvement_result.get('suggestions', []))
        
        # Calculate scores
        # bias_score = llm_bias_result.get('bias_score')
           # Calculate scores - HANDLE STRING TO FLOAT CONVERSION
        bias_score = llm_bias_result.get('bias_score')
        if isinstance(bias_score, str):
            try:
                bias_score = float(bias_score)
            except (ValueError, TypeError):
                bias_score = 0.0

        # clarity_score = llm_improvement_result.get( self._calculate_clarity_score(text))
        clarity_score = llm_improvement_result.get('clarity_score')
        if isinstance(clarity_score, str):
            try:
                clarity_score = float(clarity_score)
            except (ValueError, TypeError):
                clarity_score = 0.0

        
        # inclusivity_score = llm_improvement_result.get( self._calculate_inclusivity_score(text))
        inclusivity_score = llm_improvement_result.get('inclusivity_score')
        if isinstance(inclusivity_score, str):
            try:
                inclusivity_score = float(inclusivity_score)
            except (ValueError, TypeError):
                inclusivity_score = 0.0

        #Get the role 
        role = llm_bias_result.get('role')

        #Get he Industry
        industry = llm_bias_result.get('industry')
        # Get overall assessment
        overall_assessment = llm_bias_result.get('overall_assessment')
        # print(f"overall_assessment: {overall_assessment}")
      
        
        result=BiasAnalysisResult(
            role=role,
            industry=industry,
            bias_score=bias_score,
            inclusivity_score=inclusivity_score,
            clarity_score=clarity_score,
            issues=all_issues,
            suggestions=suggestions,
            seo_keywords=llm_improvement_result.get('seo_keywords', []),
            improved_text=llm_improvement_result.get('improved_text'),
            overall_assessment=llm_bias_result.get('overall_assessment')
        )

        print(f"Final result before return: {result}")  # Debug log
        return result
    
    def _parse_llm_issues(self, llm_issues: List[Dict]) -> List[BiasIssue]:
        """Parse LLM bias issues into BiasIssue objects"""
        issues = []
        for issue in llm_issues:
            try:
                # Validate required fields
                if not issue.get('type') or not issue.get('text'):
                    print(f"Skipping incomplete issue: {issue}")
                    continue
                
                # Handle BiasType validation
                bias_type_str = issue.get('type', 'gender').lower()
                try:
                    bias_type = BiasType(bias_type_str)
                except ValueError:
                    print(f"Unknown bias type '{bias_type_str}', defaulting to gender")
                    bias_type = BiasType.GENDER
                
                # Handle SeverityLevel validation
                severity_str = issue.get('severity', 'medium').lower()
                try:
                    severity = SeverityLevel(severity_str)
                except ValueError:
                    print(f"Unknown severity '{severity_str}', defaulting to medium")
                    severity = SeverityLevel.MEDIUM
                
                bias_issue = BiasIssue(
                    type=bias_type,
                    text=issue.get('text', ''),
                    start_index=issue.get('start_index', 0),
                    end_index=issue.get('end_index', 0),
                    severity=severity,
                    explanation=issue.get('explanation', '')
                )
                issues.append(bias_issue)
            except Exception as e:
                print(f"Error parsing LLM issue: {e}")
                print(f"Problematic issue: {issue}")
                continue
        return issues
    
    def _parse_llm_suggestions(self, llm_suggestions: List[Dict]) -> List[Suggestion]:
        """Parse LLM suggestions into Suggestion objects"""
        suggestions = []
        for suggestion in llm_suggestions:
            try:
                # Handle pipe-separated categories - take the first valid one
                category_str = suggestion.get('category', 'clarity')
                category = self._parse_category(category_str)
                
                # Skip suggestions marked as "Removed"
                improved_text = suggestion.get('improved', '')
                if improved_text.lower().startswith('removed'):
                    continue
                
                suggestion_obj = Suggestion(
                    original=suggestion.get('original', ''),
                    improved=improved_text,
                    rationale=suggestion.get('rationale', ''),
                    category=category
                )
                suggestions.append(suggestion_obj)
            except Exception as e:
                print(f"Error parsing LLM suggestion: {e}")
                print(f"Problematic suggestion: {suggestion}")
                continue
        return suggestions
    
    def _parse_category(self, category_str: str) -> CategoryType:
        """Parse category string, handling pipe-separated values"""
        if not category_str:
            return CategoryType.CLARITY
        
        # Split by pipe and try each category
        categories = [cat.strip().lower() for cat in category_str.split('|')]
        
        for cat in categories:
            try:
                return CategoryType(cat)
            except ValueError:
                continue
        
        # If none match, default to clarity
        print(f"No valid category found in '{category_str}', defaulting to clarity")
        return CategoryType.CLARITY
    
    # def _detect_rule_based_bias(self, text: str) -> List[BiasIssue]:
    #     """Rule-based bias detection as fallback/supplement to LLM"""
    #     issues = []
    #     text_lower = text.lower()
        
    #     # Check for gender-coded words
    #     for category, words in self.gender_coded_words.items():
    #         for word in words:
    #             if word in text_lower:
    #                 start_idx = text_lower.find(word)
    #                 issues.append(BiasIssue(
    #                     type=BiasType.GENDER,
    #                     text=word,
    #                     start_index=start_idx,
    #                     end_index=start_idx + len(word),
    #                     severity=SeverityLevel.MEDIUM,
    #                     explanation=f"'{word}' is {category}-coded language that may discourage diverse applicants"
    #                 ))
        
    #     # Check for other problematic phrases
    #     for bias_category, phrases in self.problematic_phrases.items():
    #         for phrase in phrases:
    #             if phrase in text_lower:
    #                 start_idx = text_lower.find(phrase)
    #                 bias_type = self._map_category_to_bias_type(bias_category)
    #                 severity = SeverityLevel.HIGH if 'need not apply' in phrase else SeverityLevel.MEDIUM
                    
    #                 issues.append(BiasIssue(
    #                     type=bias_type,
    #                     text=phrase,
    #                     start_index=start_idx,
    #                     end_index=start_idx + len(phrase),
    #                     severity=severity,
    #                     explanation=f"'{phrase}' indicates {bias_category.replace('_', ' ')} and may be discriminatory"
    #                 ))
        
    #     return issues
    
    # def _map_category_to_bias_type(self, category: str) -> BiasType:
    #     mapping = {
    #         'gender_bias': BiasType.GENDER,
    #         'race_bias': BiasType.RACIAL,
    #         'age_bias': BiasType.AGE,
    #         'cultural_bias': BiasType.CULTURAL,
    #         'religious_bias': BiasType.RELIGIOUS,
    #         'educational_bias': BiasType.SOCIOECONOMIC
    #     }
    #     return mapping.get(category, BiasType.GENDER)
        
   
    