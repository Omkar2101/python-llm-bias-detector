from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class BiasType(str, Enum):
    GENDER = "gender"
    AGE = "age"
    RACIAL = "racial"
    CULTURAL = "cultural"
    DISABILITY = "disability"
    RELIGIOUS = "religious"
    SOCIOECONOMIC = "socioeconomic"
    PHYSICAL = "physical"
    LEGAL = "legal"  # Added based on LLM response

class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class CategoryType(str, Enum):
    BIAS = "bias"
    CLARITY = "clarity"
    SEO = "seo"
    INCLUSIVITY = "inclusivity"
    PROFESSIONALISM = "professionalism"  # Added - this was missing!
    LEGAL = "legal"  # Added based on LLM response

class BiasIssue(BaseModel):
    type: BiasType
    text: str
    start_index: int
    end_index: int
    severity: SeverityLevel
    explanation: str

class Suggestion(BaseModel):
    original: str
    improved: str
    rationale: str
    category: CategoryType

class BiasAnalysisResult(BaseModel):
    bias_score: float
    inclusivity_score: float
    clarity_score: float
    issues: List[BiasIssue]
    suggestions: List[Suggestion]
    seo_keywords: List[str]
    improved_text: Optional[str] = None
    overall_assessment: Optional[str] = None

class AnalyzeRequest(BaseModel):
    text: str

class TextExtractionResponse(BaseModel):
    success: bool
    extracted_text: Optional[str] = None
    file_type: Optional[str] = None
    error_message: Optional[str] = None