# arquivo para criar e gerenciar os endpoints/rotas
from flask_restx import Resource, Namespace

"""
namespace age como uma blueprint
dentro da namespace você registra os endpoints de sua API
você pode ter quantas namespaces desejar
"""

# criando um objeto Namespace, o primeiro argumento será a url da sua api
ns = Namespace("api")


# definindo o primeiro endpoint
@ns.route('/hello')  # decorator definindo o caminho/url
class Hello(Resource):  # classe que herda Resource
    def get(self):  # função com o nome da operação/método desejado
        return {"hello": "restx"}  # retorno em formato de JSON serializável (dict)