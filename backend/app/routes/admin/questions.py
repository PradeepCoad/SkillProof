from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.pg_db import SessionLocal
from models.question import Question
from models.skill import Skill
from routes.admin.deps import get_current_admin
from schemas.admin.questions import AdminQuestionResponse, AdminQuestionCreate, AdminQuestionUpdate
from utils.audit_logger import log_action


router = APIRouter(prefix="/admin/questions", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Create Question
@router.post("/{skill_id}", response_model=AdminQuestionResponse)
def create_question(
    skill_id: int,
    payload: AdminQuestionCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")  
    
    question = Question(skill_id=skill_id, **payload.dict())
    db.add(question)
    db.commit()
    db.refresh(question)
    # log_action(
    #     db,
    #     action="CREATE",
    #     entity="QUESTION",
    #     entity_id=question.id,
    #     user_id=admin.id,
    #     message="Question created"
    # ) 
    return question

#get all questions
@router.get("/{skill_id}", response_model=list[AdminQuestionResponse])
def get_all_questions(
    skill_id:int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    return db.query(Question).filter(Question.skill_id == skill_id).all()
    
#update question by id
@router.put("/{question_id}", response_model=AdminQuestionResponse)
def update_question(
    question_id: int,
    payload: AdminQuestionUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(question, key, value)
    
    db.commit()
    
    # log_action(
    #     db,
    #     action="UPDATE",
    #     entity="QUESTION",
    #     entity_id=question.id,
    #     user_id=admin.id,
    #     message="Question updated"
    # )
    
    db.refresh(question)
    return question

#delete question by id
@router.delete("/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db.delete(question)
    db.commit()
    
    # log_action(
    #     db,
    #     action="DELETE",
    #     entity="QUESTION",
    #     entity_id=question.id,
    #     user_id=admin.id,
    #     message="Question deleted"
    # )
    
    return {"detail": "Question deleted successfully"}
