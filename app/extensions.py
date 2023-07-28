from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_jwt_extended import JWTManager  # importing the main class of this library in order to implement token

# instantiating database and flaskrestx objects
db = SQLAlchemy()
api = Api()
jwt = JWTManager()
