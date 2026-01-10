from pydantic import BaseModel
from typing import List, Optional

class PortfolioSkill(BaseModel):
    name: str
    score: float

class PortfolioProject(BaseModel):
    title: str
    description: Optional[str]
    tech_stack: Optional[str]
    github_url: Optional[str]
    live_url: Optional[str]

    class Config:
        from_attributes = True

class PortfolioResponse(BaseModel):
    name: str
    email: str
    skills: List[PortfolioSkill]
    projects: List[PortfolioProject]