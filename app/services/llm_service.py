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

        # # Configure Google Gemini
        # api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        # if not api_key:
        #     raise ValueError("GOOGLE_GEMINI_API_KEY not found in environment variables")

        # Configure Google Gemini
        genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    async def detect_bias(self, text: str) -> Dict:
        """Use Gemini to detect bias in job description"""
       
       

      
        # bias_detection_prompt = f"""
        #         At first check that the job description is related to the particular job role and industry and fulfill the requirements of the job description then do the following
        #         Analyze the following text for job description bias. Follow this structured approach:

        #         **STEP 1: VALIDATION**
        #         Determine if the text is a job description. If not, return N/A response format.

        #         **STEP 2: CONTEXT ANALYSIS** 
        #         Identify the job role, industry, and core functions to distinguish legitimate requirements from bias.

        #         **STEP 3: BIAS DETECTION**
                
        #         Scan for these bias types, considering job relevance. IMPORTANT: Only flag language that EXCLUDES qualified candidates WITHOUT job-related justification:

        #         1. **Gender Bias**: Gendered language not required for job function
        #         - BIASED: "salesman", "aggressive", "dominant leader", "rockstar developer", "ninja developer"
        #         - IMPROVED: "salesperson", "bold", "effective leader", "skilled developer", "expert developer"
        #         - LEGITIMATE: "confident patient care", "strong clinical skills", "assertive communication" for leadership roles

        #         2. **Age Bias**: Age requirements without job justification
        #         - BIASED: "young and energetic", "digital native", "recent graduate only", "new graduates", "millennial mindset"
        #         - IMPROVED: "passionate and motivated", "person passionate about technology", "graduates", "early-career professional"
        #         - LEGITIMATE: "5+ years experience", "senior-level position", "entry-level role"

        #         **2a. Age Information Disclosure Bias (Job Application Fairness Act Compliance)**: Requesting age-related information inappropriately
        #         - PROHIBITED: Asking for "age", "date of birth", "graduation dates", "dates of attendance at educational institution" on initial applications
        #         - BIASED: "Please provide graduation year", "Date of birth required", "Age verification needed upfront"
        #         - LEGITIMATE: Age verification only for bona fide occupational qualifications (safety roles, legal requirements), allowing redaction of age-identifying information in transcripts/certifications
        #         - COMPLIANT: "Age verification required only if position necessitates per legal/safety requirements", "Transcripts accepted with age-related information redacted"

        #         3. **Racial/Cultural Bias**: Cultural assumptions not job-relevant
        #         - BIASED: "native English speaker", "pow wow", "nitty gritty", "cultural fit" without specifics
        #         - IMPROVED: "fluent English speaker", "meet and greet", "details", "team collaboration skills"
        #         - LEGITIMATE: "Hindi fluency for Hindi teacher", "bilingual for international role", specific language skills

        #         4. **Disability Bias**: Physical requirements unnecessary for job
        #         - BIASED: "perfect vision" for desk job, "must stand" for remote work, "typing", "walking"
        #         - IMPROVED: "attention to detail", "available during work hours", "inputting", "moving"
        #         - LEGITIMATE: "lifting 50lbs" for warehouse, "clear vision" for driver, "manual dexterity" for surgeon

        #         5. **LGBTQ+ Bias**: Gendered assumptions or heteronormative language
        #         - BIASED: "he/she" references, "maternity leave" only, assumptions about family structures
        #         - IMPROVED: "team member", "they", "parental leave", "family leave"
        #         - LEGITIMATE: Gender-specific roles where legally required

        #         6. **Former Felons Bias**: Automatic exclusion based on criminal history
        #         - BIASED: "no criminal history", "convicted felon", "criminal history check"
        #         - IMPROVED: "background check as required by law", "former felon", "background verification"
        #         - LEGITIMATE: Legal requirements for specific roles (financial, childcare)

        #         7. **Elitism Bias**: Educational or social class assumptions
        #         - BIASED: "bachelor's degree from top university", "MBA from top business school", "prestigious institution only"
        #         - IMPROVED: "bachelor's degree", "MBA", "accredited institution"
        #         - LEGITIMATE: Specific accreditation requirements for professional roles 
        #         - CRITICAL: Do NOT flag standard professional degrees required by licensing boards (e.g., DDS/DMD for dentists, RN for nurses)
                
        #         8. **Mental Health Bias**: Language that stigmatizes mental health conditions
        #         - BIASED: "sanity check", "crazy hours", "high-stress environment only"
        #         - IMPROVED: "review", "audit", "flexible hours", "fast-paced environment"
        #         - LEGITIMATE: Genuine stress tolerance requirements with support systems

        #         9. **Religion Bias**: Religious assumptions or preferences
        #         - BIASED: References to specific religious holidays, practices, or beliefs as requirements
        #         - IMPROVED: "flexible holiday schedule", "respectful of all beliefs"
        #         - LEGITIMATE: Religious organizations with bona fide occupational qualifications

        #         10. **Socioeconomic Bias**: Class-based assumptions not job-relevant
        #         - BIASED: "own car" for remote work, "elite background", specific lifestyle requirements
        #         - IMPROVED: "reliable transportation when required", "relevant background"
        #         - LEGITIMATE: "valid license" for driver, actual job-related requirements

        #         11. **Clarity Issues**: Unclear or ambiguous content that confuses candidates
        #         - UNCLEAR: "handle various tasks", "other duties as assigned" without context, undefined jargon
        #         - ADD: Ambiguous eligibility language that obscures pathways for internationally trained professionals
        #         - CLEAR: Specific responsibilities, defined terms, concrete expectations

        #         12. **General Inclusivity Issues**: Language that unnecessarily excludes candidates
        #         - EXCLUSIVE: "must work 24/7", "no accommodations", excessive requirements for entry-level roles
        #         - INCLUSIVE: "reasonable accommodations available", "flexible schedule considered", specific role needs

        #         **DO NOT PENALIZE:**
        #         - Whatever job role you find above, you must know the basic requirements of that job role. Examples: 
        #             - Security guards or police officers needing physical fitness requirements
        #             - Janitors or maintenance workers needing ability to lift, bend, or stand for extended periods
        #             - Medical roles (doctors, nurses, surgeons) needing clinical confidence, steady hands, or ability to work under pressure
        #             - Teachers needing classroom management skills and patience with students
        #             - Sales roles needing strong communication and persuasion abilities
        #             - Construction workers needing physical strength and safety awareness
        #             - Pilots needing excellent vision and quick decision-making skills
        #             - Chefs needing ability to work in hot environments and handle kitchen equipment
        #             - Customer service roles needing patience and conflict resolution skills
        #             - Drivers needing valid license and clean driving record
        #             - Accountants needing attention to detail and numerical accuracy
        #             - IT roles needing specific technical certifications or programming languages
        #             - Healthcare workers needing specific medical certifications and ability to handle bodily fluids
        #             - Firefighters needing physical fitness and ability to work in dangerous conditions
        #             - Childcare workers needing background checks and patience with children
        #         - Standard professional terms: "confident", "independent", "strong", "leadership", "competitive", "dedicated"
        #         - Industry-appropriate requirements
        #         - Legitimate qualifications: teaching credentials, technical certifications, relevant experience

        #         **STEP 4: SCORING**

        #         **Bias Score:** Use the best known method to calculate this and by Python programming calculate the value.

        #         **Inclusivity Score:** Use the best known method to calculate this and by Python programming calculate the value.

        #         **Clarity Score:** Use the best known method to calculate this and by Python programming calculate the value.

        #         **CRITICAL RULE:** 
        #             **CRITICAL RULES:**
        #             - Only flag requirements that exclude candidates WITHOUT job-related justification.
        #             - In issues if the same biased phrase comes more than once so do not repeat it in the issues list, just mention it once with the start and end index of the first occurrence.
        #             - DO NOT flag standard professional requirements that are job-relevant
        #             - DO NOT suggest adding elements that weren't originally present (e.g., don't suggest adding education requirements if none were mentioned)
        #             - Standard professional terms are acceptable: "confident", "independent", "strong", "leadership", "competitive", "dedicated"

        #         Job Description:
        #         {text}
                

        #             **For job related text, return a structured JSON response:**
        #             Return ONLY valid JSON with calculated scores:

        #             {{
        #                 "role": "job title",
        #                 "industry": "industry name", 
        #                 "issues": [
        #                     {{
        #                         "type": "gender|age|age_disclosure|racial|cultural|disability|lgbtq|former_felons|elitism|mental_health|religion|socioeconomic|clarity|inclusivity",
        #                         "text": "biased phrase",
        #                         "start_index": 0,
        #                         "end_index": 10,
        #                         "severity": "low|medium|high",
        #                         "explanation": "why this is biased and not job-relevant in simpler terms "
                                
        #                     }}
        #                 ],
        #                 "bias_score": 0.0,
        #                 "inclusivity_score": 1.0,
        #                 "clarity_score": 1.0,
        #                 "overall_assessment": "summary of findings considering job context"
        #             }}

        #             **For non-job related text, return this JSON:**
        #             {{
        #                 "role": "N/A",
        #                 "industry": "N/A",
        #                 "issues": [],
        #                 "bias_score": "N/A",
        #                "inclusivity_score": "N/A", 
        #                 "clarity_score": "N/A",
        #                 "overall_assessment": "The provided text does not appear to be a job description."
        #         }}
        # """
        
        bias_detection_prompt = f"""
        At first check that the job description is related to the particular job role and industry and fulfill the requirements of the job description then do the following
        Analyze the following text for job description bias. Follow this structured approach:

        **STEP 1: VALIDATION**
        Determine if the text is a job description. If not, return N/A response format.

        **STEP 2: CONTEXT ANALYSIS** 
        Identify the job role, industry, and core functions to distinguish legitimate requirements from bias.

        **STEP 3: BIAS DETECTION**

        **DO NOT PENALIZE:**
        - Whatever job role you find above, you must know the basic requirements of that job role. Examples: 
            - Security guards or police officers needing physical fitness requirements
            - Janitors or maintenance workers needing ability to lift, bend, or stand for extended periods
            - Medical roles (doctors, nurses, surgeons) needing clinical confidence, steady hands, or ability to work under pressure
            - Teachers needing classroom management skills and patience with students
            - Sales roles needing strong communication and persuasion abilities
            - Construction workers needing physical strength and safety awareness
            - Pilots needing excellent vision and quick decision-making skills
            - Chefs needing ability to work in hot environments and handle kitchen equipment
            - Customer service roles needing patience and conflict resolution skills
            - Drivers needing valid license and clean driving record
            - Accountants needing attention to detail and numerical accuracy
            - IT roles needing specific technical certifications or programming languages
            - Healthcare workers needing specific medical certifications and ability to handle bodily fluids
            - Firefighters needing physical fitness and ability to work in dangerous conditions
            - Childcare workers needing background checks and patience with children
        - Standard professional terms: "confident", "independent", "strong", "leadership", "competitive", "dedicated"
        - Industry-appropriate requirements
        - Legitimate qualifications: teaching credentials, technical certifications, relevant experience

        Scan for these bias types, considering job relevance. IMPORTANT: Only flag language that EXCLUDES qualified candidates WITHOUT job-related justification:

        1. **Gender Bias**: Gendered language not required for job function
        - BIASED: "salesman", "aggressive", "dominant leader", "rockstar developer", "ninja developer"
        - IMPROVED: "salesperson", "bold", "effective leader", "skilled developer", "expert developer"
        - LEGITIMATE: "confident patient care", "strong clinical skills", "assertive communication" for leadership roles

        2. **Age Bias**: Age requirements without job justification
        - BIASED: "young and energetic", "digital native", "recent graduate only", "new graduates", "millennial mindset"
        - IMPROVED: "passionate and motivated", "person passionate about technology", "graduates", "early-career professional"
        - LEGITIMATE: "5+ years experience", "senior-level position", "entry-level role"

        **2a. Age Information Disclosure Bias (Job Application Fairness Act Compliance)**: Requesting age-related information inappropriately
        - PROHIBITED: Asking for "age", "date of birth", "graduation dates", "dates of attendance at educational institution" on initial applications
        - BIASED: "Please provide graduation year", "Date of birth required", "Age verification needed upfront"
        - LEGITIMATE: Age verification only for bona fide occupational qualifications (safety roles, legal requirements), allowing redaction of age-identifying information in transcripts/certifications
        - COMPLIANT: "Age verification required only if position necessitates per legal/safety requirements", "Transcripts accepted with age-related information redacted"

        3. **Racial/Cultural Bias**: Cultural assumptions not job-relevant
        - BIASED: "native English speaker", "pow wow", "nitty gritty", "cultural fit" without specifics
        - IMPROVED: "fluent English speaker", "meet and greet", "details", "team collaboration skills"
        - LEGITIMATE: "Hindi fluency for Hindi teacher", "bilingual for international role", specific language skills

        4. **Disability Bias**: Physical requirements unnecessary for job
        - BIASED: "perfect vision" for desk job, "must stand" for remote work, "typing", "walking"
        - IMPROVED: "attention to detail", "available during work hours", "inputting", "moving"
        - LEGITIMATE: "lifting 50lbs" for warehouse, "clear vision" for driver, "manual dexterity" for surgeon

        5. **LGBTQ+ Bias**: Gendered assumptions or heteronormative language
        - BIASED: "he/she" references, "maternity leave" only, assumptions about family structures
        - IMPROVED: "team member", "they", "parental leave", "family leave"
        - LEGITIMATE: Gender-specific roles where legally required

        6. **Former Felons Bias**: Automatic exclusion based on criminal history
        - BIASED: "no criminal history", "convicted felon", "criminal history check"
        - IMPROVED: "background check as required by law", "former felon", "background verification"
        - LEGITIMATE: Legal requirements for specific roles (financial, childcare)

        7. **Elitism Bias**: Educational or social class assumptions
        - ONLY flag if the requirement EXCLUDES candidates without a certain level of education or specific institution, AND the requirement is not clearly justified by job duties or legal necessity.
        - DO NOT FLAG if the text explicitly states that education is "not required", "no high school diploma", "no GED", "no degree", "not necessary", or similar negation.
        - BIASED: "bachelor's degree from top university", "MBA from top business school", "prestigious institution only"
        - IMPROVED: "bachelor's degree", "MBA", "accredited institution"
        - LEGITIMATE: Specific accreditation requirements for professional roles 
        - CRITICAL: Do NOT flag standard professional degrees required by licensing boards (e.g., DDS/DMD for dentists, RN for nurses)

        8. **Mental Health Bias**: Language that stigmatizes mental health conditions
        - BIASED: "sanity check", "crazy hours", "high-stress environment only"
        - IMPROVED: "review", "audit", "flexible hours", "fast-paced environment"
        - LEGITIMATE: Genuine stress tolerance requirements with support systems

        9. **Religion Bias**: Religious assumptions or preferences
        - BIASED: References to specific religious holidays, practices, or beliefs as requirements
        - IMPROVED: "flexible holiday schedule", "respectful of all beliefs"
        - LEGITIMATE: Religious organizations with bona fide occupational qualifications

        10. **Socioeconomic Bias**: Class-based assumptions not job-relevant
        - BIASED: "own car" for remote work, "elite background", specific lifestyle requirements
        - IMPROVED: "reliable transportation when required", "relevant background"
        - LEGITIMATE: "valid license" for driver, actual job-related requirements

        11. **Clarity Issues**: Unclear or ambiguous content that confuses candidates
        - UNCLEAR: "handle various tasks", "other duties as assigned" without context, undefined jargon
        - ADD: Ambiguous eligibility language that obscures pathways for internationally trained professionals
        - CLEAR: Specific responsibilities, defined terms, concrete expectations

        12. **General Inclusivity Issues**: Language that unnecessarily excludes candidates
        - EXCLUSIVE: "must work 24/7", "no accommodations", excessive requirements for entry-level roles
        - INCLUSIVE: "reasonable accommodations available", "flexible schedule considered", specific role needs


        **STEP 4: SCORING**

        **Bias Score:**(Consider the severity of issues related to biasness or inclusiveness ) Use the best known method to calculate this and by Python programming calculate the value.

        **Inclusivity Score:**(Consider the severity of issues related to biasness or inclusiveness) Use the best known method to calculate this and by Python programming calculate the value.

        **Clarity Score:** Use the best known method to calculate this and by Python programming calculate the value.

        **CRITICAL RULES:** 
            - Only flag requirements that exclude candidates WITHOUT job-related justification.
            - **AGGREGATE IDENTICAL ISSUES: For any exact phrase (case-sensitive), report ONLY the FIRST occurrence. Never duplicate issues for the same text.**
            - **TYPE ACCURACY: Match issues STRICTLY to the 12 bias types defined above. Never invent new types.**
            - DO NOT flag standard professional requirements that are job-relevant
            - DO NOT suggest adding elements that weren't originally present (e.g., don't suggest adding education requirements if none were mentioned)
            - Standard professional terms are acceptable: "confident", "independent", "strong", "leadership", "competitive", "dedicated"

        Job Description:
        {text}

        **For job related text, return a structured JSON response:**
        Return ONLY valid JSON with calculated scores:

        {{
            "role": "job title",
            "industry": "industry name", 
            "issues": [
                {{
                    "type": "gender|age|age_disclosure|racial|cultural|disability|lgbtq|former_felons|elitism|mental_health|religion|socioeconomic|clarity|inclusivity",
                    "text": "biased phrase",
                    "start_index": 0,
                    "end_index": 10,
                    "severity": "low|medium|high",
                    "explanation": "Explain in simple terms why this phrase may show bias, how it could unfairly exclude certain candidates, and why it might not be directly relevant to the job's core tasks."
                    
                }}
            ],
            "bias_score": 0.0,
            "inclusivity_score": 1.0,
            "clarity_score": 1.0,
            "overall_assessment": "summary of findings considering job context"
        }}

        **For non-job related text, return this JSON:**
        {{
            "role": "N/A",
            "industry": "N/A",
            "issues": [],
            "bias_score": "N/A",
            "inclusivity_score": "N/A", 
            "clarity_score": "N/A",
            "overall_assessment": "The provided text does not appear to be a job description."
        }}
        """
        
        
        try:
            response = self.model.generate_content(
                bias_detection_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=2048,
                )
            )
            
            # Clean the response text to extract JSON
            response_text = response.text.strip()
            
            # Remove any markdown formatting if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            result = json.loads(response_text)
            print(f"Cleaned result from detect bias function: {result}")
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
    
    async def improve_language(self, text: str) -> Dict:
        """Use Gemini to suggest language improvements"""
        
        
        # improvement_prompt = f"""
        #         **At first check that the job description is related to the particular job role and industry and fulfill the requirements of the job description then do the following**
                
        #         Improve the following job description for:
        #         1. Clarity and readability
        #         2. Inclusive language
        #         3. Brevity and conciseness
        #         4. Professional tone
        #         5. SEO optimization with relevant keywords (Suggest ONLY keywords that are relevant to the job description and are STRICTLY NOT present anywhere in the original text - perform thorough analysis to ensure complete absence)
                
        #         **CRITICAL IMPROVEMENT RULES:**
        #         - If it is mentioned that no education requirements are needed or no graduation is required then add this in the **REQUIRED QUALIFICATIONS** section: "No formal education requirements are needed for this role"
        #         - Add all the skills that are presnet in the original job description in the **REQUIRED SKILLS** section do not miss any skills that are present in the original job description
        #         - If it is mentioned that no experience is needed then add this in the **REQUIRED QUALIFICATIONS** section: "No prior experience is required for this role, but relevant skills and enthusiasm are essential."
                


        #         Original Job Description:
        #         {text}

        #         **Analysis Instructions:**
        #         1. Identify job role and industry context first
        #         2. Distinguish between legitimate professional requirements and actual bias
        #         3. Only suggest improvements for genuinely problematic language
        #         4. Maintain professional tone while improving inclusivity
        #         5. DO NOT flag or penalize standard professional language unless clearly discriminatory
        #         6.Suggest ONLY keywords that are relevant to the job description and are STRICTLY NOT present in the Original Job Description - analyze the original text thoroughly to ensure none of the suggested keywords appear anywhere in the original content
        #         7.Frame the sentences using the seo_keywords that you have found in the previous step and use them in the improved text. CRITICAL: When incorporating these keywords into the text, write them as plain text without any ** or * formatting. For example, if the keyword is "Patient Care", write it as "Patient Care" NOT as "**Patient Care**". IMPORTANT: Only use keywords that are completely absent from the original job description.
        #         8. DO NOT use any markdown formatting (**, *, etc.) within the content text - ONLY use ** for the section headers as specified in the format below. All keywords and content must be written in plain text without any bold or italic formatting.
                
        #         **IMPROVED TEXT FORMATTING REQUIREMENTS:**
        #         The improved job description must follow this exact structure and format (keep the ** around section headers):
                
        #         **JOB TITLE:** [Clear, specific job title]
                
        #         **COMPANY:** [Company name if provided, otherwise "Company Name"]
                
        #         **INDUSTRY:** [Specific industry/sector]
                
        #         **LOCATION:** [Work location/type - Remote/On-site/Hybrid]
                
        #         **EMPLOYMENT TYPE:** [Full-time/Part-time/Contract/Internship]
                
        #         **JOB SUMMARY:**
        #         [6-7 sentences providing an engaging overview of the role and its impact]
                
        #         **KEY RESPONSIBILITIES:**
        #         • [Responsibility 1 - action-oriented, specific]
        #         • [Responsibility 2 - action-oriented, specific]
        #         • [Responsibility 3 - action-oriented, specific]
        #         • [Additional responsibilities as needed]
                
        #         **REQUIRED QUALIFICATIONS:**
        #         • [Essential qualification 1]
        #         • [Essential qualification 2]
        #         • [Essential qualification 3]
        #         • [Additional essential qualifications]
                
        #         **PREFERRED QUALIFICATIONS:**
        #         • [Preferred qualification 1]
        #         • [Preferred qualification 2]
        #         • [Additional preferred qualifications]
                
        #         **REQUIRED SKILLS:**
        #         • [Technical skill 1]
        #         • [Technical skill 2]
        #         • [Soft skill 1]
        #         • [Soft skill 2]
        #         • [Additional skills]
                
        #         **WHAT WE OFFER:**
        #         • [Benefit 1]
        #         • [Benefit 2]
        #         • [Benefit 3]
        #         • [Additional benefits]
                
        #         **APPLICATION PROCESS:**
        #         [Brief, clear instructions on how to apply]
                
        #         Return ONLY a valid JSON response (no additional text and extra markdowns):
        #         {{
        #             "suggestions": [
        #                 {{
        #                     "original": "original phrase",
        #                     "improved": "improved phrase",
        #                     "rationale": "why this is better",
        #                     "category": "clarity|inclusivity"
        #                 }}
        #             ],
        #             "seo_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5 - ENSURE these keywords are completely absent from the original job description"],
        #             "improved_text": "[Complete rewritten job description using the SEO keywords identified above also following the EXACT structure outlined above. Maintain all original context while improving clarity, inclusivity, and SEO optimization. Use the specific headers with ** formatting and bullet point format as specified. Keep section headers with ** but write ALL CONTENT INCLUDING KEYWORDS in plain text without any markdown formatting. Example: write 'Patient Care' not '**Patient Care**'.]",
                    
                    
        #         }}
                
        #         **If the provided text is not related to a job description and does not fulfill the requirements of job descriptions then do the following**
        #         Return ONLY a valid JSON response (no additional text):
        #         {{
        #             "suggestions": [],
        #             "improved_text": "N/A - The provided text does not appear to be a job description or does not contain sufficient job-related information to generate an improved version.",
        #             "seo_keywords": []
        #         }}
        #     """

        improvement_prompt = f"""

                **CRITICAL JSON FORMATTING RULES:**
                - Return ONLY valid JSON - no extra text before or after
                - Ensure all strings are properly quoted
                - Ensure all JSON objects and arrays are properly closed
                - Use proper comma separation between all properties
                - Escape any quotes within string values
               
                **At first check that the job description is related to the particular job role and industry and fulfill the requirements of the job description then do the following**
                
                Improve the following job description for:
                1. Clarity and readability
                2. Inclusive language
                3. Brevity and conciseness
                4. Professional tone
                5. SEO optimization with relevant keywords (Suggest ONLY keywords that are relevant to the job description and are STRICTLY NOT present anywhere in the original text - perform thorough analysis to ensure complete absence)
                
                **CRITICAL IMPROVEMENT RULES:**
                - If it is mentioned that no education requirements are needed or no graduation is required then add this in the **OUR IDEAL CANDIDATE** section: "No formal education requirements are needed for this role"
                - Mention the education requirements in the **OUR IDEAL CANDIDATE** section if it is mentioned in the original job description
                - Add all the skills that are present in the original job description in the **REQUIRED SKILLS** section do not miss any skills that are present in the original job description
                - If it is mentioned that no experience is needed then add this in the **OUR IDEAL CANDIDATE** section: "No prior experience is required for this role, but relevant skills and enthusiasm are essential."
                - Add the required experience in the **OUR IDEAL CANDIDATE** section if it is mentioned in the original job description
                - FLAG LANGUAGE THAT EXCLUDES QUALIFIED CANDIDATES WITHOUT JOB-RELATED JUSTIFICATION
                - DO NOT FLAG LEGITIMATE PROFESSIONAL REQUIREMENTS (e.g., DDS/DMD for dentists, physical demands for construction roles)
                - FOR CLARITY ISSUES: Focus on ambiguous eligibility language that obscures pathways for internationally trained professionals
                

                Original Job Description:
                {text}

                **Analysis Instructions:**
                1. Identify job role and industry context first
                2. Verify if requirements match industry standards (e.g., Colorado dental board for DDS/DMD)
                2a.Suggest improvemnts for the clarity and incusivity issues in the original job description
                3. Suggest improvements for genuinely problematic language
                4. Maintain professional tone while improving inclusivity
                5. DO NOT flag or penalize standard professional language unless clearly discriminatory
                5a. Never flag licensure-mandated terms (e.g., "DDS/DMD", "RN license") as elitism
                6. Suggest ONLY keywords that are relevant to the job description and are STRICTLY NOT present in the Original Job Description - analyze the original text thoroughly to ensure none of the suggested keywords appear anywhere in the original content
                7. Frame the sentences using the seo_keywords that you have found in the previous step and use them in the improved text. CRITICAL: When incorporating these keywords into the text, write them as plain text without any ** or * formatting. For example, if the keyword is "Patient Care", write it as "Patient Care" NOT as "**Patient Care**". IMPORTANT: Only use keywords that are completely absent from the original job description.
                8. DO NOT use any markdown formatting (**, *, etc.) within the content text - ONLY use ** for the section headers as specified in the format below. All keywords and content must be written in plain text without any bold or italic formatting.
                
                **IMPROVED TEXT FORMATTING REQUIREMENTS:**
                The improved job description must follow this exact structure and format (keep the ** around section headers):
                **Rewrite the sentences with (removing the bias and inclusivity issues) some diffrent writting style dont just copy the exact sentences in the KEY RESPONSIBILITIES and OUR IDEAL CANDIDATE sections**
                
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
                    max_output_tokens=3000,
                )
            )
            

            #  # Add detailed logging
            # print(f"Raw Gemini response: {response.text}")

            # Clean the response text to extract JSON
            response_text = response.text.strip()
            
            # print(f"Cleaned response text: {response_text}")
            
            # Remove any markdown formatting if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]

            
            # Debug log before parsing
            print("==== Raw JSON response ====")
            print(response_text)
           
            
            result = json.loads(response_text)
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