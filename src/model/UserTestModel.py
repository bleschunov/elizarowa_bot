from sqlalchemy import Table, Column, Integer, ForeignKey, String

from db import Base

user_role_association = Table(
    "user_role_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("test_id", Integer, ForeignKey("test.id")),
    Column("total_score", Integer),
    Column("result_description", String)
)
