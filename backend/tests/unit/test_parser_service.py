import pytest
from fastapi import HTTPException
from app.services.parser_service import ParserService

@pytest.fixture
def parser_service():
    return ParserService()

@pytest.mark.asyncio
async def test_parse_job_requirements(parser_service):
    requirements = "Looking for a Python developer with 5+ years experience"
    job = await parser_service.parse_job_requirements(requirements)
    assert "python" in job.required_skills
    assert "developer" in job.required_skills

@pytest.mark.asyncio
async def test_parse_resume_invalid_type(parser_service):
    with pytest.raises(HTTPException):
        await parser_service.parse_resume(b"test content", "invalid/type")
