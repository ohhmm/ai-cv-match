from pydantic import BaseModel
from typing import List, Optional

class JobRequirements(BaseModel):
    id: str = "test-job-id"
    title: str = "Software Developer"
    required_skills: List[str]
    preferred_skills: Optional[List[str]] = None
    min_experience_years: Optional[int] = None
    education_level: Optional[str] = None
