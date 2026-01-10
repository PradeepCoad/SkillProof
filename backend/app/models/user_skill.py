from sqlalchemy import Column, Integer, ForeignKey,Boolean, Float, DateTime
from datetime import datetime
from database.pg_db import Base

class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))

    score = Column(Float)
    passed = Column(Boolean, default=False)

    last_attempt = Column(DateTime, default=datetime.utcnow)