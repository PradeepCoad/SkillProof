from pydantic import BaseModel
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