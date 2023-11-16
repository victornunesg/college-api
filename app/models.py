from .extensions import db  # importando o banco de dados


# definindo as tabelas/modelos do banco de dados
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    # students


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    course_id = db.Column(db.ForeignKey("course.id"))

