import os
import google.generativeai as genai
from typing import List, Dict
import json
from app.models.schemas import BiasIssue, Suggestion, BiasType, SeverityLevel, CategoryType

class LLMService:
    def __init__(self):
        # Configure Google Gemini
        genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def detect_bias(self, text: str) -> Dict:
        """Use Gemini to detect bias in job description"""
        
        bias_detection_prompt = f"""
        Analyze the following job description for various types of bias and discriminatory language.
        Focus on:
        1. Gender bias (masculine/feminine coded words)
        2. Age bias (age-related requirements or preferences)
        3. Racial/cultural bias (cultural assumptions or requirements)
        4. Disability bias (unnecessary physical requirements)
        5. Socioeconomic bias (class-based assumptions)
        6.calculate the bias score using python and add it in the json response that is below=> bias_score
        
        Job Description:
        {text}
        
        Return ONLY a valid JSON response with the following structure (no additional text):
        {{
            "issues": [
                {{
                    "type": "gender|age|racial|cultural|disability|socioeconomic",
                    "text": "the biased phrase",
                    "start_index": 0,
                    "end_index": 10,
                    "severity": "low|medium|high",
                    "explanation": "why this is problematic"
                }}
            ],
            "bias_score": calculate using python and put the float value here only,
            "overall_assessment": "summary of bias findings"
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
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error in bias detection: {str(e)}")
            print(f"Response text: {response.text if 'response' in locals() else 'No response'}")
            return {
                "issues": [],
                "bias_score": 0.0,
                "overall_assessment": "Error occurred during JSON parsing"
            }
        except Exception as e:
            print(f"Error in bias detection: {str(e)}")
            return {
                "issues": [],
                "bias_score": 0.0,
                "overall_assessment": "Error occurred during analysis"
            }
    
    async def improve_language(self, text: str) -> Dict:
        """Use Gemini to suggest language improvements"""
        
        improvement_prompt = f"""
        Improve the following job description for:
        1. Clarity and readability
        2. Inclusive language
        3. Brevity and conciseness
        4. Professional tone
        5. SEO optimization with relevant keywords
        
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
            "clarity_score": 0.0,
            "inclusivity_score": 0.0,
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
            # print(f"Cleaned result: {result}")
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error in language improvement: {str(e)}")
            print(f"Response text: {response.text if 'response' in locals() else 'No response'}")
            return {
                "suggestions": [],
                "improved_text": text,
                "clarity_score": 0.5,
                "inclusivity_score": 0.5,
                "seo_keywords": []
            }
        except Exception as e:
            print(f"Error in language improvement: {str(e)}")
            return {
                "suggestions": [],
                "improved_text": text,
                "clarity_score": 0.5,
                "inclusivity_score": 0.5,
                "seo_keywords": []
            }