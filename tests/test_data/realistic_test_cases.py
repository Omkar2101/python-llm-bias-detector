# tests/test_data/realistic_test_cases.py

from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class RealTestCase:
    id: str
    name: str
    job_description: str
    expected_bias_score: float
    expected_inclusivity_score: float
    expected_clarity_score: float
    expected_issues_count: int
    expected_bias_types: List[str]
    expected_severity_levels: List[str]
    difficulty_level: str
    description: str
    industry: str  # Added for more context
    role_level: str  # junior, mid, senior, executive



# REALISTIC MEDIUM CASES - Subtle biases common in real job postings
REALISTIC_MEDIUM_CASES = [
    RealTestCase(
        id="RM001",
        name="Sales Role with Subtle Gender Coding",
        job_description="""
        Account Executive - Enterprise Sales
        
        We're seeking a competitive sales professional to penetrate new markets and 
        dominate our territory. The ideal candidate is aggressive in pursuing leads, 
        assertive in negotiations, and thrives in a cut-throat competitive environment.
        
        Key Responsibilities:
        - Aggressively pursue new business opportunities
        - Dominate client meetings and close deals
        - Compete with other sales reps to exceed quotas
        - Build relationships through networking events and golf outings
        - Travel extensively to client sites (up to 70% travel)
        
        Qualifications:
        - Proven track record of crushing sales targets
        - Strong, assertive communication style
        - Ability to work independently with minimal supervision
        - Comfortable in high-pressure, competitive situations
        - Bachelor's degree preferred
        
        This role requires someone with a killer instinct who can take charge and 
        drive results in a fast-paced environment.
        """,
        expected_bias_score=0.6,
        expected_inclusivity_score=0.4,
        expected_clarity_score=0.8,
        expected_issues_count=4,
        expected_bias_types=["gender"],
        expected_severity_levels=["medium"],
        difficulty_level="medium",
        description="Masculine-coded language that may deter female applicants",
        industry="sales",
        role_level="mid"
    ),
    
    RealTestCase(
        id="RM002",
        name="Marketing Role with Cultural Assumptions",
        job_description="""
        Marketing Manager - Consumer Brands
        
        Growing consumer goods company seeks marketing manager to lead brand strategy 
        for our American market. Ideal candidate understands American consumer culture 
        and traditional family values.
        
        Responsibilities:
        - Develop marketing campaigns that resonate with mainstream American families
        - Manage relationships with advertising agencies and media partners
        - Conduct market research on traditional demographic segments
        - Present to senior leadership and external partners
        
        Requirements:
        - MBA from top-tier American university preferred
        - Native English speaker with excellent written communication
        - Deep understanding of American cultural nuances and traditions
        - Professional appearance suitable for client presentations
        - Strong network within US marketing industry
        - Comfortable working standard business hours (some evening events)
        
        We're looking for someone who naturally understands our target demographic 
        and can authentically represent our brand values to traditional families.
        """,
        expected_bias_score=0.55,
        expected_inclusivity_score=0.45,
        expected_clarity_score=0.7,
        expected_issues_count=4,
        expected_bias_types=["cultural", "socioeconomic"],
        expected_severity_levels=["medium"],
        difficulty_level="medium",
        description="Cultural assumptions and native speaker requirement that may exclude qualified candidates",
        industry="marketing",
        role_level="senior"
    ),
    
    RealTestCase(
        id="RM003",
        name="Finance Role with Subtle Ageism",
        job_description="""
        Financial Analyst - Investment Banking
        
        Fast-paced investment bank seeks energetic financial analyst to join our 
        dynamic team. This role demands fresh thinking and the ability to adapt 
        quickly to our evolving technological environment.
        
        Key Requirements:
        - Recent graduate with finance or economics degree
        - High energy and enthusiasm for long hours
        - Tech-savvy with ability to learn new digital platforms quickly
        - Fresh perspective on market trends and investment strategies
        - Ability to keep up with our fast-moving, high-energy culture
        - Comfortable with extensive travel and irregular schedules
        
        Ideal Candidate:
        - Early career professional (0-3 years experience)
        - Digitally native with strong social media understanding
        - Eager to learn and willing to start at entry level
        - Energetic personality that fits our youthful company culture
        
        This is an excellent opportunity for a recent graduate looking to launch 
        their career in a vibrant, youth-oriented environment.
        """,
        expected_bias_score=0.5,
        expected_inclusivity_score=0.5,
        expected_clarity_score=0.7,
        expected_issues_count=3,
        expected_bias_types=["age"],
        expected_severity_levels=["medium", "low"],
        difficulty_level="medium",
        description="Age-coded language favoring younger candidates without explicit discrimination",
        industry="finance",
        role_level="junior"
    ),
    
    RealTestCase(
        id="RM004",
        name="Healthcare Role with Physical Requirements",
        job_description="""
        Registered Nurse - Emergency Department
        
        Busy emergency department seeks experienced RN to provide patient care 
        in fast-paced environment. Must be physically and mentally capable of 
        handling demanding situations.
        
        Essential Functions:
        - Provide direct patient care including lifting and moving patients
        - Stand and walk for entire 12-hour shifts
        - Respond quickly to emergency situations
        - Work rotating shifts including nights, weekends, and holidays
        - Maintain composure under extreme pressure
        
        Requirements:
        - Current RN license in good standing
        - BLS and ACLS certification
        - Minimum 2 years emergency or critical care experience
        - Ability to lift 50 pounds and assist with patient transfers
        - Excellent physical stamina and mental resilience
        - Perfect vision and hearing to monitor patient conditions
        - Quick reflexes for emergency response
        
        This role requires someone in excellent physical condition who can handle 
        the physical and emotional demands of emergency medicine.
        """,
        expected_bias_score=0.3,
        expected_inclusivity_score=0.7,
        expected_clarity_score=0.8,
        expected_issues_count=2,
        expected_bias_types=["disability"],
        expected_severity_levels=["medium", "low"],
        difficulty_level="medium",
        description="Some physical requirements may be job-relevant, others potentially discriminatory",
        industry="healthcare",
        role_level="mid"
    )
]

