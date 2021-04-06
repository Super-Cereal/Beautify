from data import db_session
from data.users import User

from flask import Flask, render_template
from flask_login import LoginManager, current_user
from flask_restful import Api

from resources import resources_user


app = Flask(__name__, template_folder=".")
app.config.from_object('config')
api = Api(app)
api.add_resource(resources_user.Auth, "/api/v1.0/auth")
api.add_resource(resources_user.UserResource, "/api/v1.0/users/<int:user_id>")
api.add_resource(resources_user.UserListResource, "/api/v1.0/users")

log_manager = LoginManager()
log_manager.init_app(app)

db_session.global_init("./data/db/main_db.sqlite")


@app.errorhandler(404)
def error404(error):
    return {"error": "Not found"}


@log_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/api/v1.0/docs')
def docs():
    return render_template("./docs.html")

@app.route("/api/v1.0/debug")
def debug():
    return f"**{current_user.id}**"