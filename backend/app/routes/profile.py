from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils.audit_logger import log_action
from database.pg_db import SessionLocal
from models.user_profile import UserProfile
from schemas.profile import ProfileCreateUpdate, ProfileResponse
from routes.deps import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=ProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("", response_model=ProfileResponse)
def create_or_update_profile(
    payload: ProfileCreateUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if profile:
        # Update existing profile
        for key, value in payload.dict(exclude_unset=True).items():
            setattr(profile, key, value)
    else:
        # Create new profile
        profile = UserProfile(
            user_id=current_user.id,
            **payload.dict()
        )
        db.add(profile)
    
    db.commit()
    
    log_action(
        db,
        action="UPDATE",
        entity="PROFILE",
        entity_id=current_user.id,
        user_id=current_user.id,
        message="User profile updated"
    )

    db.refresh(profile)
    return profile