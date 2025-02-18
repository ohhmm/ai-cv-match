import re
from typing import List, Dict, Optional
from datetime import datetime

class ExperienceExtractor:
    def __init__(self):
        self.year_pattern = r'(\d{4})'
        self.duration_pattern = r'(\d+)\+?\s*(year|yr|years)'
        
    def extract_years_of_experience(self, text: str) -> Optional[int]:
        """Extract years of experience from text"""
        # Look for explicit duration mentions
        duration_matches = re.findall(self.duration_pattern, text.lower())
        if duration_matches:
            return int(duration_matches[0][0])
            
        # Look for year ranges
        years = re.findall(self.year_pattern, text)
        if len(years) >= 2:
            try:
                start_year = int(min(years))
                end_year = int(max(years))
                current_year = datetime.now().year
                if end_year > current_year:
                    end_year = current_year
                return end_year - start_year
            except ValueError:
                return None
                
        return None

    def extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience entries from text"""
        # For now, return basic structure
        # In a real implementation, this would use more sophisticated NLP
        experience = []
        years = self.extract_years_of_experience(text)
        if years:
            experience.append({
                "years": years,
                "description": text
            })
        return experience
