from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.pg_db import SessionLocal
from models.user import User
from models.project import Project
from models.user_skill import UserSkill
from models.skill import Skill
from schemas.portfolio import PortfolioResponse

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{username}", response_model=PortfolioResponse)
def get_portfolio(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    projects = db.query(Project).filter(Project.user_id == user.id).all()

    user_skills = db.query(Skill.name, UserSkill.score).join(UserSkill,Skill.id == UserSkill.skill_id).filter(UserSkill.user_id == user.id, UserSkill.passed == True).all()

    return {
        "name": user.name,
        "email": user.email,
        "projects": projects,
        "skills": [
            {"name": name, "score": score} for name,score in user_skills
            ]
    }