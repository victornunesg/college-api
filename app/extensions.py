# arquivo para criar e gerenciar extensões do flask restx e sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

# instanciando as classes, criando objetos das extensões
api = Api()
db = SQLAlchemy()