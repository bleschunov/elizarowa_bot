from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base


class QuestionModel(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    test_id = Column(Integer, ForeignKey('test.id'))
