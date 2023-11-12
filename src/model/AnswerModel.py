from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base


class AnswerModel(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    description = Column(String)
    score = Column(Integer)
    question_id = Column(Integer, ForeignKey('question.id'))
