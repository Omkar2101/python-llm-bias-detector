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
    expected_bias_types: List[str]  # Using string values that match BiasType enum values
    expected_severity_levels: List[str]  # Using string values that match SeverityLevel enum values
    difficulty_level: str  # "easy", "medium", "hard"
    description: str

# EASY TEST CASES - Clear and obvious bias detection
EASY_CASES = [
    # POSITIVE TEST CASE - Obviously biased
    TestCase(
        id="EC001",
        name="Clear Gender Discrimination",
        job_description="""
        Sales Representative - Tech Company
        
        We are looking for a dynamic salesman to join our team. The ideal candidate 
        should be aggressive, dominant, and able to handle the pressure of our 
        male-dominated industry. This role requires someone who can be one of the boys 
        and fit in with our fraternal company culture.
        
        Requirements:
        - Male preferred
        - Strong, aggressive personality
        - Ability to work in a boys' club environment
        """,
        expected_bias_score=0.9,
        expected_inclusivity_score=0.1,
        expected_clarity_score=0.7,
        expected_issues_count=5,
        expected_bias_types=["gender"],
        expected_severity_levels=["high", "medium"],
        difficulty_level="easy",
        description="Obvious gender bias with explicit male preference"
    ),
    
    # NEGATIVE TEST CASE - Obviously unbiased
    TestCase(
        id="EC002",
        name="Clean Professional Description",
        job_description="""
        Software Engineer - Web Development
        
        We are seeking a skilled software engineer to join our development team. 
        The successful candidate will work on building scalable web applications 
        and collaborating with cross-functional teams.
        
        Requirements:
        - Bachelor's degree in Computer Science or related field
        - 3+ years of experience with JavaScript and Python
        - Strong problem-solving skills
        - Experience with modern web frameworks
        - Excellent communication skills
        """,
        expected_bias_score=0.0,
        expected_inclusivity_score=0.9,
        expected_clarity_score=0.9,
        expected_issues_count=0,
        expected_bias_types=[],
        expected_severity_levels=[],
        difficulty_level="easy",
        description="Clean, professional job description with no bias"
    ),
    
    # POSITIVE TEST CASE - Age bias
    TestCase(
        id="EC003",
        name="Obvious Age Discrimination",
        job_description="""
        Marketing Assistant - Startup
        
        We want young, energetic recent graduates who are digital natives. 
        Looking for someone under 25 who can bring fresh ideas and youthful 
        energy to our dynamic startup culture. No old-school thinking allowed!
        
        Requirements:
        - Recent graduate (within 2 years)
        - Under 25 years old
        - Young and energetic personality
        - Digital native mindset
        """,
        expected_bias_score=0.8,
        expected_inclusivity_score=0.2,
        expected_clarity_score=0.8,
        expected_issues_count=4,
        expected_bias_types=["age"],
        expected_severity_levels=["high", "medium"],
        difficulty_level="easy",
        description="Clear age discrimination targeting only young candidates"
    )
]

# MEDIUM TEST CASES - Subtle bias requiring more nuanced detection
MEDIUM_CASES = [
    # POSITIVE TEST CASE - Subtle gender bias
    TestCase(
        id="MC001",
        name="Subtle Gender-Coded Language",
        job_description="""
        Project Manager - Construction
        
        We need a strong leader who can take charge and dominate project timelines. 
        The ideal candidate is competitive, assertive, and can handle the rough 
        environment of construction sites. Must be tough enough to deal with 
        challenging contractors and aggressive negotiations.
        
        Requirements:
        - Strong leadership and dominant personality
        - Competitive and assertive nature
        - Ability to work in rough, physical environments
        - Thick skin for aggressive business dealings
        """,
        expected_bias_score=0.4,
        expected_inclusivity_score=0.6,
        expected_clarity_score=0.8,
        expected_issues_count=3,
        expected_bias_types=["gender"],
        expected_severity_levels=["medium", "low"],
        difficulty_level="medium",
        description="Gender-coded language that may discourage female applicants"
    ),
    
    # POSITIVE TEST CASE - Cultural bias
    TestCase(
        id="MC002",
        name="Cultural Assumptions",
        job_description="""
        Customer Service Representative - Global Company
        
        We are seeking a customer service representative with excellent communication 
        skills. The candidate must be a native English speaker with American cultural 
        understanding to better connect with our clientele. Should have traditional 
        work values and professional demeanor that aligns with our company culture.
        
        Requirements:
        - Native English speaker
        - American cultural background preferred
        - Traditional work ethic and values
        - Professional appearance and demeanor
        """,
        expected_bias_score=0.5,
        expected_inclusivity_score=0.5,
        expected_clarity_score=0.7,
        expected_issues_count=3,
        expected_bias_types=["cultural", "racial"],
        expected_severity_levels=["medium"],
        difficulty_level="medium",
        description="Cultural bias requiring native speaker when fluency would suffice"
    ),
    
    # CONFUSING TEST CASE - Physical requirements that may be legitimate
    TestCase(
        id="MC003",
        name="Ambiguous Physical Requirements",
        job_description="""
        Retail Associate - Fashion Store
        
        We are looking for a retail associate who can represent our brand well. 
        The candidate should have a professional appearance and be comfortable 
        interacting with fashion-conscious customers. Must be able to stand for 
        long periods and lift merchandise up to 30 pounds.
        
        Requirements:
        - Professional and attractive appearance
        - Comfortable with fashion and style
        - Ability to stand for 8+ hours
        - Lifting capacity up to 30 pounds
        - Outgoing personality
        """,
        expected_bias_score=0.3,
        expected_inclusivity_score=0.7,
        expected_clarity_score=0.8,
        expected_issues_count=2,
        expected_bias_types=["physical"],
        expected_severity_levels=["medium", "low"],
        difficulty_level="medium",
        description="Physical appearance requirements that may be unnecessary for role"
    )
]

