from data import db_session
from data.users import User

from flask import Flask, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources import resources_user


app = Flask(__name__, template_folder=".")
app.config.from_object('config')
api = Api(app)
api.add_resource(resources_user.Auth, "/api/v1.0/auth")
api.add_resource(resources_user.UserResource, "/api/v1.0/users/<int:user_id>")
api.add_resource(resources_user.UserListResource, "/api/v1.0/users")

db_session.global_init("./data/db/main_db.sqlite")


jwt = JWTManager(app)
jwt.unauthorized_loader(
    lambda msg: {"resultCode": 1, "message": msg, "data": {"id": None}})


@app.errorhandler(404)
def error404(error):
    return {"resultCode": 1, "data": {"message": "Not found"}}


@app.route('/api/v1.0/docs')
def docs():
    return render_template("./docs.html")
