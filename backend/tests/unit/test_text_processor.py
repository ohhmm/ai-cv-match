import pytest
from app.utils.text_processor import TextProcessor

@pytest.fixture
def text_processor():
    return TextProcessor()

def test_preprocess_text(text_processor):
    text = "This is a TEST with Numbers 123 and Symbols !@#"
    processed = text_processor.preprocess_text(text)
    assert "test" in processed
    assert "123" not in processed
    assert "!@#" not in processed

def test_extract_skills(text_processor):
    text = "Proficient in Python programming and Machine Learning"
    skills = text_processor.extract_skills(text)
    assert "python" in skills
    assert "programming" in skills
    assert "machine learning" in skills

def test_calculate_similarity(text_processor):
    text1 = "Python developer with machine learning experience"
    text2 = "Looking for Python developer with ML skills"
    similarity = text_processor.calculate_similarity(text1, text2)
    assert 0 <= similarity <= 1
