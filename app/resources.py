# in this file we will define the API endpoints

from flask_restx import Resource, Namespace  # namespace is going to act like a Blueprint in Flask
# importing this function to enable token in the endpoints
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, current_user
from werkzeug.security import generate_password_hash, check_password_hash  # to register and login users
from models import Course, Student, User
from app import db

# brings a JSON response structured to be used in the endpoints
from api_models import course_model, student_model, course_input_model, student_input_model, login_model, user_model

# this dictionary is used to define the structure and to describe the nature of the credentials that can be passed to a
# particular endpoint, in order to pass the authorization using the swagger
authorizations = {
    "jsonWebToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"  # name of the header key
    }
}

# instantiating NameSpace object, the first argument will be the API URL location, the second one is the authorization
ns = Namespace("college-api", authorizations=authorizations)


# defining an actual endpoint
@ns.route("/hello")
class Hello(Resource):  # inside the class you can define methods for each HTTP method you want to support
    def get(self):  # here you need to return something as JSON serializable (like a dictionary)
        return {"hello": "restx"}


@ns.route("/users")
class UserList(Resource):
    method_decorators = [jwt_required()]

    @ns.doc(security="jsonWebToken")
    @ns.marshal_list_with(user_model)
    def get(self):
        return User.query.all()

@ns.route("/courses")
class CourseListAPI(Resource):
    # since it is not possible to put jwt as a decorator, we use method_decorators attribute from Resource class
    # to call jwt informing that for this endpoint a token authorization is required to run in any method for this class
    method_decorators = [jwt_required()]

    # informing the authorization is valid to this endpoint
    @ns.doc(security="jsonWebToken")
    # marshal_list_with will take the value returned from get function and will use the model passed in the marshal
    # argument into a list of dictionaries that can be JSON serializable in order to give an expected response
    @ns.marshal_list_with(course_model)  # course_model defined in api_models.py, like a mold to return a response
    def get(self):
        print(get_jwt_identity())  # getting the ID from token (user logged in)
        print(current_user)  # getting the user as an object
        return Course.query.all()
        # return Course.query.filter_by(instructor=current_user).all()  # getting only the courses related to the user
        # this is a list of tuples that is converted into a JSON by marshal_list_with decorator

    @ns.doc(security="jsonWebToken")
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


@ns.route("/register")
class Register(Resource):
    @ns.expect(login_model)
    @ns.marshal_with(user_model)
    def post(self):
        # creating a new user
        user = User(username=ns.payload["username"], password_hash=generate_password_hash(ns.payload["password"]))
        db.session.add(user)
        db.session.commit()
        return user, 201

@ns.route("/login")
class Login(Resource):

    @ns.expect(login_model)
    def post(self):
        user = User.query.filter_by(username=ns.payload["username"]).first()
        if not user:
            return {"error": "User does not exist"}, 401
        if not check_password_hash(user.password_hash, ns.payload["password"]):
            return {"error": "Incorrect password"}, 401
        return {"access_token": create_access_token(user)}
