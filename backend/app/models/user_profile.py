from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database.pg_db import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    bio = Column(Text, nullable=True)
    gender = Column(String(20), nullable=True)
    qualification = Column(String(150), nullable=True)
    experience = Column(String(50), nullable=True)
    location = Column(String(100), nullable=True)

    insta_url = Column(String(255), nullable=True)
    linkedin_url = Column(String(255), nullable=True)
    github_url = Column(String(255), nullable=True)