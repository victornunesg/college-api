from flask import Flask
from extensions import db, api, jwt
from resources import ns
from models import User

''' Library installation:
pip install flask
pip install flask-restx
pip install flask-sqlalchemy
'''

app = Flask(__name__)  # instantiate Flask

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"  # configuring database source of sqlalchemy
app.config["JWT_SECRET_KEY"] = "thisisasecret"

api.init_app(app)  # initianting api inside the app
db.init_app(app)  # initianting db inside the app
jwt.init_app(app)  # initiating jwt inside app (token module)

api.add_namespace(ns)  # registering the namespace defined in resources.py


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id  # returns something unique about the user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):  # the first argument has a '_' before because it will not be used
    identity = jwt_data["sub"]  # identity is who the user is
    return User.query.filter_by(id=identity).first()
