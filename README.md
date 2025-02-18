# Resume Matcher

A FastAPI and React-based application for matching resumes to job positions using advanced NLP techniques.

## Features

- Automated skill extraction saves manual review time
- Bulk processing capability for multiple positions/resumes
- Clear match explanations for quick decision making
- Configurable matching criteria
- Export functionality for integration with other systems

## Architecture

The system follows a microservice architecture with:

- FastAPI backend with modular services
- React frontend with TypeScript
- In-memory caching for performance
- Batch processing for bulk operations
- Security middleware for authentication

### Performance Optimizations

- Caching for parsed documents
- Batch processing for bulk uploads
- Asynchronous matching for large datasets
- Incremental updates for changed requirements

### Security Features

- Resume data encryption
- Access control for sensitive information
- Audit logging for compliance

### Scalability Features

- Horizontally scalable architecture
- Queue-based processing for large workloads
- Modular design for easy extensions

## API Documentation

### Authentication

All endpoints require authentication using Bearer tokens:

```
Authorization: Bearer <token>
```

### Endpoints

#### POST /api/jobs
Create a new job position with requirements.

Request:
```json
{
  "requirements": "Looking for a Python developer with React experience"
}
```

Response:
```json
{
  "id": "job-id",
  "required_skills": ["python", "react"],
  "preferred_skills": ["aws"],
  "min_experience_years": 3,
  "education_level": "Bachelors"
}
```

#### POST /api/resumes
Upload and parse a resume (PDF only).

Request:
- Multipart form data with "file" field

Response:
```json
{
  "skills": ["python", "react", "aws"],
  "experience": [
    {
      "years": 5,
      "description": "Software Developer"
    }
  ],
  "education": [
    {
      "level": "Masters",
      "description": "Computer Science"
    }
  ]
}
```

#### GET /api/matches/{job_id}/top
Get top matching candidates for a job.

Response:
```json
[
  {
    "id": "match-id",
    "match_details": {
      "total_score": 0.85,
      "skill_match_score": 0.9,
      "matched_required_skills": ["python", "react"]
    },
    "resume": {
      "skills": ["python", "react", "aws"],
      "experience": [...],
      "education": [...]
    }
  }
]
```

## Development Setup

1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m pytest  # Run tests
python -m fastapi dev app/main.py  # Start development server
```

2. Frontend Setup
```bash
cd frontend/resume-matcher-ui
npm install
npm run dev
```

## Deployment

1. Backend Deployment
```bash
cd backend
<deploy_backend dir="." />
```

2. Frontend Deployment
```bash
cd frontend/resume-matcher-ui
npm run build
<deploy_frontend dir="dist" />
```

## Testing

Run the test suite:
```bash
cd backend
python -m pytest
```

The test suite includes:
- Unit tests for all services
- Integration tests for the full pipeline
- Validation metrics for matching accuracy
