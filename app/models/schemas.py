from pydantic import BaseModel
from typing import List, Optional,Union
from enum import Enum

class BiasType(str, Enum):
    GENDER = "gender"
    AGE = "age"
    RACIAL = "racial"
    CULTURAL = "cultural"
    DISABILITY = "disability"
    RELIGION = "religion",
    AGE_DISCLOSURE = "age_disclosure"  # Added based on LLM response
    SOCIOECONOMIC = "socioeconomic"
    PHYSICAL = "physical"
    LEGAL = "legal"  # Added based on LLM response
    CLARITY = "clarity"        # Added - missing from original
    INCLUSIVITY = "inclusivity"  # Added - missing from original
    LGBTQ = "lgbtq"
    FORMER_FELONS = "former_felons"
    ELITISM = "elitism"
    MENTAL_HEALTH = "mental_health"


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
    AGE = "age"  # Added based on LLM response
    DISABILITY = "disability"  # Added based on LLM response
    ELITISM = "elitism"  # Added based on LLM response
    MENTAL_HEALTH = "mental_health"  # Added based on LLM response
    

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
    role:Optional[str] = None
    industry: Optional[str] = None
    # bias_score: float 
    # inclusivity_score: float
    # clarity_score: float
    bias_score: Union[str, float]
    inclusivity_score: Union[str, float]
    clarity_score: Union[str, float]
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


class AnalyzeFileResponse(BaseModel):
    extracted_text: str
    analysis: BiasAnalysisResult