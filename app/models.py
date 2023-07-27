# file to storge SQLAlchemy models of the database, the table definition
from extensions import db


# creating the database 'tables'
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    students = db.relationship("Student", back_populates="course")


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    course_id = db.Column(db.ForeignKey("course.id"))
    course = db.relationship("Course", back_populates="students")
