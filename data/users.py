import sqlalchemy as sql
from sqlalchemy_serializer import SerializerMixin

from flask_jwt_extended import create_access_token
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash

from .base_model import BaseModel


class User(BaseModel, SerializerMixin):
    __tablename__ = "users"

    nickname = sql.Column(sql.String)
    email = sql.Column(sql.String, index=True, unique=True)
    hashed_password = sql.Column(sql.String)
    # collection = sql.orm.relation("Collection", back_populates="user")

    def __init__(self, **kwargs):
        self.nickname = kwargs.get("nickname")
        self.email = kwargs.get("email")
        self.hashed_password = generate_password_hash(kwargs.get("password"))

    def get_token(self, expire_time=24):
        expires_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expires_delta
        )
        return token

    def check_password(self, value):
        return check_password_hash(self.hashed_password, value)
