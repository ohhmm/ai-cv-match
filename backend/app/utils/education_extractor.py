import re
from typing import List, Dict, Optional

class EducationExtractor:
    def __init__(self):
        self.degree_patterns = {
            "phd": r"ph\.?d\.?|doctor of philosophy",
            "masters": r"master'?s|m\.?s\.?|m\.?eng\.?|m\.?b\.?a\.?",
            "bachelors": r"bachelor'?s|b\.?s\.?|b\.?a\.?|b\.?eng\.?"
        }
        
    def extract_education_level(self, text: str) -> Optional[str]:
        """Extract highest education level from text"""
        text = text.lower()
        
        # Check for each degree level
        if re.search(self.degree_patterns["phd"], text):
            return "PhD"
        elif re.search(self.degree_patterns["masters"], text):
            return "Masters"
        elif re.search(self.degree_patterns["bachelors"], text):
            return "Bachelors"
            
        return None

    def extract_education(self, text: str) -> List[Dict]:
        """Extract education entries from text"""
        # For now, return basic structure with highest degree
        # In a real implementation, this would use more sophisticated NLP
        education = []
        level = self.extract_education_level(text)
        if level:
            education.append({
                "level": level,
                "description": text
            })
        return education
