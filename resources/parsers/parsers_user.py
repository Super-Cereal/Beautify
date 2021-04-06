from flask_restful import reqparse


parserRegisterUser = reqparse.RequestParser()
parserRegisterUser.add_argument("nickname", required=True)
parserRegisterUser.add_argument("email", required=True)
parserRegisterUser.add_argument("password", required=True)

parserLoginUser = reqparse.RequestParser()
parserLoginUser.add_argument("email", required=True)
parserLoginUser.add_argument("password", required=True)
parserLoginUser.add_argument("remember_me", default=False)