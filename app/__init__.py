from flask import Flask  # importando a classe Flask
from extensions import api, db  # importando os objetos criados em extensions
from routes import ns  # importando o namespace que registra as rotas da API

app = Flask(__name__)  # criando objeto Flask

# passando configurações para o app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"  # banco de dados será criado em uma pasta 'instance' na raiz do projeto

# iniciando api e db dentro do app
api.init_app(app)
db.init_app(app)

# registrando o namespace na api
api.add_namespace(ns)


