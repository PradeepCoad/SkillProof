from sqlalchemy import Column, Integer, String, ForeignKey
from database.pg_db import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    question = Column(String(500), nullable=False)

    option_a = Column(String(200))
    option_b = Column(String(200))
    option_c = Column(String(200))
    option_d = Column(String(200))

    correct_option = Column(String(1))  # a, b, c, d