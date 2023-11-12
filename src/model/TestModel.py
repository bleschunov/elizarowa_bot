from sqlalchemy import Column, Integer, String
from db import Base


class TestModel(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