# HARD TEST CASES - Complex scenarios requiring sophisticated analysis
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
        expected_bias_types=["gender", "age", "socioeconomic", "cultural", "physical"],
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
        expected_bias_types=["physical"],
        expected_severity_levels=["medium", "low"],
        difficulty_level="hard",
        description="Industry-specific appearance requirements that may be legitimate but potentially discriminatory"
    ),
    
    # POSITIVE TEST CASE - Religious bias
    TestCase(
        id="HC006",
        name="Religious and Legal Status Bias",
        job_description="""
        Administrative Coordinator - Non-Profit Organization
        
        We are seeking an administrative coordinator who shares our Christian values 
        and can work within our faith-based organization. The candidate must be a 
        US citizen with strong moral character and traditional family values.
        
        Requirements:
        - US citizenship required (no work visa holders)
        - Christian faith and values alignment
        - Available to work Sundays when needed
        - Strong moral character and family values
        - Bachelor's degree from accredited institution
        - 2+ years administrative experience
        """,
        expected_bias_score=0.7,
        expected_inclusivity_score=0.3,
        expected_clarity_score=0.8,
        expected_issues_count=4,
        expected_bias_types=["religious", "legal"],
        expected_severity_levels=["high", "medium"],
        difficulty_level="hard",
        description="Religious requirements and citizenship bias for non-religious role"
    ),
    
    # EDGE CASE - Disability-related requirements
    TestCase(
        id="HC007",
        name="Unnecessary Physical Ability Requirements",
        job_description="""
        Data Analyst - Remote Position
        
        We are seeking a data analyst for a fully remote position. The ideal 
        candidate should have perfect vision, excellent hearing, and the ability 
        to work in a fast-paced environment. Must be able to stand and walk as 
        needed during the workday.
        
        Requirements:
        - Perfect vision (20/20) and excellent hearing
        - Ability to stand and walk throughout workday
        - Quick reflexes and manual dexterity
        - Bachelor's degree in Statistics or related field
        - 3+ years experience with SQL and Python
        - Strong analytical and problem-solving skills
        """,
        expected_bias_score=0.6,
        expected_inclusivity_score=0.4,
        expected_clarity_score=0.7,
        expected_issues_count=4,
        expected_bias_types=["disability"],
        expected_severity_levels=["medium", "high"],
        difficulty_level="hard",
        description="Unnecessary physical requirements for remote data analysis role"
    )
]

# NON-JOB DESCRIPTION TEST CASES - For testing N/A responses
NON_JOB_CASES = [
    TestCase(
        id="NJ001",
        name="Recipe Text",
        job_description="""
        Chocolate Chip Cookie Recipe
        
        Ingredients:
        - 2 cups all-purpose flour
        - 1 cup butter, softened
        - 3/4 cup brown sugar
        - 1/2 cup white sugar
        - 2 eggs
        - 2 teaspoons vanilla extract
        - 1 teaspoon baking soda
        - 1 teaspoon salt
        - 2 cups chocolate chips
        
        Instructions:
        1. Preheat oven to 375°F
        2. Mix butter and sugars until creamy
        3. Add eggs and vanilla
        4. Combine dry ingredients and mix in
        5. Stir in chocolate chips
        6. Bake for 9-11 minutes
        """,
        expected_bias_score=0.0,  # Should be N/A but we test for proper handling
        expected_inclusivity_score=0.0,
        expected_clarity_score=0.0,
        expected_issues_count=0,
        expected_bias_types=[],
        expected_severity_levels=[],
        difficulty_level="easy",
        description="Non-job description text - should return N/A"
    ),
    
    TestCase(
        id="NJ002",
        name="Movie Review",
        job_description="""
        Movie Review: The Great Adventure
        
        This action-packed thriller delivers on every front. The cinematography is 
        stunning, with breathtaking landscapes and expertly choreographed fight 
        sequences. The lead actor brings depth to what could have been a one-dimensional 
        character, while the supporting cast provides excellent chemistry.
        
        The plot moves at a brisk pace, keeping viewers engaged throughout the 
        two-hour runtime. Special effects are seamlessly integrated, never feeling 
        overdone or distracting from the story. The soundtrack complements the 
        on-screen action perfectly.
        
        Rating: 4.5/5 stars
        Highly recommended for fans of the action genre.
        """,
        expected_bias_score=0.0,  # Should be N/A
        expected_inclusivity_score=0.0,
        expected_clarity_score=0.0,
        expected_issues_count=0,
        expected_bias_types=[],
        expected_severity_levels=[],
        difficulty_level="easy",
        description="Movie review text - should return N/A"
    )
]

# Combine all test cases
ALL_TEST_CASES = EASY_CASES + MEDIUM_CASES + HARD_CASES + NON_JOB_CASES

# Group by difficulty for easy access
EASY_CASES = EASY_CASES
MEDIUM_CASES = MEDIUM_CASES
HARD_CASES = HARD_CASES