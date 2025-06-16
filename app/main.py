from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import AnalyzeRequest, BiasAnalysisResult, TextExtractionResponse
from app.services.text_extractor import TextExtractor
from app.services.bias_detector import BiasDetector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Job Description Bias Detection API",
    description="AI-powered bias detection and language improvement for job descriptions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5268"],  # React and .NET URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
text_extractor = TextExtractor()
bias_detector = BiasDetector()

@app.get("/")
async def root():
    return {"message": "Job Description Bias Detection API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "python-llm-bias-detector"}

# @app.post("/extract-text", response_model=TextExtractionResponse)
# async def extract_text_from_file(file: UploadFile = File(...)):
#     """Extract text from uploaded file (PDF, DOCX, images, etc.)"""
    
#     if not file.filename:
#         raise HTTPException(status_code=400, detail="No file provided")
    
#     # Check file size (10MB limit)
#     file_size = 0
#     content = await file.read()
#     file_size = len(content)
#     print(f"Uploaded file size: {file_size} bytes") # Debug log checkpoint 1 done
    
#     if file_size > 10 * 1024 * 1024:  # 10MB
#         raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB")
    
#     # Reset file pointer
#     await file.seek(0)
    
#     result = await text_extractor.extract_from_file(file)
    
#     if not result.success:
#         raise HTTPException(status_code=400, detail=result.error_message)
    
#     return result

@app.post("/extract", response_model=TextExtractionResponse)
async def extract_text_from_file(file: UploadFile = File(...)):
    """Extract text from uploaded file (PDF, DOCX, images, etc.)"""
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    try:
        # Read file content once
        content = await file.read()
        file_size = len(content)
        print(f"Uploaded file size: {file_size} bytes")
        
        if file_size > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB")
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="Empty file provided")
        
        # Pass content directly to extractor
        result = await text_extractor.extract_from_content(content, file.filename)
        
        if not result.success:
            print(f"Extraction failed: {result.error_message}")
            raise HTTPException(status_code=400, detail=result.error_message)
        
        print(f"Extraction result: {result}")  # Debug log here also good
        return result
        
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/analyze", response_model=BiasAnalysisResult)
async def analyze_bias(request: AnalyzeRequest):
    """Analyze job description text for bias and suggest improvements"""
    
    if not request.text or len(request.text.strip()) < 50:
        raise HTTPException(
            status_code=400, 
            detail="Job description text must be at least 50 characters long"
        )
    
    try:
        result = await bias_detector.analyze_comprehensive(request.text)
        print(f"Analysis result going from /analyze: {result}")  # Debug log
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze-file")
async def analyze_uploaded_file(file: UploadFile = File(...)):
    """Extract text from file and analyze for bias - convenience endpoint"""
    
    # First extract text
    extraction_result = await extract_text_from_file(file)
    
    if not extraction_result.success:
        raise HTTPException(status_code=400, detail=extraction_result.error_message)
    
    # Then analyze the extracted text
    analysis_request = AnalyzeRequest(text=extraction_result.extracted_text)
    analysis_result = await analyze_bias(analysis_request)

    print(f"Analysis result from /analyze-file: {analysis_result}")  # Debug log
    
    return {
        "extracted_text": extraction_result.extracted_text,
        "analysis": analysis_result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
