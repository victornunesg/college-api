# arquivo para criar e gerenciar os endpoints/rotas
from flask_restx import Resource, Namespace
from models import Course, Student, User
from api_models import course_model, student_model, course_input_model, student_input_model, login_model, user_model # modelos que definem estruturas de resposta aos apontamentos
from extensions import db
from flask_jwt_extended import jwt_required  # importando a função que irá realizar a autenticação a ser implementada nos métodos da API
from flask_jwt_extended import get_jwt_identity  # função que mostra quem está realizando consulta nos endpoins que exigem autenticação
from flask_jwt_extended import create_access_token  # função para gerar o token do usuário
from werkzeug.security import generate_password_hash, check_password_hash  # funções para criptografar/decriptografar senhas de usuário

"""
namespace age como uma blueprint
dentro da namespace você registra os endpoints de sua API
você pode ter quantas namespaces desejar e inserir endpoints para cada uma delas
"""

# dicionário que descreve a natureza das credenciais que podem ser passadas a certo endpoint
authorizations = {
    "jsonWebToken": {  # chave de autenticação
        "type": "apiKey",  # tipo
        "in": "header",  # local onde serão passadas as credenciais
        "name": "Authorization"  # nome da autenticação
    }
}

# criando um objeto Namespace, o primeiro argumento será a url da sua api e também passamos o dicionário contendo o modelo de autenticação
ns = Namespace("Flask Restx API", authorizations=authorizations)

# definindo o primeiro endpoint
@ns.route('/hello')  # decorator definindo o caminho/url
class Hello(Resource):  # classe que herda Resource
    @ns.doc(description="Exemplo de uma REST API, utilizando Flask RestX com autenticação através de JSON Web Token")  # coloca um comentário/descrição no swagger da API
    def get(self):  # função com o nome da operação/método desejado
        return {"Hello": "API RestX Example"}  # retorno em formato de JSON serializável (dict)


# operações envolvendo todos os cursos
@ns.route('/courses')
class CourseListAPI(Resource):
    # atributo de classe que define os decorators para todos os métodos da classe "CourseListAPI"
    method_decorators = [jwt_required()]
    # @jwt_required()  # opção de decorator para sinalizar que a autenticação é necessária para cada método, individualmente

    @ns.doc(security="jsonWebToken")  # informa que a forma de validação é válida para esse endpoint (habilita a autenticação/"cadeado no swagger")
    @ns.marshal_list_with(course_model)  # pega o valor de retorno da query dentro da função get e usará o course_model para converter em uma lista de dicionários (JSON serializável) para disponibilizar oa usuário pela API
    def get(self):
        print(get_jwt_identity())  # imprime o usuário autenticado que está chamando o endpoint
        return Course.query.all()

    # deve-se considerar o tipo de dado que iremos receber para fazer um 'post', para isso, usamos o decorator abaixo
    @ns.expect(course_input_model) # espera dados no formato do course_input_model, pois precisaremos somente do nome do curso
    @ns.marshal_with(course_model)  # usamos o marshal_with por se tratar de apenas 1 item a ser retornado, e não uma lista
    def post(self):
        print(ns.payload)  # payload é a informação de entrada do usuário na API
        course = Course(name=ns.payload["name"])  # coletando o nome do curso advindo do payload
        db.session.add(course)
        db.session.commit()  # adicionando o novo curso no banco de dados
        return course, 201  # 201 é um código HTTP que sinaliza sucesso para inserção de dados


# operações envolvendo um curso específico, a partir do seu id
@ns.route('/courses/<int:id>')  # buscaremos um curso através do parâmetro id, a ser passado na requisição
class CourseAPI(Resource):
    @ns.marshal_with(course_model)
    def get(self, id):  # id da requisição é passado como parâmetro na função get
        course = Course.query.get(id)  # filtraremos diretamente pelo id do curso, através do método get
        return course

    @ns.expect(course_input_model)
    @ns.marshal_with(course_model)
    def put(self, id):
        course = Course.query.get(id)
        course.name = ns.payload["name"]
        db.session.commit()
        return course, 201

    def delete(self, id):
        course = Course.query.get(id)
        db.session.delete(course)
        db.session.commit()
        return None, 204


# operações envolvendo todos os estudantes
@ns.route('/students')
class StudentListAPI(Resource):
    @ns.marshal_list_with(student_model)
    def get(self):
        return Student.query.all()

    @ns.expect(student_input_model)
    @ns.marshal_with(student_model)
    def post(self):
        print(ns.payload)
        student = Student(name=ns.payload["name"], course_id=ns.payload["course_id"])
        db.session.add(student)
        db.session.commit()
        return student, 201


# operações envolvendo um estudante específico, a partir do seu id
@ns.route('/students/<int:id>')
class StudentAPI(Resource):
    @ns.marshal_with(student_model)
    def get(self, id):
        student = Student.query.get(id)
        return student

    @ns.expect(student_input_model)  # necessário receber o nome e o id do curso do estudante, para realizar o update
    @ns.marshal_with(student_model)  # retorna no modelo student_model (id e nome)
    def put(self, id):  # put irá realizar o update
        student = Student.query.get(id)  # busca o estudante
        student.name = ns.payload["name"]  # atualiza o nome com base no payload, relacionado ao student_input_model
        student.course_id = ns.payload["course_id"]  # atualiza o curso
        db.session.commit()
        return student, 200

    def delete(self, id):  # deletando algum estudante
        student = Student.query.get(id)
        db.session.delete(student)
        db.session.commit()
        return None, 204


@ns.route('/register')
class Register(Resource):
    @ns.expect(login_model)  # recebe usuário e senha para cadastro
    @ns.marshal_with(user_model)  # retorna nome e id do usuário criado
    def post(self):
        # a senha é criptografada antes de ser inserida no banco de dados
        user = User(username=ns.payload["username"], password_hash=generate_password_hash(ns.payload["password"]))
        db.session.add(user)
        db.session.commit()
        return user, 201


@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        user = User.query.filter_by(username=ns.payload["username"]).first()  # busca o usuário pelo nome no BD
        if not user:
            return {"error": "User does not exists"}, 401
        if not check_password_hash(user.password_hash, ns.payload["password"]): # verifica se a senha está batendo
            return {"error": "Incorrect password"}, 401
        return {"access token": create_access_token(user.username)}  # gerando token através da função e o nome do usuário