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
       
        bias_detection_prompt = f"""
        At first check that the job description is related to the particular job role and industry and fulfill the requirements of the job description then do the following
        Analyze the following text for job description bias. Follow this structured approach:

        **STEP 1: VALIDATION**
        Determine if the text is a job description. If not, return N/A response format.

        **STEP 2: CONTEXT ANALYSIS** 
        Identify the job role, industry, and core functions to distinguish legitimate requirements from bias.

        **STEP 3: BIAS DETECTION**
        Scan for these bias types, considering job relevance:

        1. **Gender Bias**: Gendered language not required for job function
        - BIASED: "salesman", "aggressive personality", "dominant leader" 
        - LEGITIMATE: "confident patient care", "strong clinical skills"

        2. **Age Bias**: Age requirements without job justification
        - BIASED: "young and energetic", "digital native", "recent graduate only"
        - LEGITIMATE: "5+ years experience", "senior-level position"

        3. **Cultural/Racial Bias**: Cultural assumptions not job-relevant
        - BIASED: "native speaker" (when fluency suffices), "cultural fit" without specifics
        - LEGITIMATE: "Hindi fluency for Hindi teacher", "bilingual for international role"

        4. **Disability Bias**: Physical requirements unnecessary for job
        - BIASED: "perfect vision" for desk job, "must stand" for remote work
        - LEGITIMATE: "lifting 50lbs" for warehouse, "clear vision" for driver

        5. **Socioeconomic Bias**: Class-based assumptions not job-relevant
        - BIASED: "prestigious university only", "own car" for remote work
        - LEGITIMATE: "bachelor's degree", "valid license" for driver

        **STEP 4: SCORING**

        **Bias Score (0.0 to 1.0):**
        - Start at 0.0, add points for each biased issue:
        - Low severity: +0.1 | Medium: +0.2 | High: +0.3
        - Cap at 1.0

        **Inclusivity Score (0.0 to 1.0):**
        - Start at 1.0, subtract for exclusionary elements:
        - Explicit discrimination: -0.8
        - Gendered terms (biased): -0.15
        - Unnecessary requirements: -0.2
        - Exclusive language: -0.1

        **Clarity Score (0.0 to 1.0):**
        - Start at 1.0, subtract for unclear elements:
        - Complex sentences: -0.1 each
        - Unclear requirements: -0.15 each
        - Excessive jargon: -0.1 each
        - Poor organization: -0.2

        **DO NOT PENALIZE:**
        - Standard professional terms: "confident", "independent", "strong", "leadership", "competitive", "dedicated"
        - Industry-appropriate requirements: medical roles needing clinical confidence, security needing fitness
        - Legitimate qualifications: teaching credentials, technical certifications, relevant experience

        **CRITICAL RULE:** Only flag requirements that exclude candidates WITHOUT job-related justification.

        Job Description:
        {text}
        

            **For job related text, return a structured JSON response:**
            Return ONLY valid JSON:

            {{
                "role": "job title",
                "industry": "industry name", 
                "issues": [
                    {{
                        "type": "gender|age|racial|cultural|disability|socioeconomic",
                        "text": "biased phrase",
                        "start_index": 0,
                        "end_index": 10,
                        "severity": "low|medium|high",
                        "explanation": "why this is biased and not job-relevant",
                        "job_relevance": "why this requirement is unnecessary for role performance"
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
        
        improvement_prompt = f"""
        **At first check that the job description is related to the particular job role and industry and fulfill the requirements of the job description then do the following**
        
        Improve the following job description for:
        1. Clarity and readability
        2. Inclusive language
        3. Brevity and conciseness
        4. Professional tone
        5. SEO optimization with relevant keywords (Suggest the keywords that are relevant to the job description and not present in the current text)
        
       

        Original Job Description:
        {text}

        **Analysis Instructions:**
        1. Identify job role and industry context first
        2. Distinguish between legitimate professional requirements and actual bias
        3. Only suggest improvements for genuinely problematic language
        4. Maintain professional tone while improving inclusivity
        5. DO NOT flag or penalize standard professional language unless clearly discriminatory
        
        **IMPROVED TEXT FORMATTING REQUIREMENTS:**
        The improved job description must follow this exact structure and format:
        
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
        
        **REQUIRED QUALIFICATIONS:**
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
        
        Return ONLY a valid JSON response (no additional text):
        {{
            "suggestions": [
                {{
                    "original": "original phrase",
                    "improved": "improved phrase",
                    "rationale": "why this is better",
                    "category": "clarity|inclusivity"
                }}
            ],
            "seo_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
            "improved_text": "[Complete rewritten job description using the SEO keywords identified above also following the EXACT structure outlined above. Maintain all original context while improving clarity, inclusivity, and SEO optimization. Use the specific headers and bullet point format as specified.]",
            
            
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