import os
import google.generativeai as genai
from typing import List, Dict
import json
from app.models.schemas import BiasIssue, Suggestion, BiasType, SeverityLevel, CategoryType
from fastapi import HTTPException
import time

class LLMService:
    def __init__(self):
        # Configure Google Gemini
        genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    async def detect_bias(self, text: str) -> Dict:
        """Use Gemini to detect bias in job description"""
       

        bias_detection_prompt = f"""
        Analyze the following job description for various types of bias and discriminatory language.
        IMPORTANT: Consider job-relevant requirements vs. discriminatory bias. Some requirements may be legitimate based on job function.

        **Job Context Analysis:**
        First, identify the job role, industry, and core functions to determine what requirements are legitimate vs. potentially biased.

        **Bias Categories to Analyze:**
        1. **Gender bias**: Masculine/feminine coded words not related to job function
        2. **Age bias**: Age-related requirements without job justification
        3. **Racial/cultural bias**: Cultural assumptions not required for job performance
        4. **Disability bias**: Physical requirements unnecessary for job function
        5. **Socioeconomic bias**: Class-based assumptions not job-relevant
        6. **Language bias**: Language requirements not essential for job performance

        **Legitimate vs. Biased Requirements:**

        **LEGITIMATE Examples (NOT bias):**
        - Hindi teacher requiring Hindi fluency
        - International sales role requiring specific language skills
        - Physical therapist requiring physical capabilities
        - Security guard requiring physical fitness standards
        - Customer service requiring communication skills
        - Teaching role requiring teaching qualification/experience
        - Technical role requiring specific technical skills
        - Driver requiring valid driving license
        - Accountant requiring accounting certification

        **POTENTIALLY BIASED Examples:**
        - Administrative role requiring "native English speaker" (vs. "fluent English")
        - General office job requiring "young and energetic"
        - Non-customer facing role requiring "attractive appearance"
        - Remote work requiring "own transportation"
        - Entry-level role requiring "prestigious university degree"
        - General role requiring "cultural fit" without specifics
        - Non-physical job requiring unnecessary physical requirements

        **Context-Specific Evaluation Rules:**
        - **Language Requirements**: Only flag if language skill isn't directly related to job function
        - **Physical Requirements**: Only flag if physical capability isn't essential for job tasks
        - **Educational Requirements**: Flag if overly specific or unnecessary for job level
        - **Experience Requirements**: Flag if unrealistic for position level
        - **Cultural Requirements**: Flag unless specific cultural knowledge is job-relevant

        **Scoring Methodology:**
        - Start with 0.0 (no bias)
        - Add points for each GENUINELY biased issue (not legitimate job requirements):
        * Low severity: +0.1 per issue
        * Medium severity: +0.2 per issue  
        * High severity: +0.3 per issue
        - Cap maximum score at 1.0
        - Consider job context when determining if requirement is discriminatory

        **Severity Guidelines:**
        - **Low**: Subtle coded language that could exclude without job relevance
        - **Medium**: Clear exclusionary language not justified by job function
        - **High**: Explicit discrimination with no job-related justification

        **Job-Specific Considerations:**
        - **Teaching/Training roles**: Language, communication, and educational requirements are typically legitimate
        - **Customer-facing roles**: Communication and presentation requirements may be legitimate
        - **Physical roles**: Physical capability requirements are typically legitimate
        - **Technical roles**: Technical skill requirements are typically legitimate
        - **Leadership roles**: Leadership experience requirements are typically legitimate
        - **Safety-critical roles**: Health and safety requirements are typically legitimate

        Job Description:
        {text}

        **Analysis Instructions:**
        1. First identify the job role and its core requirements
        2. Evaluate each potential bias against job relevance
        3. Only flag requirements that are NOT justified by job function
        4. Provide clear explanation for why flagged items are biased vs. job-relevant

        Return ONLY a valid JSON response with the following structure (no additional text):
        {{
            "job_context": {{
                "role": "identified job title/role",
                "industry": "identified industry/sector",
                "core_functions": ["list of main job functions"]
            }},
            "issues": [
                {{
                    "type": "gender|age|racial|cultural|disability|socioeconomic|language",
                    "text": "the biased phrase",
                    "start_index": 0,
                    "end_index": 10,
                    "severity": "low|medium|high",
                    "explanation": "why this is problematic and not job-relevant",
                    "job_relevance": "explanation of why this requirement is/isn't necessary for the role"
                }}
            ],
            "bias_score": bias_score,
            "overall_assessment": "summary of bias findings considering job context",
            "legitimate_requirements": ["list of requirements that are job-relevant and not biased"]
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
        Improve the following job description for:
        1. Clarity and readability
        2. Inclusive language
        3. Brevity and conciseness
        4. Professional tone
        5. SEO optimization with relevant keywords
        
        **IMPORTANT: Consider job-relevant requirements vs. discriminatory bias. Some requirements may be legitimate based on job function.**
        
        6. Calculate clarity_score: A single float value between 0 and 1, where 0 means very unclear/confusing and 1 means crystal clear and easy to understand. Evaluate based on sentence structure, jargon usage, and requirement clarity. Normalize this based on the number and severity of clarity issues found. Keep this value realistic. Put this value in below response in front of clarity_score.
        
        7. Calculate inclusivity_score: A single float value between 0 and 1, where 0 means highly exclusive/biased and 1 means fully inclusive. Evaluate based on gender-neutral language, unnecessary requirements, and accessibility considerations. Start with 1.0 and subtract points for exclusionary elements. Consider job context - only penalize requirements that aren't justified by job function. Keep this value realistic and consistent with the issues present. Put this value in below response in front of inclusivity_score.
        
        **Scoring Guidelines:**
        
        **Clarity Score Deductions (start from 1.0):**
        - Complex sentences (-0.1 each)
        - Unclear requirements (-0.15 each)
        - Excessive jargon (-0.1 each)
        - Poor organization (-0.2)
        - Confusing structure (-0.15 each)
        
        **Inclusivity Score Deductions (start from 1.0):**
        - **AUTOMATIC LOW SCORES (0.1-0.2) for explicit discrimination:**
          * "Male preferred" or "females need not apply" (-0.8)
          * Racial requirements like "Caucasian background" (-0.8)
          * Religious discrimination "no religious accommodations" (-0.8)
          * Age discrimination "young professionals only" (-0.8)
        - Gender-biased terms (-0.15 each)
        - Unnecessary degree requirements (-0.2 each)
        - Exclusive language (-0.1 each)
        - Cultural assumptions (-0.1 each)
        - Appearance requirements (-0.2 each)
        - Inappropriate work requirements (-0.3 each)
        
        **Examples of Discriminatory Language:**
        - **Explicit discrimination**: "male preferred", "Caucasian background", "no religious accommodations"
        - **Gender bias**: "masculine presence", "aggressive", "dominant"
        - **Age bias**: "young and energetic", "recent graduate", "digital native"
        - **Cultural bias**: "native speaker", "cultural fit", "American values"
        - **Appearance bias**: "traditional appearance", "classic look", "attractive"
        - **Educational elitism**: "Ivy League only", "prestigious university"
        
        **Legitimate vs. Discriminatory Requirements:**
        - **Legitimate**: Hindi teacher requiring Hindi fluency, security guard requiring physical fitness
        - **Discriminatory**: Administrative role requiring "native English speaker", general office job requiring "young and energetic"
        
        Original Job Description:
        {text}
        
        Return ONLY a valid JSON response (no additional text):
        {{
            "suggestions": [
                {{
                    "original": "original phrase",
                    "improved": "improved phrase",
                    "rationale": "why this is better",
                    "category": "bias|clarity|seo|inclusivity"
                }}
            ],
            "improved_text": "complete rewritten job description",
            "clarity_score": clarity_score,
            "inclusivity_score": inclusivity_score,
            "seo_keywords": ["keyword1", "keyword2"]
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
            print(f"Cleaned result: {result}")
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