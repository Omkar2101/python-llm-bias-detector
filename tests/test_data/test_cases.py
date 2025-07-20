

# from typing import Dict, List, Optional
# from dataclasses import dataclass

# @dataclass
# class TestCase:
#     id: str
#     name: str
#     job_description: str
#     expected_bias_score: float
#     expected_inclusivity_score: float
#     expected_clarity_score: float
#     expected_issues_count: int
#     expected_bias_types: List[str]
#     expected_severity_levels: List[str]
#     difficulty_level: str  # "easy", "medium", "hard"
#     description: str

# # HIGH BIAS TEST CASES
# HIGH_BIAS_CASES = [
#     TestCase(
#         id="HB001",
#         name="Explicit Gender Discrimination",
#         job_description="""
#         Sales Manager Position - Males Only
        
#         We are looking for a dynamic male professional to join our sales team. 
#         The ideal candidate should be a young, energetic guy who can handle 
#         aggressive sales targets. Previous experience with masculine industries 
#         preferred. Must be able to work long hours and frequent travel.
        
#         Requirements:
#         - Male candidates only
#         - Age: 25-35 years
#         - Aggressive personality
#         - No family commitments preferred
#         """,
#         expected_bias_score=0.8,
#         expected_inclusivity_score=0.2,
#         expected_clarity_score=0.7,
#         expected_issues_count=5,
#         expected_bias_types=["gender", "age"],
#         expected_severity_levels=["high", "medium"],
#         difficulty_level="easy",
#         description="Explicit gender discrimination with age bias"
#     ),
    
#     TestCase(
#         id="HB002",
#         name="Multiple Discrimination Types",
#         job_description="""
#         Executive Assistant - Premium Company
        
#         Seeking an attractive, well-groomed female assistant from a good family 
#         background. Must be a native English speaker with traditional values. 
#         Preference for unmarried candidates who can dedicate full time to the role.
        
#         Requirements:
#         - Female candidates preferred
#         - Native English speaker only
#         - Traditional appearance
#         - No religious accommodations
#         - Must be from reputable family
#         """,
#         expected_bias_score=0.9,
#         expected_inclusivity_score=0.1,
#         expected_clarity_score=0.6,
#         expected_issues_count=6,
#         expected_bias_types=["gender", "racial", "cultural", "religious"],
#         expected_severity_levels=["high"],
#         difficulty_level="easy",
#         description="Multiple types of explicit discrimination"
#     ),
# ]

# # MEDIUM BIAS TEST CASES
# MEDIUM_BIAS_CASES = [
#     TestCase(
#         id="MB001",
#         name="Subtle Gender Coded Language",
#         job_description="""
#         Project Manager - Tech Startup
        
#         We need a rockstar project manager who can dominate the market and 
#         aggressively pursue new opportunities. The ideal candidate is a ninja 
#         who can hack through obstacles and crush the competition. Must be 
#         a digital native with fresh perspectives.
        
#         Requirements:
#         - Recent graduate preferred
#         - Competitive and aggressive mindset
#         - Must be a natural leader
#         - High energy and ambitious
#         """,
#         expected_bias_score=0.4,
#         expected_inclusivity_score=0.6,
#         expected_clarity_score=0.5,
#         expected_issues_count=4,
#         expected_bias_types=["gender", "age"],
#         expected_severity_levels=["medium", "low"],
#         difficulty_level="medium",
#         description="Subtle masculine-coded language with age bias"
#     ),
    
#     TestCase(
#         id="MB002",
#         name="Cultural and Educational Bias",
#         job_description="""
#         Marketing Coordinator
        
#         Looking for a creative marketing professional who understands American 
#         culture and values. Must be a cultural fit with our team. Preference 
#         for candidates from prestigious universities with strong networks.
        
#         Requirements:
#         - Native English speaker
#         - Understanding of American market
#         - Ivy League or top-tier university preferred
#         - Strong professional network
#         - Cultural alignment with company values
#         """,
#         expected_bias_score=0.5,
#         expected_inclusivity_score=0.5,
#         expected_clarity_score=0.7,
#         expected_issues_count=3,
#         expected_bias_types=["cultural", "socioeconomic"],
#         expected_severity_levels=["medium"],
#         difficulty_level="medium",
#         description="Cultural assumptions and educational elitism"
#     ),
# ]

# # LOW BIAS TEST CASES
# LOW_BIAS_CASES = [
#     TestCase(
#         id="LB001",
#         name="Minor Language Issues",
#         job_description="""
#         Software Developer
        
#         We are seeking a skilled developer to join our team. The candidate 
#         should be passionate about coding and have strong problem-solving 
#         abilities. We value fresh ideas and innovative thinking.
        
#         Requirements:
#         - Bachelor's degree in Computer Science or related field
#         - 2+ years of experience in software development
#         - Strong communication skills
#         - Ability to work in a fast-paced environment
#         """,
#         expected_bias_score=0.1,
#         expected_inclusivity_score=0.9,
#         expected_clarity_score=0.8,
#         expected_issues_count=1,
#         expected_bias_types=["age"],
#         expected_severity_levels=["low"],
#         difficulty_level="easy",
#         description="Minor age-related language (fresh ideas)"
#     ),
# ]

