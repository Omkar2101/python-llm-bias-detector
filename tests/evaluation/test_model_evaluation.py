# tests/evaluation/test_model_evaluation.py

import pytest
import asyncio
from typing import Dict, List, Tuple
import json
from datetime import datetime
import os
import sys

# Add the parent directory to sys.path to import from app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.services.llm_service import LLMService
from app.services.bias_detector import BiasDetector
from tests.test_data.test_cases import ALL_TEST_CASES, EASY_CASES, MEDIUM_CASES, HARD_CASES, TestCase

class BiasModelEvaluator:
    def __init__(self):
        self.llm_service = LLMService()
        self.bias_detector = BiasDetector()
        self.results = []
        
    def calculate_score_accuracy(self, expected: float, actual: float, tolerance: float = 0.5) -> bool:
        """Check if the actual score is within tolerance of expected score"""
        return abs(expected - actual) <= tolerance
    
    def calculate_score_difference(self, expected: float, actual: float) -> float:
        """Calculate absolute difference between expected and actual scores"""
        return abs(expected - actual)
    

 

    
    async def evaluate_single_case(self, test_case: TestCase) -> Dict:
        """Evaluate a single test case"""
        try:
            # Get the actual result from your bias detector
            result = await self.bias_detector.analyze_comprehensive(test_case.job_description)
            
            # Calculate accuracies
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
            detected_bias_types = [issue.type for issue in result.issues]
            expected_types_found = all(
                bias_type in detected_bias_types 
                for bias_type in test_case.expected_bias_types
            )
            
            evaluation_result = {
                'test_case_id': test_case.id,
                'test_case_name': test_case.name,
                'difficulty_level': test_case.difficulty_level,
                'description': test_case.description,
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
                        'type': issue.type,
                        'text': issue.text,
                        'severity': issue.severity,
                        'explanation': issue.explanation
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
    
    async def evaluate_all_cases(self, test_cases: List[TestCase] = None) -> Dict:
        """Evaluate all test cases or a subset"""
        if test_cases is None:
            test_cases = ALL_TEST_CASES
        
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
        
        overall_stats = {
            'total_cases': len(test_cases),
            'successful_evaluations': len(successful_results),
            'passed_cases': len(passed_results),
            'pass_rate': len(passed_results) / len(successful_results) if successful_results else 0,
            'avg_bias_score_diff': sum(r['score_differences']['bias_diff'] for r in successful_results) / len(successful_results) if successful_results else 0,
            'avg_inclusivity_score_diff': sum(r['score_differences']['inclusivity_diff'] for r in successful_results) / len(successful_results) if successful_results else 0,
            'avg_clarity_score_diff': sum(r['score_differences']['clarity_diff'] for r in successful_results) / len(successful_results) if successful_results else 0,
        }
        
        # Group results by difficulty
        difficulty_stats = {}
        for difficulty in ['easy', 'medium', 'hard']:
            difficulty_results = [r for r in successful_results if r['difficulty_level'] == difficulty]
            if difficulty_results:
                difficulty_passed = [r for r in difficulty_results if r['passed']]
                difficulty_stats[difficulty] = {
                    'total': len(difficulty_results),
                    'passed': len(difficulty_passed),
                    'pass_rate': len(difficulty_passed) / len(difficulty_results)
                }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'overall_stats': overall_stats,
            'difficulty_stats': difficulty_stats,
            'individual_results': results
        }
    
    def save_results(self, results: Dict, filename: str = None):
        """Save evaluation results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bias_evaluation_results_{timestamp}.json"
        
        results_dir = os.path.join(os.path.dirname(__file__), 'results')
        os.makedirs(results_dir, exist_ok=True)
        
        filepath = os.path.join(results_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to: {filepath}")
        return filepath
    
    def print_summary(self, results: Dict):
        """Print a summary of the evaluation results"""
        stats = results['overall_stats']
        
        print("\n" + "="*50)
        print("BIAS DETECTION MODEL EVALUATION SUMMARY")
        print("="*50)
        
        print(f"Total Test Cases: {stats['total_cases']}")
        print(f"Successfully Evaluated: {stats['successful_evaluations']}")
        print(f"Passed Cases: {stats['passed_cases']}")
        print(f"Overall Pass Rate: {stats['pass_rate']:.2%}")
        
        print(f"\nAverage Score Differences:")
        print(f"  Bias Score: {stats['avg_bias_score_diff']:.3f}")
        print(f"  Inclusivity Score: {stats['avg_inclusivity_score_diff']:.3f}")
        print(f"  Clarity Score: {stats['avg_clarity_score_diff']:.3f}")
        
        print(f"\nResults by Difficulty:")
        for difficulty, diff_stats in results['difficulty_stats'].items():
            print(f"  {difficulty.upper()}: {diff_stats['passed']}/{diff_stats['total']} ({diff_stats['pass_rate']:.2%})")
        
        # Print failed cases
        failed_cases = [r for r in results['individual_results'] if not r.get('passed', False)]
        if failed_cases:
            print(f"\nFailed Cases ({len(failed_cases)}):")
            for case in failed_cases:
                if 'error' in case:
                    print(f"  - {case['test_case_id']}: ERROR - {case['error']}")
                else:
                    print(f"  - {case['test_case_id']}: {case['test_case_name']}")
                    accuracy = case['accuracy_flags']
                    failed_metrics = [k for k, v in accuracy.items() if not v]
                    print(f"    Failed metrics: {', '.join(failed_metrics)}")





# Test functions for pytest


@pytest.mark.asyncio
async def test_hard_cases():
    """Test hard cases - these are the most challenging"""
    evaluator = BiasModelEvaluator()
    results = await evaluator.evaluate_all_cases(HARD_CASES)
    evaluator.print_summary(results)
    evaluator.save_results(results, "hard_cases_results1.json")
    
    # Assert minimum pass rate for hard cases (lower threshold)
    assert results['overall_stats']['pass_rate'] >= 0.4, f"Hard cases pass rate too low: {results['overall_stats']['pass_rate']:.2%}"

@pytest.mark.asyncio
async def test_all_cases():
    """Test all cases - comprehensive evaluation"""
    evaluator = BiasModelEvaluator()
    results = await evaluator.evaluate_all_cases()
    evaluator.print_summary(results)
    evaluator.save_results(results, "all_cases_results.json")
    
    # Assert overall minimum pass rate
    assert results['overall_stats']['pass_rate'] >= 0.4, f"Overall pass rate too low: {results['overall_stats']['pass_rate']:.2%}"





# Standalone evaluation script
if __name__ == "__main__":
    async def main():
        evaluator = BiasModelEvaluator()
        
        print("Starting comprehensive bias detection evaluation...")
        results = await evaluator.evaluate_all_cases()
        
        evaluator.print_summary(results)
        filepath = evaluator.save_results(results)
        
        print(f"\nEvaluation complete. Results saved to: {filepath}")
        
        # Print some specific case details
        print("\n" + "="*50)
        print("SAMPLE CASE DETAILS")
        print("="*50)
        
        for result in results['individual_results'][:3]:  # Show first 3 cases
            if 'error' not in result:
                print(f"\nCase: {result['test_case_name']}")
                print(f"Expected vs Actual Bias Score: {result['expected_scores']['bias_score']:.2f} vs {result['actual_scores']['bias_score']:.2f}")
                print(f"Expected vs Actual Inclusivity Score: {result['expected_scores']['inclusivity_score']:.2f} vs {result['actual_scores']['inclusivity_score']:.2f}")
                print(f"Issues Detected: {result['actual_scores']['issues_count']}")
                print(f"Passed: {result['passed']}")
    
    asyncio.run(main())