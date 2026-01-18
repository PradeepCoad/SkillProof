from pydantic import BaseModel, EmailStr
from datetime import datetime

class AdminUserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True

class AdminUserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None