import sqlalchemy as sql

from .base_model import BaseModel

texts_to_collections = sql.Table(
    "texts_to_collections",
    BaseModel.metadata,
    sql.Column("texts", sql.Integer, sql.ForeignKey("texts.id")),
    sql.Column("collections", sql.Integer, sql.ForeignKey("collections.id")),
)


class Text(BaseModel):
    __tablename__ = "texts"

    name = sql.Column(sql.String)
    address = sql.Column(sql.String)
    user_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    # collections by texts_to_collections
