from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from database.pg_db import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    tech_stack = Column(String(300), nullable=True)
    github_url = Column(String(300), nullable=True)
    live_url = Column(String(300), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
