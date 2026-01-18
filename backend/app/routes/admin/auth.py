from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from database.pg_db import SessionLocal
from utils.audit_logger import log_action
from models.admin import Admin
from core.admin_security import create_admin_token,verify_password

router = APIRouter(prefix="/admin/auth", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def admin_login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    admin = db.query(Admin).filter(Admin.name == form.username).first()
    if not admin or not verify_password(form.password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_admin_token({"sub":admin.name})
    
    # log_action(
    #     db,
    #     action="LOGIN",
    #     entity="ADMIN",
    #     entity_id=admin.id,
    #     user_id=admin.id,
    #     message="Admin logged in"
    # )
    return {"access_token": token, "token_type": "bearer"}