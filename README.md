# PDF to JSON API

A FastAPI-based REST API for converting PDF documents to structured JSON format. Built with Python, featuring rate limiting, API key authentication, and Docker support.

## Features

- PDF to JSON conversion using pdfplumber
- RESTful API with FastAPI
- JWT authentication
- API key-based access control
- Rate limiting for abuse prevention
- Docker containerization
- PostgreSQL database support
- Comprehensive error handling

## Installation

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)

### Local Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd PDF-to-JSON-API
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker Setup

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /api/v1/health
```

### Authentication
```
POST /api/v1/auth/register
POST /api/v1/auth/token
```

### PDF Conversion
```
POST /api/v1/upload          # Upload PDF file
POST /api/v1/convert         # Convert uploaded PDF to JSON
POST /api/v1/convert-url     # Convert PDF from URL
```

## Example Usage

### Upload and Convert PDF

```bash
curl -X POST "http://localhost:8000/api/v1/convert" \
  -H "X-API-Key: default-key" \
  -F "file=@document.pdf"
```

### Convert PDF from URL

```bash
curl -X POST "http://localhost:8000/api/v1/convert-url" \
  -H "X-API-Key: default-key" \
  -d "url=https://example.com/document.pdf"
```

## Response Format

```json
{
  "document_id": 123,
  "filename": "document.pdf",
  "json_output": {
    "metadata": {...},
    "text_content": {...},
    "tables": {...},
    "images": {...}
  },
  "status": "completed",
  "message": "PDF converted to JSON successfully"
}
```

## Project Structure

```
app/
├── api_keys.py      # API key middleware
├── auth.py          # JWT authentication
├── main.py          # FastAPI application
├── models/
│   └── base.py      # SQLAlchemy models
├── pdf_processor.py # PDF processing logic
├── rate_limit.py    # Rate limiting
├── routes/
│   ├── __init__.py
│   └── api.py       # API endpoints
├── schemas.py       # Pydantic schemas
└── __init__.py
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT secret key | `your-secret-key-here` |
| `API_KEYS` | Comma-separated API keys | `default-key` |
| `UPLOAD_DIR` | Directory for uploaded files | `uploads` |
| `DATABASE_URL` | PostgreSQL connection string | - |

## License

MIT License