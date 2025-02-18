from typing import List, Dict, Optional
from ..models.resume import Resume
from ..models.job import JobRequirements
from ..utils.text_processor import TextProcessor

class MatchingService:
    def __init__(self):
        self.text_processor = TextProcessor()

    async def calculate_skill_match_score(self, resume_skills: List[str], job_skills: List[str]) -> float:
        """Calculate skill match score based on required skills"""
        if not job_skills:
            return 0.0
        
        matched_skills = set(resume_skills).intersection(set(job_skills))
        return len(matched_skills) / len(job_skills)

    async def match_resume_to_job(self, resume: Resume, job: JobRequirements) -> Dict:
        """Match resume against job requirements and return score with explanation"""
        try:
            # Calculate skill match score
            skill_score = await self.calculate_skill_match_score(resume.skills, job.required_skills)
            
            # Calculate preferred skills score
            preferred_score = 0.0
            if job.preferred_skills:
                preferred_score = await self.calculate_skill_match_score(resume.skills, job.preferred_skills)
            
            # Calculate weighted total score
            total_score = (skill_score * 0.7) + (preferred_score * 0.3)
            
            return {
                "total_score": total_score,
                "skill_match_score": skill_score,
                "preferred_skills_score": preferred_score,
                "matched_required_skills": list(set(resume.skills).intersection(set(job.required_skills))),
                "matched_preferred_skills": list(set(resume.skills).intersection(set(job.preferred_skills))) if job.preferred_skills else []
            }
        except Exception as e:
            raise Exception(f"Error matching resume to job: {str(e)}")

    async def rank_candidates(self, job: JobRequirements, candidates: List[Resume]) -> List[Dict]:
        """Rank candidates for a job and return top matches with explanations"""
        try:
            matches = []
            for candidate in candidates:
                match_result = await self.match_resume_to_job(candidate, job)
                matches.append({
                    "resume": candidate,
                    "match_details": match_result
                })
            
            # Sort by total score and get top 10
            matches.sort(key=lambda x: x["match_details"]["total_score"], reverse=True)
            return matches[:10]
        except Exception as e:
            raise Exception(f"Error ranking candidates: {str(e)}")
