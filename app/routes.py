# arquivo para criar e gerenciar os endpoints/rotas
from flask_restx import Resource, Namespace
from models import Course, Student, User
from api_models import course_model, student_model, course_input_model, student_input_model, login_model, user_model # modelos que definem estruturas de resposta aos apontamentos
from extensions import db
from flask_jwt_extended import jwt_required  # importando a função que irá realizar a autenticação a ser implementada nos métodos da API
from flask_jwt_extended import get_jwt_identity  # função que mostra quem está realizando consulta nos endpoins que exigem autenticação
from flask_jwt_extended import create_access_token  # função para gerar o token do usuário
from werkzeug.security import generate_password_hash, check_password_hash  # funções para criptografar/decriptografar senhas de usuário


# dicionário que descreve a natureza das credenciais que podem ser passadas a certo endpoint
authorizations = {
    "jsonWebToken": {  # chave de autenticação
        "type": "apiKey",  # tipo de chave
        "in": "header",  # local onde serão passadas as credenciais
        "name": "Authorization"  # nome da autenticação
    }
}

# criando os objetos Namespace
# o primeiro argumento será a url da sua api, também passamos o dicionário contendo o modelo de autenticação nos casos aplicáveis
ns_hello = Namespace("Rest API - Flask RESTX")
ns_login = Namespace("Login-Register")
ns_public = Namespace("Courses-Students")
ns_private = Namespace("Logged-Area", authorizations=authorizations)


# =====================================
# ENDPOINTS NAMESPACE REST API - FLASK RESTX
# =====================================


# definindo o primeiro endpoint
@ns_hello.route('/hello')  # decorator definindo o caminho/url
class Hello(Resource):  # classe que herda Resource
    @ns_hello.doc(description="Exemplo de uma REST API, utilizando Flask RestX com autenticação através de JSON Web Token")  # coloca um comentário/descrição no swagger da API
    def get(self):  # função com o nome da operação/método desejado
        return {"Hello": "API RestX Example"}  # retorno em formato de JSON serializável (dict)


# =====================================
# ENDPOINTS NAMESPACE LOGIN-REGISTER
# =====================================


@ns_login.route('/register')
class Register(Resource):
    @ns_login.expect(login_model)  # deve-se considerar o tipo de dado que iremos receber para fazer um 'post', para isso, usamos o decorator 'expect'. Espera dados no formato do course_input_model, pois precisaremos somente do nome do curso
    @ns_login.marshal_with(user_model)  # retorna nome e id do usuário criado. usamos o marshal_with por se tratar de apenas 1 item a ser retornado, e não uma lista
    def post(self):
        # a senha é criptografada antes de ser inserida no banco de dados
        user = User(username=ns_login.payload["username"], password_hash=generate_password_hash(ns_login.payload["password"]))
        # payload é a informação de entrada do usuário na API
        db.session.add(user)
        db.session.commit()
        return user, 201


@ns_login.route('/login')
class Login(Resource):
    @ns_login.expect(login_model)
    def post(self):
        user = User.query.filter_by(username=ns_login.payload["username"]).first()  # busca o usuário pelo nome no BD
        if not user:
            return {"error": "User does not exists"}, 401
        if not check_password_hash(user.password_hash, ns_login.payload["password"]): # verifica se a senha está batendo
            return {"error": "Incorrect password"}, 401
        return {"access token": create_access_token(user.username)}  # gerando token através da função e o nome do usuário


# =====================================
# ENDPOINTS NAMESPACE COURSES-STUDENTS
# =====================================


# visão geral de todos os cursos
@ns_public.route('/courses')
class GetCourses(Resource):

    @ns_public.marshal_list_with(course_model)  # pega o valor de retorno da query dentro da função get e usará o course_model para converter em uma lista de dicionários (JSON serializável) para disponibilizar oa usuário pela API
    def get(self):
        return Course.query.all()


