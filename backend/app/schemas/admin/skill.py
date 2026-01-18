from pydantic import BaseModel
from typing import Optional

class AdminSkillCreate(BaseModel):
    name: str

class AdminSkillUpdate(BaseModel):
    name: str | None = None

class AdminSkillResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True