from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.pg_db import SessionLocal
from models.skill import Skill
from routes.admin.deps import get_current_admin
from schemas.admin.skill import AdminSkillResponse, AdminSkillCreate, AdminSkillUpdate
from utils.audit_logger import log_action

router = APIRouter(prefix="/admin/skills", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Create Skill
@router.post("", response_model=AdminSkillResponse)
def create_skill(
    payload: AdminSkillCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    skill = Skill(**payload.dict())
    db.add(skill)
    db.commit()
    db.refresh(skill)
    
    # log_action(
    #     db,
    #     action="CREATE",
    #     entity="SKILL",
    #     entity_id=skill.id,
    #     user_id=admin.id,
    #     message="Skill created"
    # )
    
    
    return skill

#get all skills
@router.get("", response_model=list[AdminSkillResponse])
def get_all_skills(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    return db.query(Skill).order_by(Skill.id.desc()).all()


#update skill by id
@router.put("/{skill_id}", response_model=AdminSkillResponse)
def update_skill(
    skill_id: int,
    payload: AdminSkillUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(skill, key, value)
    
    db.commit()
    
    # log_action(
    #     db,
    #     action="UPDATE",
    #     entity="SKILL",
    #     entity_id=skill.id,
    #     user_id=admin.id,
    #     message="Skill updated"
    # )
    
    db.refresh(skill)
    return skill

#delete skill by id
@router.delete("/{skill_id}")
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    db.delete(skill)
    db.commit()
    
    # log_action(
    #     db,
    #     action="DELETE",
    #     entity="SKILL",
    #     entity_id=skill.id,
    #     user_id=admin.id,
    #     message="Skill deleted"
    # )
    
    return {"msg": "Skill deleted successfully"}