# # CONFUSING/EDGE CASES
# CONFUSING_CASES = [
#     TestCase(
#         id="CC001",
#         name="Legitimate Physical Requirements",
#         job_description="""
#         Physical Therapist Position
        
#         We are seeking a licensed physical therapist to join our rehabilitation 
#         team. The candidate must be physically capable of demonstrating exercises, 
#         lifting patients, and standing for extended periods. Must have strong 
#         interpersonal skills and be able to motivate patients.
        
#         Requirements:
#         - Licensed Physical Therapist (RPT)
#         - Ability to lift up to 50 pounds
#         - Physical stamina for 8-hour shifts
#         - Excellent communication skills
#         - Experience with rehabilitation techniques
#         """,
#         expected_bias_score=0.0,
#         expected_inclusivity_score=0.95,
#         expected_clarity_score=0.9,
#         expected_issues_count=0,
#         expected_bias_types=[],
#         expected_severity_levels=[],
#         difficulty_level="hard",
#         description="Physical requirements that are job-relevant, not discriminatory"
#     ),
    
#     TestCase(
#         id="CC002",
#         name="Language Teacher Requirements",
#         job_description="""
#         Hindi Language Teacher
        
#         We are looking for a native Hindi speaker to teach Hindi language 
#         and culture to international students. The candidate must be fluent 
#         in Hindi, English, and have deep understanding of Indian culture.
        
#         Requirements:
#         - Native Hindi speaker
#         - Fluent in English
#         - Knowledge of Indian cultural traditions
#         - Teaching experience preferred
#         - Ability to conduct classes in Hindi
#         """,
#         expected_bias_score=0.0,
#         expected_inclusivity_score=0.95,
#         expected_clarity_score=0.9,
#         expected_issues_count=0,
#         expected_bias_types=[],
#         expected_severity_levels=[],
#         difficulty_level="hard",
#         description="Language requirements that are job-relevant"
#     ),
    
#     TestCase(
#         id="CC003",
#         name="Ambiguous Requirements",
#         job_description="""
#         Customer Service Representative
        
#         Looking for a people person who can handle difficult customers with 
#         grace. Must be presentable and have a pleasant personality. The ideal 
#         candidate is someone who naturally connects with people and can 
#         represent our brand professionally.
        
#         Requirements:
#         - Strong interpersonal skills
#         - Professional appearance
#         - Positive attitude
#         - Ability to remain calm under pressure
#         - Team player mentality
#         """,
#         expected_bias_score=0.2,
#         expected_inclusivity_score=0.8,
#         expected_clarity_score=0.6,
#         expected_issues_count=2,
#         expected_bias_types=["gender", "physical"],
#         expected_severity_levels=["low"],
#         difficulty_level="hard",
#         description="Ambiguous language that could be interpreted as biased"
#     ),
# ]

# # NEGATIVE TEST CASES (Should have no bias)
# NEGATIVE_CASES = [
#     TestCase(
#         id="NC001",
#         name="Inclusive Job Description",
#         job_description="""
#         Software Engineer - Remote Position
        
#         We are seeking a talented software engineer to join our diverse and 
#         inclusive team. We welcome applications from all qualified candidates 
#         regardless of background, identity, or experience level.
        
#         Requirements:
#         - Bachelor's degree in Computer Science or equivalent experience
#         - Proficiency in Python and JavaScript
#         - Experience with cloud platforms
#         - Strong problem-solving abilities
#         - Collaborative mindset
        
#         We offer flexible working arrangements and are committed to creating 
#         an inclusive workplace where everyone can thrive.
#         """,
#         expected_bias_score=0.0,
#         expected_inclusivity_score=1.0,
#         expected_clarity_score=0.95,
#         expected_issues_count=0,
#         expected_bias_types=[],
#         expected_severity_levels=[],
#         difficulty_level="easy",
#         description="Highly inclusive job description with no bias"
#     ),
    
#     TestCase(
#         id="NC002",
#         name="Skills-Focused Description",
#         job_description="""
#         Data Analyst
        
#         Join our analytics team to help drive data-driven decisions. You'll 
#         work with cross-functional teams to analyze business metrics and 
#         provide actionable insights.
        
#         Requirements:
#         - Experience with SQL and Python
#         - Strong analytical and critical thinking skills
#         - Ability to communicate complex data insights clearly
#         - Experience with data visualization tools
#         - Collaborative approach to problem-solving
        
#         We value diverse perspectives and encourage applications from 
#         candidates with varied backgrounds and experiences.
#         """,
#         expected_bias_score=0.0,
#         expected_inclusivity_score=0.95,
#         expected_clarity_score=0.9,
#         expected_issues_count=0,
#         expected_bias_types=[],
#         expected_severity_levels=[],
#         difficulty_level="easy",
#         description="Skills-focused description with inclusive language"
#     ),
# ]

# # Combine all test cases
# ALL_TEST_CASES = HIGH_BIAS_CASES + MEDIUM_BIAS_CASES + LOW_BIAS_CASES + CONFUSING_CASES + NEGATIVE_CASES

# # Group by difficulty
# EASY_CASES = [case for case in ALL_TEST_CASES if case.difficulty_level == "easy"]
# MEDIUM_CASES = [case for case in ALL_TEST_CASES if case.difficulty_level == "medium"]
# HARD_CASES = [case for case in ALL_TEST_CASES if case.difficulty_level == "hard"]

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
