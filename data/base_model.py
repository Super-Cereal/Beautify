import sqlalchemy as sql
from .db_session import SqlAlchemyBase


class BaseModel(SqlAlchemyBase):
    __abstract__ = True
    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