# busca de curso pelo ID
@ns_public.route('/courses/<int:id>')  # buscaremos um curso através do parâmetro id, a ser passado na requisição
class GetCourseID(Resource):

    @ns_public.marshal_with(course_model)
    def get(self, id):  # id da requisição é passado como parâmetro na função get
        course = Course.query.get(id)  # filtraremos diretamente pelo id do curso, através do método get
        return course


# visão geral de todos os estudantes
@ns_public.route('/students')
class GetStudents(Resource):

    @ns_public.marshal_list_with(student_model)
    def get(self):
        return Student.query.all()


# busca de estudante pelo ID
@ns_public.route('/students/<int:id>')
class GetStudentID(Resource):

    @ns_public.marshal_with(student_model)
    def get(self, id):
        student = Student.query.get(id)
        return student, 201


# =====================================
# ENDPOINTS NAMESPACE LOGGED-AREA
# =====================================


# adicionar algum curso
@ns_private.route('/courses')
class AddCourses(Resource):

    # print(get_jwt_identity())  # imprime o usuário autenticado que está chamando o endpoint
    @jwt_required()  # opção de decorator para sinalizar que a autenticação é necessária para cada método, individualmente
    @ns_private.doc(security="jsonWebToken")  # informa que a forma de validação é válida para esse endpoint (habilita a autenticação/"cadeado no swagger")
    @ns_private.expect(course_input_model)
    @ns_private.marshal_with(course_model)
    def post(self):
        print(ns_public.payload)
        course = Course(name=ns_public.payload["name"])  # coletando o nome do curso advindo do payload
        db.session.add(course)  # adicionando o novo curso no banco de dados
        db.session.commit()  # commitando a alteração na sessão do banco de dados
        return course, 201  # 201 é um código HTTP que sinaliza sucesso para inserção de dados


# operações envolvendo um curso específico, a partir do seu id
@ns_private.route('/courses/<int:id>')  # buscaremos um curso através do parâmetro id, a ser passado na requisição
class EditCourses(Resource):

    method_decorators = [jwt_required()]  # atributo de classe que define os decorators para todos os métodos da classe "CourseListAPI"

    @ns_private.expect(course_input_model)
    @ns_private.marshal_with(course_model)
    @ns_private.doc(security="jsonWebToken")
    def put(self, id):
        course = Course.query.get(id)
        course.name = ns_private.payload["name"]
        db.session.commit()
        return course, 201

    @ns_private.doc(security="jsonWebToken")
    def delete(self, id):
        course = Course.query.get(id)
        db.session.delete(course)
        db.session.commit()
        return None, 204


# adicionar algum estudante
@ns_private.route('/students')
class AddStudents(Resource):

    @jwt_required()
    @ns_private.doc(security="jsonWebToken")
    @ns_private.expect(student_input_model)
    @ns_private.marshal_with(student_model)
    def post(self):
        print(ns_private.payload)
        student = Student(name=ns_private.payload["name"], course_id=ns_private.payload["course_id"])
        db.session.add(student)
        db.session.commit()
        return student, 201


# operações envolvendo um estudante específico, a partir do seu id
@ns_private.route('/students/<int:id>')
class EditStudents(Resource):

    method_decorators = [jwt_required()]  # atributo de classe que define os decorators para todos os métodos da classe "CourseListAPI"

    @ns_private.expect(student_input_model)  # necessário receber o nome e o id do curso do estudante, para realizar o update
    @ns_private.marshal_with(student_model)  # retorna no modelo student_model (id e nome)
    @ns_private.doc(security="jsonWebToken")
    def put(self, id):  # put irá realizar o update
        student = Student.query.get(id)  # busca o estudante
        student.name = ns_private.payload["name"]  # atualiza o nome com base no payload, relacionado ao student_input_model
        student.course_id = ns_private.payload["course_id"]  # atualiza o curso
        db.session.commit()
        return student, 200

    @ns_private.doc(security="jsonWebToken")
    def delete(self, id):  # deletando algum estudante
        student = Student.query.get(id)
        db.session.delete(student)
        db.session.commit()
        return None, 204
