from pydantic import BaseModel
from datetime import datetime
from typing import List

class SkillResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class QuestionResponse(BaseModel):
    id: int
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str

    class Config:
        from_attributes = True

class AnswerSubmit(BaseModel):
    question_id: int
    selected_option: str

class AssessmentSubmit(BaseModel):
    answers: List[AnswerSubmit]


class AttemptHistoryResponse(BaseModel):
    skill_id: int
    score: float
    passed: bool
    attempted_at: datetime

    class Config:
        from_attributes = True
    

class PassedSkillResponse(BaseModel):
    skill_id : int
    score : float

    class Config:
        from_attributes = True