# tests/evaluation/practical_usage_examples.py

import pytest
import asyncio
from typing import Dict, List, Union
import json
from datetime import datetime
import os
import sys

# Add the parent directory to sys.path to import from app (same as test_model_evaluation.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.services.llm_service import LLMService
from app.services.bias_detector import BiasDetector
# from tests.test_data.test_cases import ALL_TEST_CASES, EASY_CASES, MEDIUM_CASES, HARD_CASES, RealTestCase
from tests.test_data.realistic_test_cases import (
    ALL_REALISTIC_CASES, RealTestCase
)

class SimpleModelEvaluator:
    def __init__(self):
        self.llm_service = LLMService()
        self.bias_detector = BiasDetector()
        self.results = []
        
    def calculate_score_accuracy(self, expected: float, actual: Union[str, float], tolerance: float = 0.5) -> bool:
        """Check if the actual score is within tolerance of expected score"""
        # Handle N/A responses for non-job descriptions
        if actual == "N/A" and expected == 0.0:
            return True
        if actual == "N/A" or isinstance(actual, str):
            return False
        return abs(expected - actual) <= tolerance
    
    def calculate_score_difference(self, expected: float, actual: Union[str, float]) -> float:
        """Calculate absolute difference between expected and actual scores"""
        # Handle N/A responses
        if actual == "N/A" or isinstance(actual, str):
            return float('inf') if expected != 0.0 else 0.0
        return abs(expected - actual)
    
    def calculate_classification_metrics(self, individual_results: List[Dict]) -> Dict:
        """Calculate precision, recall, and F1 score for bias detection"""
        true_positives = 0
        false_positives = 0
        true_negatives = 0
        false_negatives = 0
        
        for result in individual_results:
            if 'error' in result:
                continue
                
            # Determine if bias was expected (based on expected_bias_score > 0)
            expected_has_bias = result['expected_scores']['bias_score'] > 0
            
            # Determine if bias was detected (based on actual_bias_score > 0)
            actual_bias_score = result['actual_scores']['bias_score']
            if actual_bias_score == "N/A":
                predicted_has_bias = False
            else:
                predicted_has_bias = actual_bias_score > 0
            
            # Calculate confusion matrix
            if expected_has_bias and predicted_has_bias:
                true_positives += 1
            elif not expected_has_bias and predicted_has_bias:
                false_positives += 1
            elif not expected_has_bias and not predicted_has_bias:
                true_negatives += 1
            elif expected_has_bias and not predicted_has_bias:
                false_negatives += 1
        
        # Calculate metrics
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        accuracy = (true_positives + true_negatives) / (true_positives + false_positives + true_negatives + false_negatives) if (true_positives + false_positives + true_negatives + false_negatives) > 0 else 0
        
        return {
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'accuracy': accuracy,
            'true_positives': true_positives,
            'false_positives': false_positives,
            'true_negatives': true_negatives,
            'false_negatives': false_negatives,
            'total_cases': true_positives + false_positives + true_negatives + false_negatives
        }
    
    async def evaluate_single_case(self, test_case: RealTestCase) -> Dict:
        """Evaluate a single test case"""
        try:
            # Get the actual result from your bias detector
            result = await self.bias_detector.analyze_comprehensive(test_case.job_description)
            
            # Handle N/A responses (non-job descriptions)
            if result.bias_score == "N/A":
                evaluation_result = {
                    'test_case_id': test_case.id,
                    'test_case_name': test_case.name,
                    'difficulty_level': test_case.difficulty_level,
                    'description': test_case.description,
                    'industry': test_case.industry,
                    'role_level': test_case.role_level,
                    'expected_scores': {
                        'bias_score': test_case.expected_bias_score,
                        'inclusivity_score': test_case.expected_inclusivity_score,
                        'clarity_score': test_case.expected_clarity_score,
                        'issues_count': test_case.expected_issues_count
                    },
                    'actual_scores': {
                        'bias_score': "N/A",
                        'inclusivity_score': "N/A",
                        'clarity_score': "N/A",
                        'issues_count': 0
                    },
                    'score_differences': {
                        'bias_diff': float('inf'),
                        'inclusivity_diff': float('inf'),
                        'clarity_diff': float('inf')
                    },
                    'accuracy_flags': {
                        'bias_score_accurate': False,
                        'inclusivity_score_accurate': False,
                        'clarity_score_accurate': False,
                        'issues_count_accurate': False,
                        'expected_types_found': False
                    },
                    'detected_issues': [],
                    'overall_assessment': result.overall_assessment,
                    'passed': False,
                    'note': 'Detected as non-job description'
                }
                return evaluation_result
            
            # Calculate accuracies for job descriptions
            bias_score_accurate = self.calculate_score_accuracy(
                test_case.expected_bias_score, 
                result.bias_score
            )
            
            inclusivity_score_accurate = self.calculate_score_accuracy(
                test_case.expected_inclusivity_score, 
                result.inclusivity_score
            )
            
            clarity_score_accurate = self.calculate_score_accuracy(
                test_case.expected_clarity_score, 
                result.clarity_score
            )
            
            # Calculate differences
            bias_diff = self.calculate_score_difference(
                test_case.expected_bias_score, 
                result.bias_score
            )
            
            inclusivity_diff = self.calculate_score_difference(
                test_case.expected_inclusivity_score, 
                result.inclusivity_score
            )
            
            clarity_diff = self.calculate_score_difference(
                test_case.expected_clarity_score, 
                result.clarity_score
            )
            
            # Check if detected issues count is reasonable
            issues_count_accurate = abs(len(result.issues) - test_case.expected_issues_count) <= 4
            
            # Check if expected bias types are detected
            detected_bias_types = [issue.type.value for issue in result.issues]
            expected_types_found = all(
                bias_type in detected_bias_types 
                for bias_type in test_case.expected_bias_types
            )
            
            evaluation_result = {
                'test_case_id': test_case.id,
                'test_case_name': test_case.name,
                'difficulty_level': test_case.difficulty_level,
                'description': test_case.description,
                'industry': test_case.industry,
                'role_level': test_case.role_level,
                'expected_bias_types': test_case.expected_bias_types,
                'expected_severity_levels': test_case.expected_severity_levels,
                'expected_scores': {
                    'bias_score': test_case.expected_bias_score,
                    'inclusivity_score': test_case.expected_inclusivity_score,
                    'clarity_score': test_case.expected_clarity_score,
                    'issues_count': test_case.expected_issues_count
                },
                'actual_scores': {
                    'bias_score': result.bias_score,
                    'inclusivity_score': result.inclusivity_score,
                    'clarity_score': result.clarity_score,
                    'issues_count': len(result.issues)
                },
                'score_differences': {
                    'bias_diff': bias_diff,
                    'inclusivity_diff': inclusivity_diff,
                    'clarity_diff': clarity_diff
                },
                'accuracy_flags': {
                    'bias_score_accurate': bias_score_accurate,
                    'inclusivity_score_accurate': inclusivity_score_accurate,
                    'clarity_score_accurate': clarity_score_accurate,
                    'issues_count_accurate': issues_count_accurate,
                    'expected_types_found': expected_types_found
                },
                'detected_issues': [
                    {
                        'type': issue.type.value,
                        'text': issue.text,
                        'severity': issue.severity.value,
                        'explanation': issue.explanation,
                        'start_index': issue.start_index,
                        'end_index': issue.end_index
                    } for issue in result.issues
                ],
                'overall_assessment': result.overall_assessment,
                'passed': all([
                    bias_score_accurate,
                    inclusivity_score_accurate,
                    clarity_score_accurate,
                    issues_count_accurate
                ])
            }
            
            return evaluation_result
            
        except Exception as e:
            print(f"Error in test case {test_case.id}: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'test_case_id': test_case.id,
                'test_case_name': test_case.name,
                'error': str(e),
                'passed': False
            }
    
    async def evaluate_all_cases(self, test_cases: List[RealTestCase] = None) -> Dict:
        """Evaluate all test cases or a subset"""
        # Fixed: Add default value assignment
        if test_cases is None:
            test_cases = ALL_REALISTIC_CASES
        
        print(f"Evaluating {len(test_cases)} test cases...")
        
        results = []
        for i, test_case in enumerate(test_cases):
            print(f"Evaluating {i+1}/{len(test_cases)}: {test_case.name}")
            result = await self.evaluate_single_case(test_case)
            results.append(result)
            
            # Add small delay to avoid rate limiting
            await asyncio.sleep(1)
        
        # Calculate overall statistics
        successful_results = [r for r in results if 'error' not in r]
        passed_results = [r for r in successful_results if r['passed']]
        
        # Calculate score differences only for successful results with numeric scores
        valid_results = [r for r in successful_results 
                        if isinstance(r.get('score_differences', {}).get('bias_diff'), (int, float))]
        
        # Calculate classification metrics
        classification_metrics = self.calculate_classification_metrics(successful_results)
        
        overall_stats = {
            'total_cases': len(test_cases),
            'successful_evaluations': len(successful_results),
            'passed_cases': len(passed_results),
            'pass_rate': len(passed_results) / len(successful_results) if successful_results else 0,
            'avg_bias_score_diff': sum(r['score_differences']['bias_diff'] for r in valid_results) / len(valid_results) if valid_results else 0,
            'avg_inclusivity_score_diff': sum(r['score_differences']['inclusivity_diff'] for r in valid_results) / len(valid_results) if valid_results else 0,
            'avg_clarity_score_diff': sum(r['score_differences']['clarity_diff'] for r in valid_results) / len(valid_results) if valid_results else 0,
        }
        
        # Group results by difficulty
        difficulty_stats = {}
        for difficulty in ['easy', 'medium', 'hard']:
            difficulty_results = [r for r in successful_results if r['difficulty_level'] == difficulty]
            if difficulty_results:
                difficulty_passed = [r for r in difficulty_results if r['passed']]
                difficulty_classification_metrics = self.calculate_classification_metrics(difficulty_results)
                difficulty_stats[difficulty] = {
                    'total': len(difficulty_results),
                    'passed': len(difficulty_passed),
                    'pass_rate': len(difficulty_passed) / len(difficulty_results),
                    'classification_metrics': difficulty_classification_metrics
                }
        
        # Group results by industry for additional insights
        industry_stats = {}
        industries = set(r.get('industry', 'unknown') for r in successful_results)
        for industry in industries:
            industry_results = [r for r in successful_results if r.get('industry') == industry]
            if industry_results:
                industry_passed = [r for r in industry_results if r['passed']]
                industry_stats[industry] = {
                    'total': len(industry_results),
                    'passed': len(industry_passed),
                    'pass_rate': len(industry_passed) / len(industry_results)
                }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'overall_stats': overall_stats,
            'classification_metrics': classification_metrics,
            'difficulty_stats': difficulty_stats,
            'industry_stats': industry_stats,
            'individual_results': results
        }
    
    def save_results(self, results: Dict, filename: str = None):
        """Save evaluation results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"practical_evaluation_results_{timestamp}.json"
        
        # Create results directory in the same folder as this script
        results_dir = os.path.join(os.path.dirname(__file__), 'practical_results')
        os.makedirs(results_dir, exist_ok=True)
        
        filepath = os.path.join(results_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"Results saved to: {filepath}")
        return filepath
    
    def print_summary(self, results: Dict):
        """Print a summary of the evaluation results"""
        stats = results['overall_stats']
        classification_metrics = results['classification_metrics']
        
        print("\n" + "="*50)
        print("PRACTICAL BIAS DETECTION EVALUATION SUMMARY")
        print("="*50)
        
        print(f"Total Test Cases: {stats['total_cases']}")
        print(f"Successfully Evaluated: {stats['successful_evaluations']}")
        print(f"Passed Cases: {stats['passed_cases']}")
        print(f"Overall Pass Rate: {stats['pass_rate']:.2%}")
        
        print(f"\nAverage Score Differences:")
        print(f"  Bias Score: {stats['avg_bias_score_diff']:.3f}")
        print(f"  Inclusivity Score: {stats['avg_inclusivity_score_diff']:.3f}")
        print(f"  Clarity Score: {stats['avg_clarity_score_diff']:.3f}")
        
        print(f"\nClassification Metrics:")
        print(f"  Precision: {classification_metrics['precision']:.3f}")
        print(f"  Recall: {classification_metrics['recall']:.3f}")
        print(f"  F1 Score: {classification_metrics['f1_score']:.3f}")
        print(f"  Accuracy: {classification_metrics['accuracy']:.3f}")
        print(f"  True Positives: {classification_metrics['true_positives']}")
        print(f"  False Positives: {classification_metrics['false_positives']}")
        print(f"  True Negatives: {classification_metrics['true_negatives']}")
        print(f"  False Negatives: {classification_metrics['false_negatives']}")
        
        print(f"\nResults by Difficulty:")
        for difficulty, diff_stats in results['difficulty_stats'].items():
            diff_metrics = diff_stats['classification_metrics']
            print(f"  {difficulty.upper()}: {diff_stats['passed']}/{diff_stats['total']} ({diff_stats['pass_rate']:.2%})")
            print(f"    F1 Score: {diff_metrics['f1_score']:.3f}, Precision: {diff_metrics['precision']:.3f}, Recall: {diff_metrics['recall']:.3f}")
        
        print(f"\nResults by Industry:")
        for industry, industry_stats in results['industry_stats'].items():
            print(f"  {industry.upper()}: {industry_stats['passed']}/{industry_stats['total']} ({industry_stats['pass_rate']:.2%})")

class SimpleModelTester:
    """Simple helper class for testing model performance"""
    
    def __init__(self):
        self.evaluator = SimpleModelEvaluator()

# Main evaluation function for all realistic test cases
async def evaluate_all_realistic_cases():
    """
    Comprehensive evaluation function that tests all realistic cases 
    (easy, medium, hard, and edge cases) and generates a single JSON report
    """
    print("🚀 Starting Comprehensive Realistic Test Case Evaluation...")
    print("="*60)
    
    evaluator = SimpleModelEvaluator()
    
    # Evaluate all realistic test cases
    results = await evaluator.evaluate_all_cases(ALL_REALISTIC_CASES)
    
    # Print comprehensive summary
    evaluator.print_summary(results)
    
    # Save results with descriptive filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"comprehensive_realistic_evaluation_{timestamp}.json"
    filepath = evaluator.save_results(results, filename)
    
    print(f"\n✅ Comprehensive evaluation completed!")
    print(f"📁 Results saved to: {filepath}")
    print(f"📊 Total cases evaluated: {results['overall_stats']['total_cases']}")
    print(f"🎯 Overall pass rate: {results['overall_stats']['pass_rate']:.2%}")
    print(f"📈 F1 Score: {results['classification_metrics']['f1_score']:.3f}")
    
    return results

# Pytest test functions
@pytest.mark.asyncio
async def test_comprehensive_realistic_evaluation():
    """Pytest version of comprehensive realistic test evaluation"""
    print("🚀 Running Comprehensive Realistic Test Cases...")
    
    results = await evaluate_all_realistic_cases()
    
    # Assert minimum performance thresholds
    assert results['overall_stats']['pass_rate'] >= 0.4, f"Overall pass rate too low: {results['overall_stats']['pass_rate']:.2%}"
    assert results['classification_metrics']['f1_score'] >= 0.5, f"F1 score too low: {results['classification_metrics']['f1_score']:.3f}"
    
    # Assert difficulty-specific performance
    if 'easy' in results['difficulty_stats']:
        easy_pass_rate = results['difficulty_stats']['easy']['pass_rate']
        assert easy_pass_rate >= 0.6, f"Easy cases pass rate too low: {easy_pass_rate:.2%}"
    
    if 'hard' in results['difficulty_stats']:
        hard_pass_rate = results['difficulty_stats']['hard']['pass_rate']
        assert hard_pass_rate >= 0.25, f"Hard cases pass rate too low: {hard_pass_rate:.2%}"

# Additional helper functions for specific test case subsets
async def evaluate_medium_cases():
    """Evaluate only medium difficulty cases"""
    from tests.test_data.realistic_test_cases import REALISTIC_MEDIUM_CASES
    evaluator = SimpleModelEvaluator()
    return await evaluator.evaluate_all_cases(REALISTIC_MEDIUM_CASES)

async def evaluate_hard_cases():
    """Evaluate only hard difficulty cases"""
    from tests.test_data.realistic_test_cases import REALISTIC_HARD_CASES
    evaluator = SimpleModelEvaluator()
    return await evaluator.evaluate_all_cases(REALISTIC_HARD_CASES)

async def evaluate_edge_cases():
    """Evaluate only edge cases"""
    from tests.test_data.realistic_test_cases import REALISTIC_EDGE_CASES
    evaluator = SimpleModelEvaluator()
    return await evaluator.evaluate_all_cases(REALISTIC_EDGE_CASES)

async def evaluate_by_industry(industry: str):
    """Evaluate test cases from a specific industry"""
    industry_cases = [case for case in ALL_REALISTIC_CASES if case.industry == industry]
    if not industry_cases:
        print(f"No test cases found for industry: {industry}")
        return None
    
    evaluator = SimpleModelEvaluator()
    return await evaluator.evaluate_all_cases(industry_cases)

# Standalone execution
if __name__ == "__main__":
    """
    Run this script directly to perform comprehensive evaluation
    """
    import asyncio
    
    async def main():
        print("Running Comprehensive Realistic Test Case Evaluation...")
        await evaluate_all_realistic_cases()
    
    asyncio.run(main())