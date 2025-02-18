import pytest
from app.utils.experience_extractor import ExperienceExtractor
from app.utils.education_extractor import EducationExtractor

@pytest.fixture
def experience_extractor():
    return ExperienceExtractor()

@pytest.fixture
def education_extractor():
    return EducationExtractor()

def test_extract_years_of_experience(experience_extractor):
    text = "5+ years of experience in software development"
    years = experience_extractor.extract_years_of_experience(text)
    assert years == 5

    text = "Worked from 2018 to 2023 as a developer"
    years = experience_extractor.extract_years_of_experience(text)
    assert years == 5

def test_extract_experience(experience_extractor):
    text = "5+ years of experience in software development"
    experience = experience_extractor.extract_experience(text)
    assert len(experience) == 1
    assert experience[0]["years"] == 5
    assert "software development" in experience[0]["description"]

def test_extract_education_level(education_extractor):
    text = "Ph.D. in Computer Science"
    level = education_extractor.extract_education_level(text)
    assert level == "PhD"

    text = "Master's degree in Engineering"
    level = education_extractor.extract_education_level(text)
    assert level == "Masters"

    text = "B.S. in Computer Science"
    level = education_extractor.extract_education_level(text)
    assert level == "Bachelors"

def test_extract_education(education_extractor):
    text = "Master's degree in Computer Science"
    education = education_extractor.extract_education(text)
    assert len(education) == 1
    assert education[0]["level"] == "Masters"
    assert "Computer Science" in education[0]["description"]
