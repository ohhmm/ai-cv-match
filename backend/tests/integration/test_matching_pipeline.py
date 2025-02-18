import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.validation_service import ValidationService

client = TestClient(app)
validation_service = ValidationService()

def test_create_job_and_match():
    # Create a job
    job_data = {
        "requirements": "Looking for a Python developer with React experience"
    }
    # Add mock authentication token
    headers = {"Authorization": "Bearer mock_token"}
    response = client.post("/api/jobs", json=job_data, headers=headers)
    assert response.status_code == 200
    job_data = response.json()
    
    # Verify required skills were extracted
    assert "python" in [skill.lower() for skill in job_data["required_skills"]]
    assert "react" in [skill.lower() for skill in job_data["required_skills"]]

    # Upload a resume
    with open("tests/fixtures/test_resume.pdf", "rb") as f:
        response = client.post(
            "/api/resumes",
            files={"file": ("test_resume.pdf", f, "application/pdf")},
            headers={"Authorization": "Bearer mock_token"}
        )
    assert response.status_code == 200
    resume_data = response.json()
    
    # Get matches
    response = client.get(
        f"/api/matches/{job_data['id']}/top",
        headers={"Authorization": "Bearer mock_token"}
    )
    assert response.status_code == 200
    matches = response.json()
    
    # Validate match quality
    for match in matches:
        # Calculate similarity score
        job_text = " ".join(job_data["required_skills"])
        resume_text = " ".join(resume_data["skills"])
        similarity = validation_service.calculate_match_similarity(job_text, resume_text)
        
        # Record score for distribution analysis
        validation_service.record_match_score(similarity)
        
        # Verify match details are present
        assert "total_score" in match["match_details"]
        assert "skill_match_score" in match["match_details"]
        assert "matched_required_skills" in match["match_details"]

def test_get_match_explanation():
    # Create a job and upload a resume first
    headers = {"Authorization": "Bearer mock_token"}
    job_data = {
        "requirements": "Python developer"
    }
    job_response = client.post("/api/jobs", json=job_data, headers=headers)
    assert job_response.status_code == 200
    job_result = job_response.json()
    job_id = "test-job-id"  # Use mock ID since we don't have a database
    
    with open("tests/fixtures/test_resume.pdf", "rb") as f:
        resume_response = client.post(
            "/api/resumes",
            files={"file": ("test_resume.pdf", f, "application/pdf")},
            headers={"Authorization": "Bearer mock_token"}
        )
    
    # Get matches to get a match ID
    matches_response = client.get(
        f"/api/matches/{job_id}/top",
        headers={"Authorization": "Bearer mock_token"}
    )
    match_id = matches_response.json()[0]["id"]
    
    # Get explanation for the match
    response = client.get(
        f"/api/explanations/{match_id}",
        headers={"Authorization": "Bearer mock_token"}
    )
    assert response.status_code == 200
    explanation = response.json()
    
    # Verify explanation structure
    assert "skill_match_details" in explanation["explanation"]
    assert "experience_match" in explanation["explanation"]
    assert "education_match" in explanation["explanation"]
    assert "recommendation" in explanation["explanation"]

def test_error_handling():
    # Test invalid job requirements
    headers = {"Authorization": "Bearer mock_token"}
    job_data = {
        "requirements": ""
    }
    response = client.post("/api/jobs", json=job_data, headers=headers)
    assert response.status_code == 400
    
    # Test invalid resume format
    response = client.post(
        "/api/resumes",
        files={"file": ("test.txt", b"invalid content")},
        headers={"Authorization": "Bearer mock_token"}
    )
    assert response.status_code == 400
    
    # Test invalid match ID
    response = client.get(
        "/api/explanations/invalid_id",
        headers={"Authorization": "Bearer mock_token"}
    )
    assert response.status_code == 400

    # Test invalid resume format
    response = client.post(
        "/api/resumes",
        files={"file": ("test.txt", b"invalid content", "text/plain")},
        headers={"Authorization": "Bearer mock_token"}
    )
    assert response.status_code == 400
