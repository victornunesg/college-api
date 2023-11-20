# arquivo para criar e gerenciar os endpoints/rotas
from flask_restx import Resource, Namespace
from models import Course, Student
from api_models import course_model, student_model, course_input_model, student_input_model # modelos que definem estruturas de resposta aos apontamentos
from extensions import db

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


# operações envolvendo todos os cursos
@ns.route('/courses')
class CourseListAPI(Resource):
    @ns.marshal_list_with(course_model)  # pega o valor de retorno da query dentro da função get e usará o course_model para converter em uma lista de dicionários (JSON serializável) para disponibilizar oa usuário pela API
    def get(self):
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
