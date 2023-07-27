from flask import Flask
from extensions import db, api
from resources import ns

''' Library installation:
pip install flask
pip install flask-restx
pip install flask-sqlalchemy
'''

app = Flask(__name__)  # instantiate Flask

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"  # configuring database source of sqlalchemy

api.init_app(app)  # initianting api inside the app
db.init_app(app)  # initianting db inside the app

api.add_namespace(ns)  # registering the namespace defined in resources.py
