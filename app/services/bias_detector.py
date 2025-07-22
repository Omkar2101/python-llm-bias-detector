
import re
from typing import List, Dict, Tuple
from app.models.schemas import BiasIssue, Suggestion, BiasType, SeverityLevel, CategoryType, BiasAnalysisResult
from app.services.llm_service import LLMService
import textstat

class BiasDetector:
    def __init__(self):
        self.llm_service = LLMService()
        
       
    
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
            # print(f"LLM improve result: {llm_improvement_result}")  # Debug log
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
        clarity_score = llm_bias_result.get('clarity_score')
        if isinstance(clarity_score, str):
            try:
                clarity_score = float(clarity_score)
            except (ValueError, TypeError):
                clarity_score = 0.0

        
        # inclusivity_score = llm_improvement_result.get( self._calculate_inclusivity_score(text))
        inclusivity_score = llm_bias_result.get('inclusivity_score')
        if isinstance(inclusivity_score, str):
            try:
                inclusivity_score = float(inclusivity_score)
            except (ValueError, TypeError):
                inclusivity_score = 0.0

        #Get the role 
        role = llm_bias_result.get('role')

        original_text = llm_bias_result.get('original_text', text)
        #Get he Industry
        industry = llm_bias_result.get('industry')
        # Get overall assessment
        overall_assessment = llm_bias_result.get('overall_assessment')
        # print(f"overall_assessment: {overall_assessment}")
      
        
        result=BiasAnalysisResult(
            original_text=original_text,
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
    
    
        
   
    