# REALISTIC HARD CASES - Complex scenarios requiring nuanced analysis
REALISTIC_HARD_CASES = [
    RealTestCase(
        id="RH001",
        name="Executive Assistant with Multiple Subtle Biases",
        job_description="""
        Executive Assistant to CEO - Fortune 500 Company
        
        Prestigious multinational corporation seeks polished executive assistant 
        to support our dynamic CEO. This high-visibility role requires someone 
        who can seamlessly represent our company culture and values.
        
        Key Responsibilities:
        - Manage complex calendar and coordinate international travel
        - Interface with C-suite executives and high-profile clients
        - Organize board meetings and corporate events
        - Handle confidential information with discretion
        - Accompany CEO to evening events and client dinners
        
        Ideal Candidate Profile:
        - Impeccable professional presentation and communication skills
        - Cultural sophistication suitable for international business settings
        - Educational background from prestigious institution preferred
        - Youthful energy combined with mature judgment (ages 25-35 ideal)
        - Flexibility for extensive travel and non-traditional hours
        - Strong family support system to handle demanding schedule
        
        We seek someone who naturally embodies our corporate values and can 
        effortlessly navigate high-level business and social situations. 
        Previous experience supporting senior executives in traditional 
        corporate environments is essential.
        """,
        expected_bias_score=0.7,
        expected_inclusivity_score=0.3,
        expected_clarity_score=0.7,
        expected_issues_count=5,
        expected_bias_types=["age", "socioeconomic", "cultural", "gender"],
        expected_severity_levels=["medium", "high"],
        difficulty_level="hard",
        description="Multiple subtle biases including age, class, and gender assumptions",
        industry="corporate",
        role_level="senior"
    ),
    
    RealTestCase(
        id="RH002",
        name="Tech Role with Accessibility Barriers",
        job_description="""
        UX Designer - Digital Products
        
        Innovative tech company seeks creative UX designer to shape the future 
        of digital experiences. Join our collaborative team creating cutting-edge 
        user interfaces.
        
        Core Responsibilities:
        - Design intuitive user interfaces for web and mobile applications
        - Conduct user research and usability testing
        - Collaborate with developers and product managers
        - Present design concepts to stakeholders
        - Iterate on designs based on user feedback
        
        Requirements:
        - Bachelor's in Design, HCI, or related field
        - 3+ years UX design experience
        - Portfolio demonstrating visual design skills
        - Proficiency in Figma, Sketch, and Adobe Creative Suite
        - Excellent visual perception and color discrimination abilities
        - Strong presentation skills and ability to articulate design decisions
        - Comfortable working in open office environment
        - Ability to work standard office hours with occasional overtime
        
        Our office features an open, collaborative workspace with standing desks 
        and requires clear verbal communication for team meetings and presentations. 
        Visual acuity is essential for detailed design work and quality control.
        """,
        expected_bias_score=0.4,
        expected_inclusivity_score=0.6,
        expected_clarity_score=0.8,
        expected_issues_count=3,
        expected_bias_types=["disability"],
        expected_severity_levels=["medium"],
        difficulty_level="hard",
        description="Subtle accessibility barriers that may exclude qualified candidates with disabilities",
        industry="technology",
        role_level="mid"
    ),
    
    RealTestCase(
        id="RH003",
        name="International Role with Cultural Requirements",
        job_description="""
        Business Development Manager - Asia Pacific
        
        Global technology company expanding into Asian markets seeks business 
        development manager to establish partnerships and drive growth across 
        the Asia Pacific region.
        
        Role Overview:
        - Lead market entry strategy for Japan, South Korea, and Southeast Asia
        - Build relationships with local partners and distributors
        - Navigate complex cultural and regulatory environments
        - Represent company at international trade shows and conferences
        - Develop localized go-to-market strategies
        
        Essential Qualifications:
        - Fluency in English and at least two Asian languages (Japanese/Korean/Mandarin)
        - Deep cultural understanding of Asian business practices
        - Extensive experience living and working in Asia (minimum 5 years)
        - Strong network of business contacts throughout region
        - MBA from internationally recognized institution
        - Proven track record in B2B sales or business development
        
        Preferred Qualifications:
        - Asian heritage with authentic cultural insights
        - Personal connections within target markets
        - Understanding of traditional business hierarchies and decision-making processes
        
        This role requires frequent travel throughout Asia (60%+) and ability to 
        build trust with traditional Asian business leaders.
        """,
        expected_bias_score=0.45,
        expected_inclusivity_score=0.55,
        expected_clarity_score=0.8,
        expected_issues_count=3,
        expected_bias_types=["cultural", "racial"],
        expected_severity_levels=["medium"],
        difficulty_level="hard",
        description="Cultural and heritage preferences that may be job-relevant but potentially discriminatory",
        industry="technology",
        role_level="senior"
    ),
    
    RealTestCase(
        id="RH004",
        name="Creative Role with Ambiguous Requirements",
        job_description="""
        Creative Director - Luxury Fashion Brand
        
        Prestigious luxury fashion house seeks visionary creative director to lead 
        our design team and brand aesthetic. This role demands someone who embodies 
        our brand's sophisticated, exclusive image.
        
        Key Responsibilities:
        - Define creative vision and seasonal design direction
        - Lead team of designers and creative professionals
        - Represent brand at fashion weeks and industry events
        - Collaborate with marketing on brand positioning
        - Maintain brand's luxury positioning and exclusivity
        
        Candidate Profile:
        - Exceptional aesthetic sensibility and cultural sophistication
        - Personal style that aligns with our luxury brand image
        - Network within high-end fashion and luxury markets
        - Background that demonstrates understanding of luxury consumer mindset
        - Presence and charisma suitable for public representation
        - Portfolio reflecting refined, sophisticated design aesthetic
        
        Qualifications:
        - 10+ years in luxury fashion or related creative field
        - Proven ability to set trends and influence cultural movements
        - Strong leadership and team management experience
        - International perspective on luxury markets
        - Fluency in fashion industry cultural codes and unspoken standards
        
        We seek someone who naturally understands and can authentically represent 
        the luxury lifestyle our brand embodies.
        """,
        expected_bias_score=0.35,
        expected_inclusivity_score=0.65,
        expected_clarity_score=0.7,
        expected_issues_count=2,
        expected_bias_types=["socioeconomic", "cultural"],
        expected_severity_levels=["medium", "low"],
        difficulty_level="hard",
        description="Subjective requirements around 'sophistication' and 'luxury lifestyle' that may exclude based on background",
        industry="fashion",
        role_level="executive"
    ),
    
    RealTestCase(
        id="RH005",
        name="Religious Organization Role",
        job_description="""
        Program Coordinator - Faith-Based Non-Profit
        
        Established Christian non-profit organization seeks program coordinator 
        to oversee youth development initiatives and community outreach programs.
        
        Position Overview:
        - Coordinate after-school programs and summer camps for at-risk youth
        - Develop partnerships with local schools and community organizations
        - Manage volunteer recruitment and training programs
        - Oversee program budgets and grant reporting
        - Represent organization at community events and fundraising activities
        
        Requirements:
        - Bachelor's degree in Social Work, Education, or related field
        - 3+ years experience in youth development or non-profit management
        - Strong organizational and communication skills
        - Commitment to Christian values and mission-driven work
        - Ability to work flexible hours including evenings and weekends
        - Background check and references required
        
        Preferred Qualifications:
        - Active participation in Christian community
        - Experience working with diverse, underserved populations
        - Bilingual abilities (English/Spanish)
        - Grant writing experience
        
        Our organization is committed to serving all community members regardless 
        of background, while maintaining our Christian identity and values in 
        program delivery and staff culture.
        """,
        expected_bias_score=0.4,
        expected_inclusivity_score=0.6,
        expected_clarity_score=0.8,
        expected_issues_count=2,
        expected_bias_types=["religious"],
        expected_severity_levels=["medium"],
        difficulty_level="hard",
        description="Religious requirements that may be legitimate for faith-based organization but potentially exclusionary",
        industry="non-profit",
        role_level="mid"
    ),
    
    RealTestCase(
        id="RH006",
        name="Startup Equity and Family Considerations",
        job_description="""
        VP of Engineering - Fast-Growth Startup
        
        Series B startup revolutionizing fintech seeks VP of Engineering to scale 
        our technical team and infrastructure. This is a ground-floor opportunity 
        with significant equity upside for the right candidate.
        
        Role Scope:
        - Build and lead engineering team from 10 to 50+ engineers
        - Define technical architecture and engineering culture
        - Work closely with founders on product strategy and roadmap
        - Recruit and mentor senior technical talent
        - Navigate rapid scaling challenges and technical debt
        
        What We're Looking For:
        - 8+ years engineering experience with 3+ years in leadership
        - Experience scaling engineering teams at high-growth companies
        - Strong technical background in distributed systems and cloud architecture
        - Entrepreneurial mindset and comfort with ambiguity
        - Ability to thrive in fast-paced, high-pressure environment
        - Willingness to work extensive hours during critical periods
        - Flexibility for irregular schedules and tight deadlines
        
        Compensation Package:
        - Competitive base salary
        - Significant equity package (0.5-1.5% of company)
        - Potential for life-changing financial returns if successful
        - Health insurance and standard benefits
        
        Note: This role demands exceptional commitment and may not be suitable 
        for candidates with significant family obligations or those seeking 
        work-life balance. We're building something extraordinary and need 
        team members who can fully commit to the mission.
        """,
        expected_bias_score=0.55,
        expected_inclusivity_score=0.45,
        expected_clarity_score=0.8,
        expected_issues_count=3,
        expected_bias_types=["gender", "age"],
        expected_severity_levels=["medium"],
        difficulty_level="hard",
        description="Indirect bias against candidates with family responsibilities, typically affecting women and older workers",
        industry="technology",
        role_level="executive"
    )
]

