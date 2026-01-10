from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database.pg_db import SessionLocal
from models.skill import Skill
from models.question import Question
from models.user_skill import UserSkill
from routes.deps import get_current_user
from schemas.skill import SkillResponse, QuestionResponse, AssessmentSubmit

router = APIRouter(prefix="/skills", tags=["Skills"])
COOLDOWN_HOURS = 24
PASS_SCORE = 70

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#list all skills
@router.get("", response_model=list[SkillResponse])
def list_skills(db: Session = Depends(get_db)):
    return db.query(Skill).all()

#get questions for a skill
@router.get("/{skill_id}/questions", response_model=list[QuestionResponse])
def get_questions(skill_id: int, db: Session = Depends(get_db)):

    return db.query(Question).filter(Question.skill_id == skill_id).all()


#submit assisment
@router.post("/{skill_id}/submit")
def submit_assessment(
    skill_id:int,
    payload: AssessmentSubmit,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    #existing attempt check
    recent_attempt = db.query(UserSkill).filter(
        UserSkill.user_id == current_user.id,
        UserSkill.skill_id == skill_id
    ).first()

    if recent_attempt:
        time_diff = datetime.utcnow() - recent_attempt.last_attempt
        if time_diff < timedelta(hours=COOLDOWN_HOURS):
            remaining = timedelta(hours=COOLDOWN_HOURS) - time_diff
            raise HTTPException(
                status_code=429,
                detail=f"Retry allowed after {remaining.seconds // 3600} hours"
            )

    #Feching questions
    questions = db.query(Question).filter(Question.skill_id == skill_id).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    

    #converting answers to dict
    answer_map = {
        answer.question_id: answer.selected_option for answer in payload.answers
    }

    #evaluating score
    correct = 0
    for question in questions:
        user_answer = answer_map.get(question.id)
        if user_answer and user_answer == question.correct_option:
            correct += 1

    score = (correct / len(questions)) * 100
    passed = score >= PASS_SCORE

    #Best score update
    if recent_attempt:
        if score > recent_attempt.score:
            recent_attempt.score = score
            recent_attempt.passed = passed
        recent_attempt.last_attempt = datetime.utcnow()
    else:
        recent_attempt = UserSkill(
            user_id = current_user.id,
            skill_id = skill_id,
            score = score,
            passed = passed,
            last_attempt = datetime.utcnow()
        )
        db.add(recent_attempt)
            
    db.commit()

    return {
        "score": score,
        "passed": passed,
        "best_score": recent_attempt.score
    }