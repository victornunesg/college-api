# arquivo onde definimos as tabelas/modelos do banco de dados
from extensions import db  # importando o banco de dados


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    # relação com a classe Student para relacionar os estudantes participantes do curso
    students = db.relationship("Student", back_populates="course")


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    # cada estudante pode fazer parte apenas de 1 curso:
    course_id = db.Column(db.ForeignKey("course.id"))  # chave estrangeira para vincular ao curso do estudante

    course = db.relationship("Course", back_populates="students")
