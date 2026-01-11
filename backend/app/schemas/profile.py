from pydantic import BaseModel
from typing import Optional

class ProfileCreateUpdate(BaseModel):
    bio: Optional[str] = None
    gender: Optional[str] = None
    qualification: Optional[str] = None
    experience: Optional[str] = None
    location: Optional[str] = None

    insta_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None


class ProfileResponse(ProfileCreateUpdate):
    
    class Config:
        from_attributes = True