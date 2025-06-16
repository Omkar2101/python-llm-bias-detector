import pytest
from fastapi import UploadFile
from app.services.text_extractor import TextExtractor
from app.models.schemas import TextExtractionResponse
import io
import os

@pytest.fixture
def text_extractor():
    return TextExtractor()

@pytest.mark.asyncio
async def test_extract_text_from_txt():
    # Create a mock text file
    content = "This is a test document."
    file = UploadFile(
        filename="test.txt",
        file=io.BytesIO(content.encode())
    )
    
    result = await TextExtractor.extract_from_file(file)
    assert isinstance(result, TextExtractionResponse)
    assert result.text == content
    assert result.success is True

@pytest.mark.asyncio
async def test_extract_text_from_pdf():
    # Create a mock PDF file content
    pdf_content = b"%PDF-1.4\n..."  # Minimal PDF content
    file = UploadFile(
        filename="test.pdf",
        file=io.BytesIO(pdf_content)
    )
    
    result = await TextExtractor.extract_from_file(file)
    assert isinstance(result, TextExtractionResponse)
    assert result.success is True

@pytest.mark.asyncio
async def test_extract_text_from_image():
    # Create a mock image file
    image_content = b"mock image content"
    file = UploadFile(
        filename="test.png",
        file=io.BytesIO(image_content)
    )
    
    result = await TextExtractor.extract_from_file(file)
    assert isinstance(result, TextExtractionResponse)
    assert result.success is True

@pytest.mark.asyncio
async def test_invalid_file_type():
    # Test with an unsupported file type
    file = UploadFile(
        filename="test.xyz",
        file=io.BytesIO(b"some content")
    )
    
    result = await TextExtractor.extract_from_file(file)
    assert isinstance(result, TextExtractionResponse)
    assert result.success is False
    assert "Unsupported file type" in result.error

@pytest.mark.asyncio
async def test_empty_file():
    # Test with an empty file
    file = UploadFile(
        filename="empty.txt",
        file=io.BytesIO(b"")
    )
    
    result = await TextExtractor.extract_from_file(file)
    assert isinstance(result, TextExtractionResponse)
    assert result.success is False
    assert "Empty file" in result.error
