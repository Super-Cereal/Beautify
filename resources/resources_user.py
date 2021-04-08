from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from data.db_session import create_session
from data.users import User

from .parsers.parsers_user import parserRegisterUser, parserLoginUser


class Auth(Resource):
    @jwt_required()
    def get(self):
        userId = get_jwt_identity()
        return {"resultCode": 0, "data": {"id": userId}}

    def post(self):
        args = parserLoginUser.parse_args()
        session = create_session()
        user = session.query(User).filter(User.email == args["email"]).first()
        if user and user.check_password(args["password"]):
            token = user.get_token()
            return {"resultCode": 0, "data": {"id": user.id, "access_token": f"{token}"}}
        else:
            return {"resultCode": 1,
                    "message": "wrong email or password",
                    "data": {"id": None, "access_token": None}}

    # @jwt_required()
    # def delete(self):
    #     return {"resultCode": 0}


class UserResource(Resource):
    def get(self, user_id):
        session = create_session()
        user = session.query(User).get(user_id)
        if user:
            return {
                "resultCode": 0,
                "user": user.to_dict(only=["id", "nickname", "email"]),
            }
        else:
            return {"resultCode": 1, "user": None}

    def delete(self, user_id):
        session = create_session()
        user = session.query(User).get(user_id)
        if user:
            session.delete(user)
            session.commit()
            return {"resultCode": 0}
        else:
            return {"resultCode": 1}


class UserListResource(Resource):
    def get(self):
        session = create_session()
        users = session.query(User).all()
        return {
            "users": [user.to_dict(only=["id", "nickname", "email"]) for user in users]
        }

    def post(self):
        args = parserRegisterUser.parse_args()
        session = create_session()
        if session.query(User.email).filter(User.email == args["email"]).first():
            return {"resultCode": 1, "message": "Email is already exists"}
        user = User(
            nickname=args["nickname"],
            email=args["email"],
            password=args["password"]
        )
        session.add(user)
        session.commit()
        token = user.get_token()
        return {"resultCode": 0, "data": {"access_token": f"{token}"}}