# EDGE CASES - Testing boundary conditions and tricky scenarios
REALISTIC_EDGE_CASES = [
    RealTestCase(
        id="RE001",
        name="Legitimate Security Clearance Requirements",
        job_description="""
        Software Engineer - Defense Contractor
        
        Defense technology company seeks software engineer to work on classified 
        government projects. This role requires the highest levels of security 
        clearance and background investigation.
        
        Security Requirements:
        - Must be eligible for Top Secret/SCI security clearance
        - US citizenship required by federal regulations
        - Extensive background investigation including financial history
        - No foreign contacts or travel to certain countries
        - Clean criminal record and credit history
        - Willingness to undergo polygraph examination
        
        Technical Requirements:
        - Bachelor's degree in Computer Science or Engineering
        - 5+ years experience in C++, Java, or similar languages
        - Experience with secure coding practices
        - Knowledge of cybersecurity principles
        - Ability to work in classified environment
        
        Due to the sensitive nature of our work, applicants must meet strict 
        federal security requirements. These requirements are mandated by 
        government contracts and are non-negotiable.
        """,
        expected_bias_score=0.1,
        expected_inclusivity_score=0.8,
        expected_clarity_score=0.9,
        expected_issues_count=1,
        expected_bias_types=["legal"],
        expected_severity_levels=["low"],
        difficulty_level="hard",
        description="Legitimate government-mandated requirements that appear discriminatory but are legally required",
        industry="defense",
        role_level="mid"
    ),
    
    RealTestCase(
        id="RE002",
        name="Actor Casting Call",
        job_description="""
        Male Actor - Historical Drama Film
        
        Major film production seeks male actor to portray historical figure 
        Abraham Lincoln in upcoming biographical drama. This is a leading 
        role requiring extensive preparation and commitment.
        
        Role Requirements:
        - Male actor, ages 35-55
        - Height 6'2" or taller to match historical accuracy
        - Ability to grow full beard
        - Strong dramatic acting background
        - Physical resemblance to Abraham Lincoln preferred
        - Experience with period costume and dialect work
        
        Production Details:
        - 6-month filming schedule
        - Extensive historical research required
        - Physical demands include outdoor scenes and long shooting days
        - Must be available for promotional activities
        
        This is a legitimate casting requirement based on historical accuracy 
        and the biographical nature of the production.
        """,
        expected_bias_score=0.2,
        expected_inclusivity_score=0.6,
        expected_clarity_score=0.9,
        expected_issues_count=1,
        expected_bias_types=["gender", "physical"],
        expected_severity_levels=["low"],
        difficulty_level="hard",
        description="Legitimate appearance requirements for acting role that would be discriminatory in other contexts",
        industry="entertainment",
        role_level="senior"
    ),
    
    RealTestCase(
        id="RE003",
        name="Women's Shelter Counselor",
        job_description="""
        Trauma Counselor - Women's Domestic Violence Shelter
        
        Non-profit women's shelter seeks female trauma counselor to provide 
        mental health services to survivors of domestic violence and sexual assault.
        
        Role Responsibilities:
        - Provide individual and group counseling to female survivors
        - Conduct crisis intervention and safety planning
        - Facilitate support groups and trauma recovery programs
        - Collaborate with legal advocates and social workers
        - Maintain confidential client records and case notes
        
        Requirements:
        - Master's degree in Social Work, Psychology, or Counseling
        - Licensed therapist (LCSW, LPC, or equivalent)
        - Specialized training in trauma and domestic violence
        - Female gender required due to the sensitive nature of client population
        - Experience working with trauma survivors preferred
        - Bilingual abilities (English/Spanish) strongly preferred
        
        Our female clients often have severe trauma histories with male perpetrators 
        and specifically request female counselors for their safety and comfort. 
        This gender requirement is essential for effective service delivery.
        """,
        expected_bias_score=0.15,
        expected_inclusivity_score=0.8,
        expected_clarity_score=0.9,
        expected_issues_count=1,
        expected_bias_types=["gender"],
        expected_severity_levels=["low"],
        difficulty_level="hard",
        description="Legitimate gender requirement based on client safety and therapeutic needs",
        industry="social_services",
        role_level="mid"
    )
]

# Combine all realistic test cases
ALL_REALISTIC_CASES =  REALISTIC_MEDIUM_CASES + REALISTIC_HARD_CASES + REALISTIC_EDGE_CASES

# Export for easy access

REALISTIC_MEDIUM = REALISTIC_MEDIUM_CASES
REALISTIC_HARD = REALISTIC_HARD_CASES
REALISTIC_EDGE = REALISTIC_EDGE_CASES