# arquivo onde definimos as tabelas/modelos do banco de dados
from extensions import db  # importando o banco de dados


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))

    # relação com a classe Course para relacionar os cursos onde o usuário é instrutor
    courses = db.relationship("Course", back_populates="instructor")


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    instructor_id = db.Column(db.ForeignKey("user.id"))  # cada usuário pode ser o instrutor de um curso

    # relação com a classe Student para relacionar os estudantes participantes do curso
    students = db.relationship("Student", back_populates="course")
    # relação com a classe User para relacionar os instrutores do curso
    instructor = db.relationship("User", back_populates="courses")


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    # cada estudante pode fazer parte apenas de 1 curso:
    course_id = db.Column(db.ForeignKey("course.id"))  # chave estrangeira para vincular ao curso do estudante

    course = db.relationship("Course", back_populates="students")
