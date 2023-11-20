# arquivo para criar e gerenciar extensões do flask restx e sqlalchemy
from flask_sqlalchemy import SQLAlchemy  # conexão com o banco de dados
from flask_restx import Api  # criação da API
from flask_jwt_extended import JWTManager  # implementação da autenticação via JSON web token

# instanciando as classes, criando objetos das extensões
api = Api()
db = SQLAlchemy()
jwt = JWTManager()
