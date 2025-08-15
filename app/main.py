# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from app.models.schemas import AnalyzeRequest, BiasAnalysisResult, TextExtractionResponse,AnalyzeFileResponse
# from app.services.text_extractor import TextExtractor
# from app.services.bias_detector import BiasDetector
# import os
# from dotenv import load_dotenv
# from fastapi.responses import JSONResponse

# # Load environment variables
# load_dotenv()

# app = FastAPI(
#     title="Job Description Bias Detection API",
#     description="AI-powered bias detection and language improvement for job descriptions",
#     version="1.0.0"
# )

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://localhost:5268"],  # React and .NET URLs
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Initialize services
# text_extractor = TextExtractor()
# bias_detector = BiasDetector()


# # Global exception handler for HTTPException
# @app.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={
#             "error": True,
#             "message": exc.detail,
#             "status_code": exc.status_code,
#             "type": get_error_type(exc.status_code)
#         }
#     )

# # Global exception handler for general exceptions
# @app.exception_handler(Exception)
# async def general_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=500,
#         content={
#             "error": True,
#             "message": "An unexpected error occurred. Please try again later.",
#             "status_code": 500,
#             "type": "internal_server_error"
#         }
#     )

# def get_error_type(status_code: int) -> str:
#     """Get user-friendly error type based on status code"""
#     error_types = {
#         400: "validation_error",
#         401: "authentication_error",
#         403: "permission_error",
#         404: "not_found_error",
#         413: "file_too_large",
#         429: "rate_limit_exceeded",
#         500: "internal_server_error",
#         503: "service_unavailable",
#         504: "timeout_error"
#     }
#     return error_types.get(status_code, "unknown_error")
# @app.get("/")
# async def root():
#     return {"message": "Job Description Bias Detection API", "status": "running"}

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy", "service": "python-llm-bias-detector"}



# @app.post("/extract", response_model=TextExtractionResponse)
# async def extract_text_from_file(file: UploadFile = File(...)):
#     """Extract text from uploaded file (PDF, DOCX, images, etc.)"""
    
#     if not file.filename:
#         raise HTTPException(status_code=400, detail="No file provided")
    
#     try:
#         # Read file content once
#         content = await file.read()
#         file_size = len(content)
#         print(f"Uploaded file size: {file_size} bytes")
        
#         if file_size > 10 * 1024 * 1024:  # 10MB
#             raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB")
        
#         if file_size == 0:
#             raise HTTPException(status_code=400, detail="Empty file provided")
        
#         # Pass content directly to extractor
#         result = await text_extractor.extract_from_content(content, file.filename)
        
#         if not result.success:
#             print(f"Extraction failed: {result.error_message}")
#             raise HTTPException(status_code=400, detail=result.error_message)
        
#         print(f"Extraction result: {result}")  # Debug log here also good
#         return result
        
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         print(f"Unexpected error during text extraction: {str(e)}")
#         raise HTTPException(
#             status_code=500, 
#             detail="Text extraction failed due to an internal error"
#         )

# @app.post("/analyze", response_model=BiasAnalysisResult)
# async def analyze_bias(request: AnalyzeRequest):
#     """Analyze job description text for bias and suggest improvements"""
    
#     if not request.text or len(request.text.strip()) < 50:
#         raise HTTPException(
#             status_code=400, 
#             detail="Job description text must be at least 50 characters long"
#         )
    
#     try:
#         result = await bias_detector.analyze_comprehensive(request.text)
#         print(f"Analysis result going from /analyze: {result}")  # Debug log
       
       

        

#         return result
#     except Exception as e:
#         print(f"Unexpected error during bias analysis: {str(e)}")
#         raise HTTPException(
#             status_code=500, 
#             detail="Bias analysis failed due to an internal error"
#         )

# @app.post("/analyze-file")
# async def analyze_uploaded_file(file: UploadFile = File(...)):
#     """Extract text from file and analyze for bias - convenience endpoint"""
#     if not file.filename:
#         raise HTTPException(status_code=400, detail="No file provided")
#     try:
#         # First extract text
#         extraction_result = await extract_text_from_file(file)
        
#         if not extraction_result.success:
#             raise HTTPException(status_code=400, detail=extraction_result.error_message)
        
#         # Then analyze the extracted text
#         analysis_request = AnalyzeRequest(text=extraction_result.extracted_text)
#         analysis_result = await analyze_bias(analysis_request)

#         print(f"Analysis result from /analyze-file: {analysis_result}")  # Debug log
        
       
#         return AnalyzeFileResponse(
#         extracted_text=extraction_result.extracted_text,
#         analysis=analysis_result
#     )

#     except HTTPException:
#         raise
#     except Exception as e:
#         print(f"Unexpected error during file analysis: {str(e)}")
#         raise HTTPException(
#             status_code=500, 
#             detail="File analysis failed due to an internal error"
#         )

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import AnalyzeRequest, BiasAnalysisResult, TextExtractionResponse,AnalyzeFileResponse
from app.services.text_extractor import TextExtractor
from app.services.bias_detector import BiasDetector
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Job Description Bias Detection API",
    description="AI-powered bias detection and language improvement for job descriptions",
    version="1.0.0"
)

# Add CORS middleware - Allow All Origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Set to False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
text_extractor = TextExtractor()
bias_detector = BiasDetector()


# Global exception handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "type": get_error_type(exc.status_code)
        }
    )

# Global exception handler for general exceptions
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "An unexpected error occurred. Please try again later.",
            "status_code": 500,
            "type": "internal_server_error"
        }
    )

def get_error_type(status_code: int) -> str:
    """Get user-friendly error type based on status code"""
    error_types = {
        400: "validation_error",
        401: "authentication_error",
        403: "permission_error",
        404: "not_found_error",
        413: "file_too_large",
        429: "rate_limit_exceeded",
        500: "internal_server_error",
        503: "service_unavailable",
        504: "timeout_error"
    }
    return error_types.get(status_code, "unknown_error")

@app.get("/")
async def root():
    return {"message": "Job Description Bias Detection API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "python-llm-bias-detector"}

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
        print(f"Unexpected error during text extraction: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Text extraction failed due to an internal error"
        )

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
        error_msg = str(e)
        if "Language improvement service failed" in error_msg:
            raise HTTPException(
                status_code=503,  # Service Unavailable
                detail="Language improvement service is temporarily unavailable. Please try again later."
            )
        else:
            print(f"Unexpected error during bias analysis: {error_msg}")
            raise HTTPException(
                status_code=500, 
                detail="Bias analysis failed due to an internal error"
            )

@app.post("/analyze-file")
async def analyze_uploaded_file(file: UploadFile = File(...)):
    """Extract text from file and analyze for bias - convenience endpoint"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    try:
        # First extract text
        extraction_result = await extract_text_from_file(file)
        
        if not extraction_result.success:
            raise HTTPException(status_code=400, detail=extraction_result.error_message)
        
        # Then analyze the extracted text
        analysis_request = AnalyzeRequest(text=extraction_result.extracted_text)
        analysis_result = await analyze_bias(analysis_request)

        print(f"Analysis result from /analyze-file: {analysis_result}")  # Debug log
        
       
        return AnalyzeFileResponse(
        extracted_text=extraction_result.extracted_text,
        analysis=analysis_result
    )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error during file analysis: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="File analysis failed due to an internal error"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
