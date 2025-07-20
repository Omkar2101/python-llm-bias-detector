

from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class TestCase:
    id: str
    name: str
    job_description: str
    expected_bias_score: float
    expected_inclusivity_score: float
    expected_clarity_score: float
    expected_issues_count: int
    expected_bias_types: List[str]
    expected_severity_levels: List[str]
    difficulty_level: str  # "easy", "medium", "hard"
    description: str

# HARD TEST CASES - Balanced set of 5 cases
HARD_CASES = [
    # POSITIVE TEST CASE - Should detect HIGH bias
    TestCase(
        id="HC001",
        name="Subtle But Clear Discrimination",
        job_description="""
        Executive Assistant - Premium Law Firm
        
        We seek a polished, attractive female assistant who can represent our 
        prestigious firm. The ideal candidate should be young, energetic, and 
        from a good family background. Must be a native English speaker with 
        traditional values and professional appearance.
        
        Requirements:
        - Female preferred for client interaction
        - Age 22-28 years
        - Ivy League education preferred
        - No visible tattoos or unconventional appearance
        - Available for evening events and travel
        - Strong family values and conservative mindset
        """,
        expected_bias_score=0.8,
        expected_inclusivity_score=0.2,
        expected_clarity_score=0.7,
        expected_issues_count=6,
        expected_bias_types=["gender", "age", "socioeconomic", "cultural"],
        expected_severity_levels=["high", "medium"],
        difficulty_level="hard",
        description="Multiple subtle discriminations that require sophisticated detection"
    ),
    
    # NEGATIVE TEST CASE - Should detect NO bias
    TestCase(
        id="HC002",
        name="Legitimate Job-Relevant Requirements",
        job_description="""
        Physical Therapist - Sports Medicine Clinic
        
        We are seeking a licensed physical therapist to join our sports medicine 
        team. The candidate must be physically capable of demonstrating exercises, 
        providing manual therapy, and working with athletes of all levels.
        
        Requirements:
        - Licensed Physical Therapist (DPT or equivalent)
        - Ability to lift and move up to 50 pounds
        - Physical stamina for 8-hour shifts
        - Experience with sports-related injuries
        - CPR certification required
        - Excellent communication and interpersonal skills
        """,
        expected_bias_score=0.0,
        expected_inclusivity_score=0.95,
        expected_clarity_score=0.9,
        expected_issues_count=0,
        expected_bias_types=[],
        expected_severity_levels=[],
        difficulty_level="hard",
        description="Physical requirements that are genuinely job-relevant and non-discriminatory"
    ),
    
    # CONFUSING TEST CASE - Ambiguous requirements
    TestCase(
        id="HC003",
        name="Cultural Role With Ambiguous Requirements",
        job_description="""
        Cultural Consultant - Japanese Market Entry
        
        We are seeking a cultural consultant to help our company enter the 
        Japanese market. The ideal candidate should have authentic understanding 
        of Japanese business culture and be able to naturally connect with 
        Japanese clients and partners.
        
        Requirements:
        - Native-level Japanese language proficiency
        - Deep understanding of Japanese business etiquette
        - Experience living in Japan for extended periods
        - Ability to represent our company in Japanese business settings
        - Strong network in Japanese business community
        - Cultural sensitivity and awareness
        """,
        expected_bias_score=0.3,
        expected_inclusivity_score=0.7,
        expected_clarity_score=0.8,
        expected_issues_count=2,
        expected_bias_types=["cultural"],
        expected_severity_levels=["medium", "low"],
        difficulty_level="hard",
        description="Cultural requirements that could be job-relevant or potentially exclusionary"
    ),
    
    # NEGATIVE TEST CASE - Highly inclusive
    TestCase(
        id="HC004",
        name="Model Inclusive Job Description",
        job_description="""
        Software Engineer - Accessibility Team
        
        Join our accessibility team to build technology that empowers everyone. 
        We welcome applications from candidates of all backgrounds, identities, 
        and experience levels. We believe diverse perspectives make our products 
        better for all users.
        
        Requirements:
        - Bachelor's degree in Computer Science or equivalent experience
        - Proficiency in JavaScript and Python
        - Experience with accessibility standards (WCAG)
        - Strong problem-solving and analytical skills
        - Collaborative mindset and empathy for user needs
        - Commitment to inclusive design principles
        
        We offer flexible work arrangements, comprehensive benefits, and are 
        committed to creating an inclusive workplace where everyone can thrive.
        """,
        expected_bias_score=0.0,
        expected_inclusivity_score=1.0,
        expected_clarity_score=0.95,
        expected_issues_count=0,
        expected_bias_types=[],
        expected_severity_levels=[],
        difficulty_level="hard",
        description="Highly inclusive job description with explicit diversity commitment"
    ),
    
    # CONFUSING TEST CASE - Industry-specific edge case
    TestCase(
        id="HC005",
        name="Fashion Industry Appearance Requirements",
        job_description="""
        Fashion Model - Luxury Brand Campaign
        
        We are casting for a fashion model to represent our luxury brand in 
        an upcoming campaign. The role requires embodying our brand aesthetic 
        and connecting with our target demographic. Must be comfortable with 
        photo shoots and public appearances.
        
        Requirements:
        - Height between 5'9" and 6'0"
        - Clothing size 2-4
        - Professional modeling portfolio
        - Photogenic qualities and camera presence
        - Ability to work flexible hours including weekends
        - Strong social media presence preferred
        """,
        expected_bias_score=0.4,
        expected_inclusivity_score=0.6,
        expected_clarity_score=0.8,
        expected_issues_count=3,
        expected_bias_types=["physical", "gender"],
        expected_severity_levels=["medium", "low"],
        difficulty_level="hard",
        description="Industry-specific appearance requirements that may be legitimate but potentially discriminatory"
    )
]

# Combine all test cases
ALL_TEST_CASES = HARD_CASES

# Group by difficulty
EASY_CASES = []
MEDIUM_CASES = []
HARD_CASES = HARD_CASES
