from pydantic import BaseModel
from typing import List, Optional

class Resume(BaseModel):
    skills: List[str]
    experience: Optional[List[dict]]
    education: Optional[List[dict]]
