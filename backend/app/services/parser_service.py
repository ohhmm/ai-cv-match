from fastapi import HTTPException
import docx
from PyPDF2 import PdfReader
from io import BytesIO
from typing import List, Dict, Optional
from ..utils.text_processor import TextProcessor
from ..utils.experience_extractor import ExperienceExtractor
from ..utils.education_extractor import EducationExtractor
from ..models.resume import Resume
from ..models.job import JobRequirements

class ParserService:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.experience_extractor = ExperienceExtractor()
        self.education_extractor = EducationExtractor()

    async def extract_text_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf = PdfReader(BytesIO(file_content))
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing PDF: {str(e)}")

    async def extract_text_from_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(BytesIO(file_content))
            return " ".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing DOCX: {str(e)}")

    async def parse_resume(self, file_content: bytes, file_type: str) -> Resume:
        """Parse resume content and extract structured information"""
        try:
            # Extract text based on file type
            if file_type == "application/pdf":
                text = await self.extract_text_from_pdf(file_content)
            elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
                text = await self.extract_text_from_docx(file_content)
            else:
                raise HTTPException(status_code=400, detail="Unsupported file type")

            # Extract information
            skills = self.text_processor.extract_skills(text)
            experience = self.experience_extractor.extract_experience(text)
            education = self.education_extractor.extract_education(text)
            
            # Create Resume object
            resume = Resume(
                skills=skills,
                experience=experience,
                education=education
            )
            return resume
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing resume: {str(e)}")

    async def parse_job_requirements(self, requirements: str) -> JobRequirements:
        """Parse and validate job requirements"""
        try:
            # Extract skills from requirements
            skills = self.text_processor.extract_skills(requirements)
            
            # Create JobRequirements object
            job_requirements = JobRequirements(
                title="",  # TODO: Extract title
                required_skills=skills,
                preferred_skills=[],  # TODO: Differentiate required vs preferred
                min_experience_years=None,
                education_level=None
            )
            return job_requirements
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing requirements: {str(e)}")
