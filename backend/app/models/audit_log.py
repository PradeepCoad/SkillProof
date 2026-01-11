from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from database.pg_db import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    action = Column(String(50), nullable=False)
    entity = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=True)

    message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)



#action: CREATE / UPDATE / DELETE / LOGIN / SUBMIT
#entity: USER / PROJECT / SKILL / ASSESSMENT
#entity_id: ID of the entity on which action is performed
#message: Additional info about the action
#user_id: ID of the user who performed the action