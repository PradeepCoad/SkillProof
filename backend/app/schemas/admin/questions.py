from pydantic import BaseModel

class AdminQuestionCreate(BaseModel):
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str

class AdminQuestionUpdate(BaseModel):
    question: str | None = None
    option_a: str | None = None
    option_b: str | None = None
    option_c: str | None = None
    option_d: str | None = None
    correct_option: str | None = None

class AdminQuestionResponse(AdminQuestionCreate):
    id: int
    skill_id: int

    class Config:
        from_attributes = True