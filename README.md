# Python LLM Bias Detector

## Description
Python LLM Bias Detector is an AI-powered API service designed to detect bias and suggest language improvements in job descriptions. It helps organizations create more inclusive and clear job postings by analyzing text or uploaded documents for biased language and providing actionable suggestions.

## Features
- Extract text from various file formats including PDF, DOCX, and images.
- Analyze job description text for bias, inclusivity, and clarity.
- Provide detailed bias issues and improvement suggestions.
- Convenient endpoint to extract and analyze uploaded files in one step.
- Robust error handling and validation.
- CORS support for integration with frontend applications.
- Dockerized for easy deployment.
- Comprehensive test coverage with pytest.

## Tech Stack
- Python 3.10
- FastAPI for building the API
- Uvicorn as ASGI server
- Pydantic for data validation
- Transformers, Torch, NLTK for NLP and AI models
- Google Generative AI SDK
- PyPDF, python-docx, Pillow for file processing
- EasyOCR for text extraction from images
- pytest for testing

## Getting Started

### Prerequisites
- Python 3.10+
- Docker (optional, for containerized deployment)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd python-llm-bias-detector
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory to set environment variables as needed.

### Running the App

Run the FastAPI server locally:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.

### Environment Variables

Environment variables can be set in a `.env` file. The project uses `python-dotenv` to load them. Example variables might include API keys or configuration options (not explicitly listed here).

## Usage

### API Endpoints

- `GET /`  
  Returns a welcome message and status.

- `GET /health`  
  Health check endpoint.

- `POST /extract`  
  Upload a file (PDF, DOCX, image) to extract text.  
  Request: multipart/form-data with file field.  
  Response: extracted text and file type.

- `POST /analyze`  
  Analyze job description text for bias.  
  Request: JSON with `text` field (minimum 50 characters).  
  Response: bias analysis results including scores, issues, and suggestions.

- `POST /analyze-file`  
  Upload a file to extract text and analyze bias in one step.  
  Request: multipart/form-data with file field.  
  Response: extracted text and bias analysis.

### Example Usage

Use tools like `curl` or Postman to interact with the API. For example, to analyze text:

```bash
curl -X POST "http://localhost:8000/analyze" -H "Content-Type: application/json" -d '{"text": "Your job description text here..."}'
```

## Folder Structure

```
python-llm-bias-detector/
├── app/                    # Application source code
│   ├── main.py             # FastAPI app and routes
│   ├── models/             # Pydantic schemas
│   ├── services/           # Business logic (text extraction, bias detection)
│   └── utils/              # Helper utilities
├── tests/                  # Test cases and evaluation data
├── Dockerfile              # Docker image build instructions
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not committed)
└── README.md               # This file
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes with clear commit messages.
4. Run tests to ensure nothing is broken.
5. Submit a pull request describing your changes.

Please adhere to the existing code style and write tests for new features.

## Tests

Tests are written using `pytest` and can be run with:

```bash
pytest
```

For coverage report:

```bash
pytest --cov=app tests/
```

## Docker Support

Build the Docker image:

```bash
docker build -t python-llm-bias-detector .
```

Run the container:

```bash
docker run -p 8000:8000 python-llm-bias-detector
```

The API will be accessible at `http://localhost:8000`.

## CI/CD

