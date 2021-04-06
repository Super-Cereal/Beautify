import sqlalchemy as sql
from sqlalchemy_serializer import SerializerMixin

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .base_model import BaseModel


class User(BaseModel, UserMixin, SerializerMixin):
    __tablename__ = "users"

    nickname = sql.Column(sql.String)
    email = sql.Column(sql.String, index=True, unique=True)
    hashed_password = sql.Column(sql.String)
    # collection = sql.orm.relation("Collection", back_populates="user")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
