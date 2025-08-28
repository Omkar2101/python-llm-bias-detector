import os
import google.generativeai as genai
from typing import List, Dict
import json
from app.models.schemas import BiasIssue, Suggestion, BiasType, SeverityLevel, CategoryType
from fastapi import HTTPException
import time
from dotenv import load_dotenv

class LLMService:
    def __init__(self):

        # Load environment variables from .env file
        load_dotenv()  # Add this line

       

        # model_name = os.getenv("gemini-2.5-flash") 
        

        # Configure Google Gemini
        genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
        # self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.model = genai.GenerativeModel("gemini-2.5-flash")
    
    async def detect_bias(self, text: str) -> Dict:
        """Use Gemini to detect bias in job description"""
       

        

        # bias_detection_prompt = f"""
        # At first check that the job description is related to the particular job role and industry and fulfill the requirements of the job description then do the following:

        # Analyze the following text for job description bias using New York Human Rights Law (Section 296) and Colorado Anti-Discrimination Act (CADA) compliance standards. Follow this structured approach:

        # **STEP 1: VALIDATION**
        # Determine if the text is a job description. If not, return N/A response format.

        # **STEP 2: CONTEXT ANALYSIS** 
        # Identify the job role, industry, and core functions to distinguish legitimate requirements from bias.

        # **STEP 3: LEGAL COMPLIANCE & BIAS DETECTION**

        # **PROTECTED CLASSES UNDER NY HUMAN RIGHTS LAW & CADA (COLORADO ANTI-DISCRIMINATION ACT):**
        #     - Age (40+ under CADA, all ages under NY Law)
        #     - Race (including hair texture, hair type, hair length, protective hairstyles like braids, locs, twists, coils, cornrows, Bantu knots, Afros, headwraps)
        #     - Creed/Religion
        #     - Color
        #     - National Origin/Ancestry
        #     - Citizenship or Immigration Status (NY Law)
        #     - Sexual Orientation
        #     - Gender Identity or Expression
        #     - Military Status (NY Law)
        #     - Sex/Gender
        #     - Disability (mental/physical impairment substantially limiting major life activity)
        #     - Predisposing Genetic Characteristics (NY Law)
        #     - Familial Status
        #     - Marital Status (including marriage to co-worker under CADA)
        #     - Status as Victim of Domestic Violence (NY Law)
        #     - Pregnancy, childbirth, and related conditions

        #     **COLORADO JOB APPLICATION FAIRNESS ACT (CADA - Effective July 1, 2024):**
        #     Starting July 1, 2024, Colorado employers are prohibited from inquiring about a prospective employee's:
        #     - Age
        #     - Date of birth
        #     - Dates of attendance at educational institutions
        #     - Date of graduation from educational institutions

        #     **EXCEPTIONS - Employers may request age verification for compliance with:**
        #     - Bona fide occupational qualifications pertaining to public or occupational safety
        #     - Federal law or regulation requirements
        #     - State or local law or regulation based on bona fide occupational qualification

        #     **REDACTION RIGHTS:**
        #     Employers may request additional application materials (certifications, transcripts, third-party materials) at initial application if they notify individuals that they may redact:
        #     - Information identifying age
        #     - Date of birth
        #     - Dates of attendance at or graduation from educational institutions

            

        #     **DO NOT PENALIZE legitimate job requirements:**
        #     - DO NOT FLAG LEGITIMATE PROFESSIONAL REQUIREMENTS (e.g., DDS/DMD for dentists, physical demands for construction roles)
        #     - Security/police,Workers,Cleaners: physical fitness requirements
        #     - Medical roles: clinical skills, steady hands, pressure tolerance
        #     - Construction: physical strength, safety requirements
        #     - Professional certifications required by law/licensing boards
        #     - Language skills genuinely needed for role function
        #     - Standard professional terms when job-relevant

        #     **BIAS DETECTION CATEGORIES:**

        #     1. **Age Discrimination (NY Human Rights Law § 296(1)(a) & CADA)**

        #     **CONTEXT CHECK REQUIRED:** Before flagging, ask: Is this about job timing/schedule OR candidate age preference?
            
        #     **VIOLATIONS - Only flag these:**
        #     - EXPLICIT AGE REQUIREMENTS: "must be under 30", "age 25-35", "maximum age 40"
        #     - CODED DISCRIMINATORY LANGUAGE: "young and energetic", "digital native", "recent graduate preferred", "millennial mindset", "old-school", "mature professional"
            
        #     **DO NOT FLAG - These are legitimate:**
        #     - OPERATIONAL TIMING: "2025-2026 school year", "academic year", "project timeline 2024-2025", "fiscal year"
        #     - EXPERIENCE LEVELS: "entry-level", "senior-level", "new graduates", "experienced professionals" ,"0 years ","1-3 years experience", "3-5 years experience", "5+ years experience"
        #     - SKILLS-BASED: "5+ years experience required", "advanced degree needed"
            
        #     **POSITIVE INCLUSIVITY :**
        #     - "all experience levels welcome", "new grads and seasoned professionals", "entry-level to senior"
            
        #     **EXPLANATION:** "This violates NY Human Rights Law Section 296(1)(a) and CADA which prohibit age discrimination in employment"
            
           

        #     2. **Age Information Disclosure Bias (Colorado Job Application Fairness Act)**
        #     - VIOLATION: Requesting "age", "date of birth", "graduation dates", "attendance dates" on initial applications without bona fide occupational qualification
        #     - EXPLANATION: "This violates Colorado Job Application Fairness Act provisions prohibiting age-related information requests on initial employment applications unless required by federal law, state/local regulation, or bona fide occupational qualification for public/occupational safety"
        #     - SEVERITY: High for direct age requests, Medium for indirect age indicators, Exception for legally required qualifications

        #     3. **Race/Color/National Origin Discrimination (NY § 296(1)(a) & CADA)**
        #     - VIOLATION: "native English speaker", "cultural fit" without specifics, discriminatory hair/appearance requirements
        #     - EXPLANATION: "This violates NY Human Rights Law Section 296(1)(a) and CADA prohibiting discrimination based on race, color, national origin, or protective hairstyles"
        #     - SEVERITY: High for explicit requirements, Medium for coded language

        #     4. **Gender/Sex Discrimination (NY § 296(1)(a) & CADA)**
        #     - VIOLATION: Gendered job titles ("salesman"), assumptions about physical capabilities
        #     - EXPLANATION: "This violates NY Human Rights Law Section 296(1)(a) and CADA prohibiting sex-based discrimination in employment"
        #     - SEVERITY: High for explicit gender requirements, Medium for gendered language

        #     5. **Sexual Orientation/Gender Identity Discrimination (NY § 296(1)(a) & CADA)**
        #     - VIOLATION: Heteronormative assumptions, "he/she" only references, traditional family structure assumptions
        #     - EXPLANATION: "This violates NY Human Rights Law Section 296(1)(a) and CADA protecting sexual orientation and gender identity/expression"
        #     - SEVERITY: High for explicit exclusions, Medium for assumptions

        #     6. **Disability Discrimination (NY § 296(1)(a) & CADA)**
        #     - VIOLATION: Unnecessary physical requirements, "perfect vision" for non-visual jobs, "must stand" for remote work
        #     - EXPLANATION: "This violates NY Human Rights Law Section 296(1)(a) and CADA prohibiting disability discrimination and requiring reasonable accommodations"
        #     - SEVERITY: High for absolute requirements, Medium for unnecessary specifications

        #     7. **Pregnancy Discrimination (NY § 296(1)(g) & CADA)**
        #     - VIOLATION: Policies that disadvantage pregnant individuals, lack of accommodation mentions
        #     - EXPLANATION: "This violates NY Human Rights Law Section 296(1)(g) and CADA protecting pregnancy, childbirth, and related conditions"
        #     - SEVERITY: High for explicit exclusions, Medium for indirect disadvantages

        #     8. **Criminal History Bias (Relevant to protected reintegration rights)**
        #     - VIOLATION: Blanket "no criminal history" requirements without job relevance
        #     - EXPLANATION: "This may violate fair chance employment principles and could disproportionately impact protected classes"
        #     - SEVERITY: Medium for blanket exclusions, Low for legally required background checks

        #     9. **Religious Discrimination (NY § 296(1)(a) & CADA)**
        #     - VIOLATION: Religious holiday assumptions, specific faith requirements outside religious organizations
        #     - EXPLANATION: "This violates NY Human Rights Law Section 296(1)(a) and CADA prohibiting religious discrimination"
        #     - SEVERITY: High for explicit religious requirements, Medium for assumptions

        #     10. **Harassment-Conducive Language (NY § 296(1)(h))**
        #         - VIOLATION: Language that could contribute to hostile work environment
        #         - EXPLANATION: "This may contribute to harassment prohibited under NY Human Rights Law Section 296(1)(h)"
        #         - SEVERITY: Medium for potentially problematic language

        #     11. **Retaliation-Risk Language**
        #         - VIOLATION: Language discouraging protected activities or complaints
        #         - EXPLANATION: "This could discourage protected activities and may violate anti-retaliation provisions of NY Human Rights Law and CADA"
        #         - SEVERITY: High for explicit discouragement, Medium for subtle deterrents

        #     12. **Third-Party Materials & Redaction Rights (Colorado Job Application Fairness Act)**
        #         - BEST PRACTICE: When requesting certifications, transcripts, or third-party materials, notify applicants of their right to redact age-identifying information
        #         - EXPLANATION: "Colorado law requires employers to notify applicants they may redact age, birth date, or educational attendance/graduation dates from third-party materials"
        #         - SEVERITY: Medium for failure to provide redaction notice

        #     13. **Clarity Issues (Employment Communication Standards)**
    
        #         **ONLY FLAG THESE GENUINE CLARITY PROBLEMS:**
                
        #         **HIGH Severity :**
        #         - Undefined technical jargon not common in the industry
        #         - Contradictory requirements (e.g., "entry-level with 10+ years experience")
        #         - Essential information missing (salary range, work location, reporting structure)
        #         - Incomprehensible sentence structure or grammar
                
        #         **MEDIUM Severity :**
        #         - Industry acronyms without explanation in non-specialist roles
        #         - Vague qualification equivalencies without examples
        #         - Ambiguous time/travel commitments without specifics
                
        #         **DO NOT FLAG AS CLARITY ISSUES:**
        #         - Standard job description verbs: "seek", "require", "prefer", "prioritize"
        #         - Common industry terminology: "CRM", "SaaS", "lead generation", "client engagement"
        #         - Clear experience requirements: "5+ years experience", "advanced knowledge"
        #         - Professional skill descriptions: "strong relationship management", "pipeline management"
        #         - Standard qualification statements: "Bachelor's degree preferred"
        #         - Common soft skills: "attention to detail", "accuracy", "communication skills",
        #          "problem solving", "teamwork", "customer service", "time management"
                
        #         **CLARITY CHECK BEFORE FLAGGING:**
        #         - Would a typical job seeker in this industry understand this phrase?
        #         - Is the requirement actually confusing or just concise?
        #         - Does the unclear language genuinely prevent understanding job duties/requirements?
        #         - Would a typical job seeker in this industry fail to understand what is required?
        #         - Is the phrase so vague or contradictory that it blocks meaningful interpretation?
        #         - If the phrase is a common competency/soft skill (e.g., attention to detail, communication skills),
        #         - do NOT flag it as unclear, even if broad.
                
        #         **EXPLANATION TEMPLATE:** "This phrase is genuinely unclear and prevents candidates from understanding [specific job requirement/duty]. Consider clarifying [specific aspect]."
        
        
        #     **ENHANCED ANALYSIS RULES:**

        #     1. **CONTEXTUAL ANALYSIS PRIORITY:**
        #     - Read complete sentences, not isolated words Ex:If it is mentioned for "2025–2026 school year"
        #     - Consider industry-standard terminology
        #     - Evaluate job function relevance
        #     - Assess discriminatory intent vs. legitimate requirement

        #     2. **SEVERITY DETERMINATION:**
        #     - **High (0.8)**: Direct protected class exclusion, explicit bias
        #     - **Medium (0.4)**: Coded language, indirect bias, unclear requirements
        #     - **Low (0.1)**: Minor language issues, easily correctable phrasing

        #     3. **POSITIVE INCLUSIVITY INDICATORS (Reduce bias score):**
        #     - "all experience levels welcome"
        #     - "new grads and experienced professionals"
        #     - "diverse backgrounds encouraged"
        #     - "equal opportunity employer"
        #     - Accommodation language
        #     - Flexible work arrangements

        #     **Example Applications:**

        #     GOOD (Low/No Bias):
        #     - "Seeking entry-level to senior professionals" (Experience-based, inclusive)
        #     - "New graduates and experienced candidates welcome" (Inclusive across experience)
        #     - "Must be 21+ for alcohol service" (Legal requirement)

        #     PROBLEMATIC (Medium/High Bias):
        #     - "Looking for young, energetic team members" (Age-coded language)
        #     - "Digital natives preferred" (Age-coded)
        #     - "Must be native English speaker" (National origin bias)

        # **STEP 4: SCORING METHODOLOGY**


       

        ## **Bias Score:**(Consider the severity of issues related to biasness or inclusiveness ) Use the best known method to calculate this and by Python programming calculate the value.

        # **Inclusivity Score:**(Consider the severity of issues related to biasness or inclusiveness) Use the best known method to calculate this and by Python programming calculate the value.

        # **Clarity Score:** (Consider the severity of detected issues related to clarity) Use the best known method to calculate this and by Python programming calculate the value.



       

        # **CRITICAL RULES:** 
        # - Flag ONLY language that violates NY Human Rights Law Section 296 or CADA
        # - **ONLY flag issues that are actually present in the provided text - do not flag phantom or inferred content**
        # - **Before flagging any issue, verify the exact phrase exists in the job description text**
        # - Aggregate identical issues - report each unique phrase only once
        # - Consider job-relevance and bona fide occupational qualifications
        # - Focus clarity assessment on genuinely confusing/complicated terms only

        # Job Description:
        # {text}

        # **For job-related text, return structured JSON:**

        # {{
        #     "role": "job title",
        #     "industry": "industry name", 
        #     "issues": [
        #         {{
        #             "type": "age|age_disclosure|race_national_origin|gender|sexual_orientation_gender_identity|disability|pregnancy|criminal_history|religion|harassment_language|retaliation_risk|clarity",
        #             "text": "biased phrase",
        #             "start_index": 0,
        #             "end_index": 10,
        #             "severity": "low|medium|high",
        #             "explanation": "This violates [specific NY Human Rights Law section/CADA provision] which [specific protection/requirement]"
        #         }}
        #     ],
        #     "bias_score": 0.0,
        #     "inclusivity_score": 1.0,
        #     "clarity_score": 1.0,
        #     "overall_assessment": "Summary of findings with legal compliance context"
        # }}

        # **For non-job related text:**
        # {{
        #     "role": "N/A",
        #     "industry": "N/A",
        #     "issues": [],
        #     "bias_score": "N/A",
        #     "inclusivity_score": "N/A", 
        #     "clarity_score": "N/A",
        #     "overall_assessment": "The provided text does not appear to be a job description."
        # }}


        # 4. **Severity Guidelines**:
        # Apply the following strictly:
        # - **High Severity (0.8 weight):**
        #     - Direct exclusion/discrimination against a protected class  
        #     (e.g., “Lady Guard”, gender-based physical/height requirements,  
        #     “under 35 only”, “must be single”, “native English speaker only”).  
        #     - Explicit age/sex restrictions not tied to clear BFOQ.  
        #     - Blanket bans (e.g., “no disabilities”, “must be Christian”).  
        #     - Language likely unlawful under NYHRL §296 or CADA.  

        # - **Medium Severity (0.4 weight):**
        #     - Indirect discouraging language, but not outright exclusion  
        #     (e.g., “young & energetic”, “digital native”, “recent graduate”).  
        #     - Requirements that may disadvantage groups without being explicit  
        #     (e.g., “cultural fit”, unnecessary degree inflation).  
        #     - Ambiguity that creates potential bias but not categorical.  

        # - **Low Severity (0.1 weight):**
        #     - Minor wording issues that may subtly impact inclusivity  
        #     (e.g., “guys”, “chairman”, “he/she” instead of neutral pronouns).  
        #     - Jargon or clarity problems not tied to protected class.  
        #     - Easily correctable without strong legal risk.  


        # 5. **Scoring (Normalized 0.0–1.0):**
        # - Each issue has a base severity weight: High=0.8, Medium=0.4, Low=0.1.
        # - **Bias Score** = min(1.0, sum(weights) / max_possible).(**Only consider severity of Bias issues for calculation**) Normalize so the score always lies between 0.0 and 1.0.
        # - **Inclusivity Score** = 1.0 - Bias Score (but never below 0.0).
        # - **Clarity Score** = 1.0 if no genuine comprehension blockers; deduct proportionally but keep within 0.0–1.0.(**Only consider severity of Clarity issues for calculation**)
        # """
        bias_detection_prompt = f"""

        **CRITICAL JSON FORMATTING RULES:**
                - Return ONLY valid JSON - no extra text before or after
                - Ensure all strings are properly quoted
                - Ensure all JSON objects and arrays are properly closed
                - Use proper comma separation between all properties
                - Escape any quotes within string values using \"
                - Use \\n for line breaks within strings, not actual newlines
                - Escape backslashes as \\\\
                - NO control characters (tabs, actual newlines, etc.) in JSON strings


        Analyze the following text for job description bias under:
        - NY Human Rights Law (NYHRL §296) 
        - Colorado Anti-Discrimination Act (CADA, including 2024 Job Application Fairness Act)

        ### Steps:
        1. **Validation**: Confirm if input is a job description; else return N/A JSON.
        2. **Context**: Identify role, industry, and core functions.
        3. **Bias & Compliance Check**:
        - Protected classes: age, race/color/national origin (including hairstyles), religion/creed, sex/gender, sexual orientation, gender identity/expression, disability, pregnancy, familial/marital status, military/veteran (NY), citizenship/immigration (NY), domestic violence victim (NY), genetic traits (NY).
        - Colorado 2024 restrictions: employers may NOT ask for age, DOB, grad/attendance dates in initial apps (unless legally required BFOQ).
        - Only flag explicit/coded bias:
            - **Age**: "under 30", "young & energetic", "digital native".  
                OK: "3–5 years exp.", "entry/senior level", timelines like "2025–2026 school year".
            - **Race/National Origin**: "native English speaker", "cultural fit", hairstyle bans.  
            - **Gender**: gendered job titles, physical assumptions.  
            - **Sexual Orientation/GI**: heteronormative, binary-only pronouns.  
            - **Disability**: unnecessary physical traits ("perfect vision" for office role).  
            - **Pregnancy**: exclusions/lack of accommodation.  
            - **Criminal History**: blanket bans unrelated to role.  
            - **Religion**: required faith/holiday assumptions (unless religious org).  
            - **Harassment/Retaliation**: hostile/discouraging language.  
            - **Clarity**:Focus clarity assessment on genuinely confusing/complicated terms only, contradictory (e.g. entry-level w/10 yrs exp), missing essentials, jargon not standard.  
        - **Do NOT flag**: legal certifications, true BFOQ (safety, law), professional skills, soft skills (teamwork, communication).
        - Inclusivity indicators (reduce bias): "all levels welcome", "EOE", "diverse backgrounds encouraged", accommodations.
        - Aggregate identical issues - report each unique phrase only once

        4. **Severity Guidelines**:
        Apply the following strictly:
        - **High Severity (0.8 weight):**
            - Direct exclusion/discrimination against a protected class  
            (e.g., "Lady Guard", gender-based physical/height requirements,  
            "under 35 only", "must be single", "native English speaker only").  
            - Explicit age/sex restrictions not tied to clear BFOQ.  
            - Blanket bans (e.g., "no disabilities", "must be Christian").  
            - Language likely unlawful under NYHRL §296 or CADA.  

        - **Medium Severity (0.4 weight):**
            - Indirect discouraging language, but not outright exclusion  
            (e.g., "young & energetic", "digital native", "recent graduate").  
            - Requirements that may disadvantage groups without being explicit  
            (e.g., "cultural fit", unnecessary degree inflation).  
            - Ambiguity that creates potential bias but not categorical.  

        - **Low Severity (0.1 weight):**
            - Minor wording issues that may subtly impact inclusivity  
            (e.g., "guys", "chairman", "he/she" instead of neutral pronouns).  
            - Jargon or clarity problems not tied to protected class.  
            - Easily correctable without strong legal risk.  

        5. **Scoring (Normalized 0.0–1.0):**
        Each issue has a base severity weight: High=0.8, Medium=0.4, Low=0.1.
        
        **Max Possible Values for Normalization:**
        - Simple JD (1-2 pages): 2.0
        - Standard JD (2-3 pages): 3.0  
        - Complex JD (3+ pages): 4.0
        
        **Bias Score Calculation:**
        - Only consider bias issues: age, race, gender, sexual_orientation, disability, pregnancy, criminal_history, religion, harassment, retaliation
        - Formula: min(1.0, sum(bias issue weights) / max_possible)
        - Normalize so score always lies between 0.0 and 1.0
        
        **Inclusivity Score Calculation:**
        - Formula: max(0.0, 1.0 - Bias Score)
        - Never below 0.0
        
        **Clarity Score Calculation:**
        - Only consider clarity issues  
        - Formula: max(0.0, 1.0 - sum(clarity issue weights) / max_possible_clarity)
        - Deduct proportionally but keep within 0.0–1.0 range


        ### Output JSON:
        If job description:
        {{
        "role": "...",
        "industry": "...",
        "issues": [
            {{
            "type": "age|race|gender|sexual_orientation|disability|pregnancy|criminal_history|religion|harassment|retaliation|clarity",
            "text": "...",
            "start_index": 0,
            "end_index": 10,
            "severity": "low|medium|high",
            "explanation": "Proper reason with (full form of law names Ex:NYHRL:New york human rights law) law reference (e.g. violates NYHRL §296(1)(a) or CADA )"
            }}
        ],
        "bias_score": 0.0,
        "inclusivity_score": 1.0,
        "clarity_score": 1.0,
        "overall_assessment": "Concise compliance summary"
        }}

        If NOT a job description:
        {{
        "role": "N/A",
        "industry": "N/A",
        "issues": [],
        "bias_score": "N/A",
        "inclusivity_score": "N/A",
        "clarity_score": "N/A",
        "overall_assessment": "Not a job description"
        }}

        Job Description:
        {text}
        """

        
        
        try:
            response = self.model.generate_content(
                bias_detection_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=8000,  
                )
            )

            print(f"Raw response: {response}")

            # ---- Safe text extraction ----
            response_text = ""
            if hasattr(response, "candidates") and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, "content") and hasattr(candidate.content, "parts"):
                    response_text = "".join(
                        getattr(part, "text", "") for part in candidate.content.parts
                    ).strip()

            if not response_text:
                raise ValueError("No text content returned by Gemini")

            # ---- Clean JSON output ----
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                # fallback: extract JSON via regex
                import re
                json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    raise

            print(f"Cleaned result: {result}")
            return result



            
     

        except Exception as e:
            error_msg = str(e)
            print(f"Error in bias detection: {error_msg}")
            
            # Check for specific Gemini API errors
            if "503" in error_msg or "overloaded" in error_msg.lower():
                raise HTTPException(
                    status_code=503,
                    detail="AI service is temporarily overloaded. Please try again in a few moments."
                )
            elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                raise HTTPException(
                    status_code=429,
                    detail="API quota exceeded. Please try again later."
                )
            elif "timeout" in error_msg.lower() or "exceeded" in error_msg.lower():
                raise HTTPException(
                    status_code=504,
                    detail="Request timed out. The AI service is taking longer than expected. Please try again."
                )
           
            elif "authentication" in error_msg.lower() or "api key" in error_msg.lower():
                raise HTTPException(
                    status_code=500,
                    detail="Service configuration error. Please contact support."
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"AI analysis failed: {error_msg}"
                )
            

       
    
    async def improve_language(self, text: str, detected_issues: List[Dict] = None) -> Dict:
        """Use Gemini to suggest language improvements with context from detected issues"""
        
        # Format detected issues for the prompt
        issues_context = ""
        if detected_issues and len(detected_issues) > 0:
            formatted_issues = []
            for issue in detected_issues:
                formatted_issues.append(
                    f"- Type: {issue['type']}\n"
                    f"  Text: '{issue['text']}'\n"
                    f"  Severity: {issue['severity']}\n"
                    f"  Explanation: {issue['explanation']}\n"
                )
            issues_context = "\nDetected Issues:\n" + "".join(formatted_issues)

        print(f"Detected issues context for improve language: {issues_context or 'NONE'}")

       
        
        improvement_prompt = f"""

                **CRITICAL JSON FORMATTING RULES:**
                - Return ONLY valid JSON - no extra text before or after
                - Ensure all strings are properly quoted
                - Ensure all JSON objects and arrays are properly closed
                - Use proper comma separation between all properties
                - Escape any quotes within string values using \"
                - Use \\n for line breaks within strings, not actual newlines
                - Escape backslashes as \\\\
                - NO control characters (tabs, actual newlines, etc.) in JSON strings
               
                **At first check that the job description is related to the particular job role and industry and fulfill the requirements of the job description then do the following**
                
                Improve the following job description for:
                **ONLY address the specific issues found in the issues_context below. DO NOT make any other improvements, suggestions, or changes to the job description.**
                **STRICT RULE: If issues_context is empty or contains no issues, return an empty suggestions array
                
                1. SEO optimization with relevant keywords (Suggest ONLY keywords that are relevant to the job description and are STRICTLY NOT present anywhere in the original text - perform thorough analysis to ensure complete absence)
                2. Brevity and conciseness

                **CRITICAL IMPROVEMENT RULES:**
                - (IMPORTANT) Only Provide the suggestions for the issues that are present in the issues_context only
                - If it is mentioned that no education requirements are needed or no graduation is required then add this in the **OUR IDEAL CANDIDATE** section: "No formal education requirements are needed for this role"
                - Mention the education requirements in the **OUR IDEAL CANDIDATE** section if it is mentioned in the original job description
                - Add all the skills that are present in the original job description in the **REQUIRED SKILLS** section do not miss any skills that are present in the original job description
                - If it is mentioned that no experience is needed then add this in the **OUR IDEAL CANDIDATE** section: "No prior experience is required for this role, but relevant skills and enthusiasm are essential."
                - Add the required experience in the **OUR IDEAL CANDIDATE** section if it is mentioned in the original job description
                - FLAG LANGUAGE THAT EXCLUDES QUALIFIED CANDIDATES WITHOUT JOB-RELATED JUSTIFICATION
                - 
                - FOR CLARITY ISSUES: Focus on ambiguous eligibility language that obscures pathways for internationally trained professionals
                

                Original Job Description:
                {text}

                {issues_context}

                **Analysis Instructions:**

                1. Identify job role and industry context first
                1a.**(Strict instruction)** Only Provide the suggestions for the issues that are present in the issues_context only (If issues_context is empty, return empty suggestions)
                2. Do NOT identify or fix any additional issues not already detected
                2a.If the issue type is marked as "clarity" in the issues_context then in suggestions catogory use "clarity" and if the issue type is marked other than clarity in the issues_context then in suggestions category use "inclusivity"
                3. Do NOT make general improvements to style, tone, or formatting
                4. Verify if requirements match industry standards (e.g., Colorado dental board for DDS/DMD)
                5. Maintain professional tone while improving inclusivity( **DO NOT** make general improvements to tone, style, or formatting unless specifically flagged in issues_context)
                6. Never flag licensure-mandated terms (e.g., "DDS/DMD", "RN license") as elitism
                7. Suggest ONLY keywords that are relevant to the job description and are STRICTLY NOT present in the Original Job Description - analyze the original text thoroughly to ensure none of the suggested keywords appear anywhere in the original content
                8. Frame the sentences using the seo_keywords that you have found in the previous step and use them in the improved text. CRITICAL: When incorporating these keywords into the text, write them as plain text without any ** or * formatting. For example, if the keyword is "Patient Care", write it as "Patient Care" NOT as "**Patient Care**". IMPORTANT: Only use keywords that are completely absent from the original job description.
                9. DO NOT use any markdown formatting (**, *, etc.) within the content text - ONLY use ** for the section headers as specified in the format below. All keywords and content must be written in plain text without any bold or italic formatting.
                
                **IMPROVED TEXT FORMATTING REQUIREMENTS:**
                The improved job description must follow this exact structure and format (keep the ** around section headers):
                **Rewrite the sentences with (removing the bias and inclusivity issues) some diffrent writting style dont just copy the exact sentences in the KEY RESPONSIBILITIES and OUR IDEAL CANDIDATE sections**

                **IMPORTANT: In the improved_text field, use \\n for line breaks, not actual newlines. Format like this:**
                "**JOB TITLE:** [Clear, specific job title]\\n\\n**COMPANY:** [Company name]\\n\\n**INDUSTRY:** [Industry]\\n\\n..."
                
                **JOB TITLE:** [Clear, specific job title]
                
                **COMPANY:** [Company name if provided, otherwise "Company Name"]
                
                **INDUSTRY:** [Specific industry/sector]
                
                **LOCATION:** [Work location/type - Remote/On-site/Hybrid]
                
                **EMPLOYMENT TYPE:** [Full-time/Part-time/Contract/Internship]
                
                **JOB SUMMARY:**
                [6-7 sentences providing an engaging overview of the role and its impact]
                
                **KEY RESPONSIBILITIES:**
                • [Responsibility 1 - action-oriented, specific]
                • [Responsibility 2 - action-oriented, specific]
                • [Responsibility 3 - action-oriented, specific]
                • [Additional responsibilities as needed]
                
                **OUR IDEAL CANDIDATE:**
                • [Essential qualification 1]
                • [Essential qualification 2]
                • [Essential qualification 3]
                • [Additional essential qualifications]
                
                **PREFERRED QUALIFICATIONS:**
                • [Preferred qualification 1]
                • [Preferred qualification 2]
                • [Additional preferred qualifications]
                
                **REQUIRED SKILLS:**
                • [Technical skill 1]
                • [Technical skill 2]
                • [Soft skill 1]
                • [Soft skill 2]
                • [Additional skills]
                
                **WHAT WE OFFER:**
                • [Benefit 1]
                • [Benefit 2]
                • [Benefit 3]
                • [Additional benefits]
                
                **APPLICATION PROCESS:**
                [Brief, clear instructions on how to apply]
                
                Return ONLY a valid JSON response (no additional text and extra markdowns):
                {{
                    "suggestions": [
                        {{
                            "original": "original phrase",
                            "improved": "improved phrase",
                            "rationale": "The actual reason why this is better",
                            "category": "clarity|inclusivity"
                        }}
                    ],
                    "seo_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5" - ENSURE these keywords are completely absent from the original job description],
                    "improved_text": "[Complete rewritten job description using the SEO keywords and improved version in the suggestions identified above also following the EXACT structure outlined above. Maintain all original context while improving clarity, brevity, inclusivity, and SEO optimization. Use the specific headers with ** formatting and bullet point format as specified. Keep section headers with ** but write ALL CONTENT INCLUDING KEYWORDS in plain text without any markdown formatting. Example: write 'Patient Care' not '**Patient Care**'.]",
                    
                    
                }}
                
                **If the provided text is not related to a job description and does not fulfill the requirements of job descriptions then do the following**
                Return ONLY a valid JSON response (no additional text):
                {{
                    "suggestions": [],
                    "improved_text": "N/A - The provided text does not appear to be a job description or does not contain sufficient job-related information to generate an improved version.",
                    "seo_keywords": []
                }}
            """
        
        
        
        try:
            response = self.model.generate_content(
                improvement_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=9000,  # increase if you still see cutoff
                )
            )

            print(f"Raw response from improve language function: {response}")

            # ---- Safe text extraction ----
            response_text = ""
            if hasattr(response, "candidates") and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, "content") and hasattr(candidate.content, "parts"):
                    response_text = "".join(
                        getattr(part, "text", "") for part in candidate.content.parts
                    ).strip()
            

            if not response_text:
                raise ValueError("No text content returned by Gemini")

            # ---- Clean JSON formatting ----
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            print("==== Raw JSON response ====")
            print(response_text)

            # ---- Try parsing JSON ----
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                import re
                json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    raise

            print(f"Cleaned result from improve language: {result}")
            return result    
       

        except Exception as e:
            error_msg = str(e)
            print(f"Error in language improvement: {error_msg}")
            
            # Check for specific Gemini API errors
            if "503" in error_msg or "overloaded" in error_msg.lower():
                raise HTTPException(
                    status_code=503,
                    detail="AI service is temporarily overloaded. Please try again in a few moments."
                )
            elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                raise HTTPException(
                    status_code=429,
                    detail="API quota exceeded. Please try again later."
                )
            elif "timeout" in error_msg.lower() or "exceeded" in error_msg.lower():
                raise HTTPException(
                    status_code=504,
                    detail="Request timed out. The AI service is taking longer than expected. Please try again."
                )
            
            elif "authentication" in error_msg.lower() or "api key" in error_msg.lower():
                raise HTTPException(
                    status_code=500,
                    detail="Service configuration error. Please contact support."
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"AI analysis failed: {error_msg}"
                )