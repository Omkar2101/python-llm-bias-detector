import os
import io
from typing import Optional
import easyocr
# import PyPDF2
from pypdf import PdfReader
from docx import Document
from PIL import Image
import numpy as np
from fastapi import UploadFile
from app.models.schemas import TextExtractionResponse

class TextExtractor:

    def __init__(self):
        # Initialize EasyOCR reader (this will download models on first use)
        self.reader = easyocr.Reader(['en'])  # Add more languages as needed: ['en', 'hi', 'mr']
    
    # @staticmethod
    # async def extract_from_file(file: UploadFile) -> TextExtractionResponse:
    #     """Extract text from uploaded file based on file type"""
    #     try:
    #         file_extension = os.path.splitext(file.filename)[1].lower()
    #         content = await file.read()
    #         printf(content[:100])  # Debug log to check content type
            
    #         if file_extension == '.txt':
    #             text = content.decode('utf-8')
    #         elif file_extension == '.pdf':
    #             text = TextExtractor._extract_from_pdf(content)
    #         elif file_extension in ['.doc', '.docx']:
    #             text = TextExtractor._extract_from_docx(content)
    #         elif file_extension in ['.png', '.jpg', '.jpeg']:
    #             text = TextExtractor._extract_from_image(content)
    #         else:
    #             return TextExtractionResponse(
    #                 extracted_text="",
    #                 success=False,
    #                 error_message=f"Unsupported file type: {file_extension}"
    #             )
            
    #         return TextExtractionResponse(
    #             extracted_text=text,
    #             success=True
    #         )
            
    #     except Exception as e:
    #         return TextExtractionResponse(
    #             extracted_text="",
    #             success=False,
    #             error_message=str(e)
    #         )
    async def extract_from_content(self, content: bytes, filename: str) -> TextExtractionResponse:
        """Extract text from file content"""
        try:
            # Determine file type from extension
            file_ext = filename.lower().split('.')[-1] if '.' in filename else ''
            
            if file_ext in ['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'gif']:
                extracted_text = self._extract_from_image(content)
            elif file_ext == 'pdf':
                extracted_text = self._extract_from_pdf(content)
            elif file_ext in ['docx', 'doc']:
                extracted_text = self._extract_from_docx(content)
                print(f"Extracted text from DOCX: {extracted_text[:100]}...")  # Debug log here is allright
            else:
                return TextExtractionResponse(
                    success=False,
                    error_message=f"Unsupported file type: {file_ext}"
                )
            
            return TextExtractionResponse(
                success=True,
                extracted_text=extracted_text,
                file_type=file_ext
            )
            
        except Exception as e:
            return TextExtractionResponse(
                success=False,
                error_message=f"Error extracting text: {str(e)}"
            )
        
    @staticmethod
    def _extract_from_pdf(content: bytes) -> str:
        """Extract text from PDF content"""
        pdf_reader = PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    
    @staticmethod
    def _extract_from_docx(content: bytes) -> str:
        """Extract text from DOCX content"""
        doc = Document(io.BytesIO(content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    
    def _extract_from_image(self, content: bytes) -> str:
        """Extract text from image using OCR"""
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(content))

            # Convert PIL Image to numpy array
            image_np = np.array(image)
            
            # Use EasyOCR to extract text
            results = self.reader.readtext(image_np)

            # Extract text from results
            extracted_text = " ".join([result[1] for result in results])
            print(f"Extracted text from image: {extracted_text[:100]}...")
            return extracted_text.strip()
            

        except Exception as e:
            print(f"Error in OCR extraction: {str(e)}")
            raise