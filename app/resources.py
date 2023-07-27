# In this file we will storage the API endpoints

from flask_restx import Resource, Namespace  # Namespace is going to act like a Blueprint in Flask
from models import Course, Student
from app import db

# brings a JSON response structured for /course endpoint
from api_models import course_model, student_model, course_input_model, student_input_model


ns = Namespace("api")  # instantiating NameSpace object, the first argument will be the API URL location


# defining an actual endpoint
@ns.route("/hello")
class Hello(Resource):  # here you can define methods for each HTTP method you wanna support
    def get(self):  # here you need to return something as JSON serializable (like a dictionary)
        return {"hello": "restx"}


@ns.route("/courses")
class CourseListAPI(Resource):
    # here is going to take the value returned from get function and it is going to use the model passed in the marshal
    # argument into a list of dictionaries that can be JSON serializable in order to give a correct response
    @ns.marshal_list_with(course_model)  # course_model defined in api_models.py, like a mold
    def get(self):
        return Course.query.all()  # list of tuples that is converted into a JSON by marshal_list_with decorator

    @ns.expect(course_input_model)  # type of data i'm going to be receiving
    @ns.marshal_with(course_model)
    def post(self):
        print(ns.payload)  # gets the input information
        course = Course(name=ns.payload["name"])  # creating a new Course object with the payload information
        db.session.add(course)
        db.session.commit()
        return course, 201  # 201 is the status code for success


@ns.route("/courses/<int:id>")
class CourseAPI(Resource):
    @ns.marshal_with(course_model)
    def get(self, id):
        course = Course.query.get(id)
        return course

    @ns.expect(course_input_model)
    @ns.marshal_with(course_model)
    def put(self, id):
        course = Course.query.get(id)
        course.name = ns.payload["name"]
        db.session.commit()
        return course, 200

    def delete(self, id):
        course = Course.query.get(id)
        db.session.delete(course)
        db.session.commit()
        return {}, 204


@ns.route("/students")
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


@ns.route("/students/<int:id>")
class StudentAPI(Resource):
    @ns.marshal_with(student_model)
    def get(self, id):
        student = Student.query.get(id)
        return student

    @ns.expect(student_input_model)
    @ns.marshal_with(student_model)
    def put(self, id):
        student = Student.query.get(id)
        student.name = ns.payload["name"]
        student.course_id = ns.payload["course_id"]
        db.session.commit()
        return student, 200

    def delete(self, id):
        student = Student.query.get(id)
        db.session.delete(student)
        db.session.commit()
        return {}, 204
