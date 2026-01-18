from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.pg_db import SessionLocal
from models.user import User
from schemas.admin.users import AdminUserResponse, AdminUserUpdate
from routes.admin.deps import get_current_admin
from utils.audit_logger import log_action


router = APIRouter(prefix="/admin/users", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#get all users
@router.get("", response_model=list[AdminUserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    return db.query(User).order_by(User.id.desc()).all()

#get user by id
@router.get("/{user_id}", response_model=AdminUserResponse)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#update user by id
@router.put("/{user_id}", response_model=AdminUserResponse)
def update_user_by_id(
    user_id: int,
    payload: AdminUserUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(user, key, value)
    
    db.commit()
    
    # log_action(
    #     db,
    #     action="UPDATE",
    #     entity="USER",
    #     entity_id=user.id,
    #     user_id=admin.id,
    #     message=f"Admin {admin.name} updated user {user.id}"
    # )

    db.refresh(user)
    return user

#delete user by id
@router.delete("/{user_id}")
def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = False
    db.commit()
    
    # log_action(
    #     db,
    #     action="DELETE",
    #     entity="USER",
    #     entity_id=user.id,
    #     user_id=admin.id,
    #     message=f"Admin {admin.name} deleted user {user.id}"
    # )

    return {"detail": "User deleted successfully"}