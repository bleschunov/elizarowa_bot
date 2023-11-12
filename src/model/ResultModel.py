from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base


class ResultModel(Base):
    __tablename__ = "result"

    id = Column(Integer, primary_key=True)
    total_score = Column(String)
    telegram_user_id = Column(Integer)
    test_id = Column(Integer, ForeignKey('test.id'))
    result_description_id = Column(Integer, ForeignKey('result_description.id'))
