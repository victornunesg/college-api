from flask import Flask  # importando a classe Flask
from extensions import api, db, jwt  # importando os objetos criados em extensions
from routes import ns_login, ns_hello, ns_public, ns_private  # importando o namespace que registra as rotas da API

app = Flask(__name__)  # criando objeto Flask

# passando configurações para o app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"  # banco de dados será criado em uma pasta 'instance' na raiz do projeto
app.config["JWT_SECRET_KEY"] = "SecretKeyExample"

# iniciando api e db dentro do app
api.init_app(app)
db.init_app(app)
jwt.init_app(app)

# registrando os namespaces na api definidas em 'routes'
api.add_namespace(ns_hello)
api.add_namespace(ns_login)
api.add_namespace(ns_public)
api.add_namespace(ns_private)
