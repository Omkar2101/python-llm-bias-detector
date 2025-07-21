# Python LLM Bias Detector Documentation

---

## 📋 Index

1. [Project Overview](#project-overview)  
2. [Directory Structure](#directory-structure)  
3. [Tech Stack & Environment](#tech-stack--environment)  
4. [File-by-File Breakdown](#file-by-file-breakdown)  
   - [app/models/schemas.py](#appmodelsschemaspy)  
   - [app/services/llm_service.py](#appservicesllm_servicepy)  
   - [app/services/bias_detector.py](#appservicesbias_detectorpy)  
   - [app/services/text_extractor.py](#appservicestext_extractorpy)  
   - [app/utils/helpers.py](#apputilshelperspy)  
   - [app/main.py](#appmainpy)  
   - [tests/test_text_extractor.py](#teststest_text_extractorpy)  
   - [tests/test_llm_service.py](#teststest_llm_servicepy)  
   - [tests/test_bias_detector.py](#teststest_bias_detectorpy)  
   - [tests/test_main.py](#teststest_mainpy)  
   - [tests/evaluation](#testsevaluation)  
   - [tests/test_data/test_cases.py](#teststest_datatest_casespy)  
   - [Configuration & Metadata](#configuration--metadata)  

---

## 🔍 Project Overview

**Name:** Job Description Bias Detection API  
**Purpose:**  
An AI-powered service that analyzes job description text (or uploaded files) to:

- Detect various types of bias (gender, age, racial, etc.)  
- Provide severity-rated issues with explanations  
- Offer language improvement suggestions (clarity, inclusivity, professionalism, SEO)  
- Compute readability and inclusivity/clarity scores  
- Support multiple input formats (plain text, PDF, DOCX, images)  

The core logic combines a Google Gemini–powered LLM (`LLMService`) with a rule-based fallback (`BiasDetector`), exposed via a FastAPI application (`app/main.py`).

---

## 📂 Directory Structure

```
.
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── app
│   ├── main.py
│   ├── models
│   │   └── schemas.py
│   ├── services
│   │   ├── llm_service.py
│   │   ├── bias_detector.py
│   │   └── text_extractor.py
│   └── utils
│       └── helpers.py
└── tests
    ├── __init__.py
    ├── .coverage
    ├── test_text_extractor.py
    ├── test_llm_service.py
    ├── test_bias_detector.py
    ├── test_main.py
    ├── test_data
    │   └── test_cases.py
    └── evaluation
        ├── test_model_evaluation.py
        └── results
            ├── all_cases_results.json
            ├── hard_cases_results.json
            └── hard_cases_results1.json
```

- **app/**: Core application  
  - **models/schemas.py**: Pydantic models and enums.  
  - **services/**: Business logic  
    - **llm_service.py**: Wraps LLM interactions.  
    - **bias_detector.py**: Combines LLM + rule-based bias detection.  
    - **text_extractor.py**: Extracts text from various file types.  
  - **utils/helpers.py**: File-format extraction utilities.  
  - **main.py**: FastAPI application and endpoints.  

- **tests/**: Pytest suite  
  - Unit tests for each service and endpoint.  
  - **evaluation/**: End-to-end evaluation harness and results.  
  - **test_data/**: Definitions of sample test cases.

- **Dockerfile**, **pyproject.toml**, **requirements.txt**: Containerization & dependencies.

---

## 🛠️ Tech Stack & Environment

- **Language**: Python 3.10  
- **Web Framework**: FastAPI  
- **LLM**: Google Gemini (`google.generativeai`)  
- **Validation**: Pydantic  
- **Readability**: textstat (Flesch–Kincaid score)  
- **File Parsing**:  
  - PDFs via PyPDF2  
  - DOCX via python-docx  
  - Images via Pillow + pytesseract  
- **Testing**: Pytest, FastAPI TestClient  
- **Containerization**: Docker (Python 3.10‐slim base)  
- **Environment Variables**:  
  - `GOOGLE_GEMINI_API_KEY` (required)

---

## 📁 File-by-File Breakdown

### app/models/schemas.py

Defines all data models and enums for requests/responses:

- **Enums**  
  - `BiasType`: gender, age, racial, cultural, disability, religious, socioeconomic, physical, legal  
  - `SeverityLevel`: low, medium, high  
  - `CategoryType`: bias, clarity, seo, inclusivity, professionalism, legal  

- **Models**  
  - `BiasIssue`: one detected bias issue  
  - `Suggestion`: one language improvement suggestion  
  - `BiasAnalysisResult`: full bias analysis + scores + suggestions  
  - `AnalyzeRequest`: `{ text: str }` for JSON analysis  
  - `TextExtractionResponse`: result of file‐based text extraction  
  - `AnalyzeFileResponse`: bundles extracted text + bias analysis  

These models ensure type safety and automatic docs generation (OpenAPI).

---

### app/services/llm_service.py

**`LLMService`** wraps the Google Gemini API:

- **Initialization**  
  - Loads `.env`, reads `GOOGLE_GEMINI_API_KEY`, configures `genai`.  
  - Instantiates `GenerativeModel('gemini-2.0-flash')`.

- **Methods**  
  - `async detect_bias(text: str) -> Dict`  
    - Builds a detailed prompt covering bias categories, job context, legitimate vs. biased requirements, and scoring methodology.  
    - Calls `model.generate_content(prompt)`; handles API errors (rate limiting, auth, timeouts) by raising appropriate `HTTPException`.  
    - Cleans markdown or code fences, parses JSON.

  - `async improve_language(text: str) -> Dict`  
    - Builds a prompt to suggest language improvements (clarity, inclusivity, SEO, professionalism).  
    - Returns suggestions, improved text, clarity & inclusivity scores, and SEO keywords.

- **Internal Helpers**  
  - Cleans markdown or extraneous whitespace before JSON parsing.  
  - Maps HTTP status codes to user-friendly error types.

---

### app/services/bias_detector.py

**`BiasDetector`** orchestrates comprehensive bias analysis:

1. **Initialization**  
   - Instantiates `LLMService`.  
   - Defines **rule-based** fallback patterns:  
     - `gender_coded_words` (masculine & feminine lists)  
     - `problematic_phrases` (keywords for gender, race, age, cultural, religious, educational biases)

2. **`async analyze_comprehensive(text: str) -> BiasAnalysisResult`**  
   - **LLM Bias Detection**: calls `detect_bias(text)`; falls back to empty issues + default bias_score on error.  
   - **LLM Language Improvement**: calls `improve_language(text)`; falls back to zeros/no suggestions.  
   - **Parse & Merge**  
     - `_parse_llm_issues`: converts raw LLM issue dicts into `BiasIssue` objects, ignoring invalid entries.  
     - `_detect_rule_based_bias`: scans text for rule-based keywords, generating additional `BiasIssue` objects.  
     - Deduplicates combined issues.  
   - **Readability**: Computes Flesch–Kincaid grade level via `textstat`.  
   - **Result Assembly**: Packages everything into `BiasAnalysisResult`.

3. **Helper Methods**  
   - `_parse_category`, `_map_category_to_bias_type`, `_parse_suggestions`.

---

### app/services/text_extractor.py

**`TextExtractor`** handles file‐based text extraction:

- **`async extract_from_content(content: bytes, filename: str) -> TextExtractionResponse`**  
  1. Determine file type via extension.  
  2. Dispatch to:  
     - `_extract_pdf` ➔ uses `helpers.read_pdf`  
     - `_extract_docx` ➔ uses `helpers.read_docx`  
     - `_extract_image` ➔ uses `helpers.extract_text_from_image`  
     - Fallback: treat as plain text.  
  3. Returns success flag, extracted text, file type, or error message.

Leverages **helpers** in `app/utils/helpers.py` for low-level extraction logic.

---

### app/utils/helpers.py

Utility functions for file parsing:

- **`read_pdf(content: bytes) -> str`**: Extract text via PyPDF2.  
- **`read_docx(content: bytes) -> str`**: Extract paragraphs via python-docx.  
- **`extract_text_from_image(image_bytes: bytes) -> str`**: OCR via Pillow + pytesseract.  
- **`get_file_extension(filename: str) -> str`**: Normalize to lowercase extension.

These helpers keep `TextExtractor` concise and focused on orchestration.

---

### app/main.py

FastAPI application setup and routing:

1. **App Configuration**  
   - Metadata (title, description, version)  
   - CORS middleware allowing frontends on `localhost:3000` & `5268`  
   - Global exception handlers for `HTTPException` and generic `Exception`  

2. **Service Initialization**  
   ```python
   text_extractor = TextExtractor()
   bias_detector   = BiasDetector()
   ```

3. **Endpoints**  
   - `GET /` → Welcome message  
   - `GET /health` → Health check  
   - `POST /extract`  
     - Accepts file upload, returns `TextExtractionResponse`.  
     - Validates file presence, size (≤ 10 MB), non‐empty.  
   - `POST /analyze`  
     - Accepts JSON `{ text }`, returns `BiasAnalysisResult`.  
     - Validates minimum length (≥ 50 chars).  
   - `POST /analyze-file`  
     - Combines `/extract` + `/analyze` in one call, returning `AnalyzeFileResponse`.

#### API Endpoint Example

```api
{
    "title": "Analyze Job Description Text",
    "description": "Detect bias and suggest language improvements in plain text",
    "method": "POST",
    "baseUrl": "http://localhost:8000",
    "endpoint": "/analyze",
    "headers": [
        { "key": "Content-Type", "value": "application/json", "required": true }
    ],
    "bodyType": "json",
    "requestBody": "{\n  \"text\": \"Your job description here...\"\n}",
    "responses": {
        "200": {
            "description": "Analysis successful",
            "body": "{\n  \"role\": \"Software Engineer\",\n  \"industry\": \"Technology\",\n  \"bias_score\": 0.2,\n  \"inclusivity_score\": 0.9,\n  \"clarity_score\": 0.8,\n  \"issues\": [ ... ],\n  \"suggestions\": [ ... ],\n  \"seo_keywords\": [ ... ],\n  \"improved_text\": \"...\",\n  \"overall_assessment\": \"...\"\n}"
        },
        "400": {
            "description": "Validation error",
            "body": "{ \"error\": true, \"message\": \"Job description text must be at least 50 characters long\" }"
        }
    }
}
```

---

## 🔄 Data & Control Flow Diagram

```mermaid
graph TD
    Client[Client] -->|POST /analyze-file with UploadFile| API[FastAPI App]
    
    subgraph "File Processing"
        API -->|extract_from_content| TE[TextExtractor]
        TE -->|Read file content| FileReaders{File Type?}
        FileReaders -->|PDF| PDF[PdfReader - pypdf]
        FileReaders -->|DOCX| DOCX[Document - docx]
        FileReaders -->|TXT| TXT[decode content]
        FileReaders -->|Image| OCR[EasyOCR Reader]
        PDF --> TE
        DOCX --> TE
        TXT --> TE
        OCR --> TE
        TE -->|TextExtractionResponse| API
    end
    
    subgraph "Bias Analysis"
        API -->|AnalyzeRequest| BD[BiasDetector]
        BD -->|analyze_comprehensive| LLM1[detect_bias]
        BD -->|analyze_comprehensive| LLM2[improve_language]
        
        LLM1 -->|LLMService| GeminiAPI1[Google Gemini API<br/>bias_detection_prompt]
        LLM2 -->|LLMService| GeminiAPI2[Google Gemini API<br/>improvement_prompt]
        
        GeminiAPI1 -->|JSON Response| Parser1[_parse_llm_issues]
        GeminiAPI2 -->|JSON Response| Parser2[_parse_llm_suggestions]
        
        Parser1 --> BD
        Parser2 --> BD
        
        BD -->|BiasAnalysisResult| API
    end
    
    subgraph "Response Processing"
        API -->|Combine results| Response[AnalyzeFileResponse]
        Response --> Client
    end
    
    subgraph "Data Models"
        Schemas[schemas.py<br/>- BiasAnalysisResult<br/>- BiasIssue<br/>- Suggestion<br/>- TextExtractionResponse<br/>- AnalyzeFileResponse]
    end
    
    subgraph "Error Handling"
        API -.->|HTTPException| ErrorHandler[Global Exception Handlers]
        ErrorHandler -.->|JSONResponse| Client
    end
    
    %% Styling
    classDef apiClass fill:#e1f5fe
    classDef serviceClass fill:#f3e5f5
    classDef externalClass fill:#fff3e0
    classDef dataClass fill:#e8f5e8
    
    class API apiClass
    class TE,BD serviceClass
    class GeminiAPI1,GeminiAPI2,PDF,DOCX,OCR externalClass
    class Schemas,Response dataClass

---
##Flow Details
-**File-based input (POST /analyze-file)**:

-**Client uploads a file.**
-The API calls TextExtractor to extract text using helpers for PDF, DOCX, or image files.
-Once the text is extracted, the API proceeds to BiasDetector for comprehensive analysis, including LLM-based detection, -rule-based checks, and readability scoring.
-Direct text input (POST /analyze):

**Client sends raw job description text**.
-The API skips the extraction step and directly invokes the BiasDetector.
-The rest of the analysis pipeline (LLM, rule-based, readability) remains the same.

## ✅ Testing Summary

- **`test_text_extractor.py`**:  
  - PDF, DOCX, image extraction success & failure.  
  - File size & empty file validation.

- **`test_llm_service.py`**:  
  - Initialization with/without API key.  
  - `detect_bias` & `improve_language` success, JSON cleaning, error paths (rate limit, timeout, auth, service unavailable).

- **`test_bias_detector.py`**:  
  - Rule-based detection (`_detect_rule_based_bias`).  
  - Parsing LLM output (`_parse_llm_issues`, `_parse_suggestions`, `_parse_category`).  
  - `analyze_comprehensive` full pipeline, handling invalid string scores.

- **`test_main.py`**:  
  - FastAPI endpoints: root, health, `/extract`, `/analyze`, `/analyze-file`.  
  - Response shape, status codes, error messages.

- **Evaluation Harness (`test_model_evaluation.py`)**:  
  - Loads predefined hard/easy cases from `tests/test_data`.  
  - Runs analysis, compares to expected metrics, outputs JSON in `tests/evaluation/results/`.  
  - Metrics: bias/inclusivity/clarity score differences, issues count accuracy, pass rates.

---

## ⚙️ Configuration & Metadata

- **Dockerfile**  
  - Base: `python:3.10-slim`  
  - Installs system deps (`build-essential`, `libpq-dev`)  
  - Copies `requirements.txt`, installs Python deps  
  - Creates non-root `appuser`  
  - Exposes port `8000`  
  - Entrypoint: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

- **requirements.txt / pyproject.toml**  
  - Key libs: `fastapi`, `uvicorn`, `pydantic`, `google-generativeai`, `textstat`, `PyPDF2`, `python-docx`, `pillow`, `pytesseract`, `python-dotenv`, `pytest`, etc.

- **Environment Variables**  
  - `GOOGLE_GEMINI_API_KEY` (must be set in `.env` or environment)

---

