# arquivo para transformar respostas das queries ao banco em JSON serializável para retorno da API
from flask_restx import fields
from extensions import api

# queremos criar modelos que representarão qual será a estrutura de resposta dos apontamentos

student_model = api.model("Student", {
    "id": fields.Integer,
    "name": fields.String,
    # "course": fields.Nested(course_model)  # traz no modelo course_model as informações do curso ao qual o estudante pertence
})

student_input_model = api.model("StudentInput", {
    "name": fields.String,
    "course_id": fields.Integer
})

course_model = api.model("Course", {
    "id": fields.Integer,
    "name": fields.String,
    "students": fields.Nested(student_model)  # traz no modelo student_model as informações dos alunos pertencentes ao curso
})

course_input_model = api.model("CourseInput", {
    "name": fields.String,
    "course_id": fields.Integer
})