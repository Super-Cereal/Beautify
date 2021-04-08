from flask_login import login_user, logout_user, current_user
from flask_restful import Resource

from data.db_session import create_session
from data.users import User

from .parsers.parsers_user import parserRegisterUser, parserLoginUser


class Auth(Resource):
    def get(self):
        if current_user.is_authenticated:
            return {
                "resultCode": 0,
                "data": {
                    "id": current_user.id,
                    "email": current_user.email,
                },
            }
        else:
            return {"resultCode": 1, "data": {"id": None, "email": None}}

    def post(self):
        args = parserLoginUser.parse_args()
        session = create_session()
        user = session.query(User).filter(User.email == args["email"]).first()
        if user and user.check_password(args["password"]):
            login_user(user, remember=args["remember_me"])
            return {"resultCode": 0, "data": {"userId": user.id}}
        else:
            return {"resultCode": 1, "data": {"userId": None}}

    def delete(self):
        if current_user.is_authenticated:
            logout_user()
            return {"resultCode": 0}
        return {"resultCode": 1}


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
        )
        user.set_password(args["password"])
        session.add(user)
        session.commit()
        return {"resultCode": 0}
