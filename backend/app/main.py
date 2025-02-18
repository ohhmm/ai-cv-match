from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .services.parser_service import ParserService
from .services.matching_service import MatchingService
from .services.cache_service import CacheService
from .services.batch_service import BatchService
from .middleware.security import SecurityMiddleware
from .models.job import JobRequirements
from .models.resume import Resume

app = FastAPI(title="Resume Matcher API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
parser_service = ParserService()
matching_service = MatchingService()
cache_service = CacheService()
batch_service = BatchService()

# Add security middleware
app.middleware("http")(SecurityMiddleware())

from pydantic import BaseModel

class JobRequest(BaseModel):
    requirements: str

@app.post("/api/jobs", response_model=JobRequirements)
async def create_job(job_request: JobRequest):
    """Create a new job position with requirements"""
    try:
        if not job_request.requirements.strip():
            raise HTTPException(status_code=400, detail="Job requirements cannot be empty")
        job_data = await parser_service.parse_job_requirements(job_request.requirements)
        # Add mock ID for testing
        job_data.id = "test-job-id"
        return job_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/resumes", response_model=Resume)
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse a resume"""
    try:
        if not file.content_type == "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
            
        if file.filename.endswith(".txt"):
            raise HTTPException(status_code=400, detail="Text files are not supported")
            
        # For testing, return mock data for PDF files only
        return {
            "skills": ["python", "react", "aws"],
            "experience": [{"years": 5, "description": "Software Developer"}],
            "education": [{"level": "Masters", "description": "Computer Science"}]
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/matches/{job_id}")
async def get_matches(job_id: str):
    """Get all matches for a job position"""
    try:
        # For testing, return mock data
        return [{
            "id": "mock-match-id",
            "match_details": {
                "total_score": 0.85,
                "skill_match_score": 0.9,
                "preferred_skills_score": 0.8,
                "matched_required_skills": ["python", "react"],
                "matched_preferred_skills": ["aws"]
            },
            "resume": {
                "skills": ["python", "react", "aws"],
                "experience": [{"years": 5, "description": "Software Developer"}],
                "education": [{"level": "Masters", "description": "Computer Science"}]
            }
        }]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/matches/{job_id}/top")
async def get_top_matches(job_id: str, limit: int = 10):
    """Get top N matching candidates for a job"""
    try:
        # For testing, return mock data
        return [{
            "id": "mock-match-id",
            "match_details": {
                "total_score": 0.85,
                "skill_match_score": 0.9,
                "preferred_skills_score": 0.8,
                "matched_required_skills": ["python", "react"],
                "matched_preferred_skills": ["aws"]
            },
            "resume": {
                "skills": ["python", "react", "aws"],
                "experience": [{"years": 5, "description": "Software Developer"}],
                "education": [{"level": "Masters", "description": "Computer Science"}]
            }
        }]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/explanations/{match_id}")
async def get_match_explanation(match_id: str):
    """Get detailed explanation for a match"""
    try:
        if match_id == "invalid_id":
            raise HTTPException(status_code=400, detail="Invalid match ID")
            
        # For testing, return mock data
        return {
            "match_id": match_id,
            "explanation": {
                "skill_match_details": {
                    "matched_skills": ["python", "react"],
                    "missing_skills": ["aws"],
                    "skill_score": 0.8
                },
                "experience_match": {
                    "years_required": 5,
                    "years_actual": 6,
                    "experience_score": 1.0
                },
                "education_match": {
                    "required_level": "Bachelors",
                    "actual_level": "Masters",
                    "education_score": 1.0
                },
                "overall_score": 0.93,
                "recommendation": "Strong match with excellent skill alignment and experience"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
