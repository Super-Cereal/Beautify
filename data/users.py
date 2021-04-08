import sqlalchemy as sql
from sqlalchemy_serializer import SerializerMixin

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .base_model import BaseModel


class User(BaseModel, UserMixin, SerializerMixin):
    __tablename__ = "users"

    nickname = sql.Column(sql.String)
    email = sql.Column(sql.String, index=True, unique=True)
    hashed_password = sql.Column(sql.String)
    # collection = sql.orm.relation("Collection", back_populates="user")

    @property
    def password(self):
        return None

    @password.setter
    def password(self, password):
        self.set_password(password)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.hashed_password, value)

    def generate_auth_token(self, expiration=3000):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})
