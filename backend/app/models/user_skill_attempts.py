from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean, DateTime
from datetime import datetime

from database.pg_db import Base

class UserSkillAttempt(Base):
    __tablename__ = "user_skill_attempts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))

    score = Column(Float)
    passed = Column(Boolean, default=False)
    attempted_at = Column(DateTime, default=datetime.utcnow)
