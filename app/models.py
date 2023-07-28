# file to storge SQLAlchemy models of the database, the table definition
from extensions import db


# creating a table for users, in order to implement token authorization
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))

    courses = db.relationship("Course", back_populates="instructor")


# creating the database 'tables'
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    instructor_id = db.Column(db.ForeignKey("user.id"))  # each user can be an instructor of a course

    students = db.relationship("Student", back_populates="course")
    instructor = db.relationship("User", back_populates="courses")


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    course_id = db.Column(db.ForeignKey("course.id"))
    course = db.relationship("Course", back_populates="students")
