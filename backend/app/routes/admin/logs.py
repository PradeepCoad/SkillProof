from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.pg_db import SessionLocal
from models.audit_log import AuditLog
from routes.admin.deps import get_current_admin

router = APIRouter(prefix="/admin/logs", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def get_all_logs(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    return (db.query(AuditLog).order_by(AuditLog.created_at.desc()).all())