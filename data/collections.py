import sqlalchemy as sql

from .base_model import BaseModel


class Collection(BaseModel):
    __tablename__ = "collections"

    texts = sql.orm.relation(
        "Collection", secondary="texts_to_collections", backref="collections"
    )
    user = sql.orm.relation("User")
