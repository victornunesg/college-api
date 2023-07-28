# In this file we will define the API endpoints

from flask_restx import Resource, Namespace  # Namespace is going to act like a Blueprint in Flask
from flask_jwt_extended import jwt_required  # importing this function to enable token in the endpoints
from models import Course, Student
from app import db

# brings a JSON response structured to be used in the endpoints
from api_models import course_model, student_model, course_input_model, student_input_model

# block to describe the nature of the credentials that can be passed to a particular endpoint
# we will use a dictionary to define the structure, in order to pass the authorizarion using the swagger

authorizations = {
    "jsonWebToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

ns = Namespace("college-api", authorizations=authorizations)  # instantiating NameSpace object, the first argument will be the API URL location


# defining an actual endpoint
@ns.route("/hello")
class Hello(Resource):  # inside the class you can define methods for each HTTP method you want to support
    def get(self):  # here you need to return something as JSON serializable (like a dictionary)
        return {"hello": "restx"}


@ns.route("/courses")
class CourseListAPI(Resource):
    # since it is not possible to put jwt as a decorator, we use method_decorators attribute from Resource class
    # to call jwt informing that for this endpoint a token authorization is required
    method_decorators = [jwt_required()]

    @ns.doc(security="jsonWebToken")  # informing the authorization is valid to this endpoint
    # marshal_list_with will take the value returned from get function and will use the model passed in the marshal
    # argument into a list of dictionaries that can be JSON serializable in order to give an expected response
    @ns.marshal_list_with(course_model)  # course_model defined in api_models.py, like a mold to return a response
    def get(self):
        return Course.query.all()  # list of tuples that is converted into a JSON by marshal_list_with decorator

    @ns.expect(course_input_model)  # expected type of data
    @ns.marshal_with(course_model)  # response structure, using marshal_with since will return only one object
    def post(self):
        print(ns.payload)  # gets the input information from post method
        course = Course(name=ns.payload["name"])  # creating a new Course object with the payload information
        db.session.add(course)  # adding to the db
        db.session.commit()  # commiting changes
        return course, 201  # 201 is the HTTP status code for 'created success'


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
        return course, 200  # 200 is the HTTP status code for 'success'

    def delete(self, id):
        course = Course.query.get(id)
        db.session.delete(course)
        db.session.commit()
        return {}, 204  # 204 is the HTTP status code for 'no content'


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
