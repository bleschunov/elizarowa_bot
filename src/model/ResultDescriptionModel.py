from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base


class ResultDescriptionModel(Base):
    __tablename__ = "result_description"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    max_score = Column(Integer)
    test_id = Column(Integer, ForeignKey('test.id'))
