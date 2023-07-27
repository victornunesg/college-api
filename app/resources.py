# In this file we will storage the API endpoints

from flask_restx import Resource, Namespace  # Namespace is going to act like a Blueprint in Flask
from models import Course
from api_models import course_model  # brings a JSON response structured for /course endpoint


ns = Namespace("api")  # instantiating NameSpace object, the first argument will be the API URL location


# defining an actual endpoint
@ns.route("/hello")
class Hello(Resource):  # here you can define methods for each HTTP method you wanna support
    def get(self):  # here you need to return something as JSON serializable (like a dictionary)
        return {"hello": "restx"}


@ns.route("/courses")
class CourseAPI(Resource):
    # here is going to take the value returned from get function and it is going to use the model passed in the marshal
    # argument into a list of dictionaries that can be JSON serializable in order to give a correct response
    @ns.marshal_list_with(course_model)  # course_model defined in api_models.py, like a mold
    def get(self):
        return Course.query.all()  # list of tuples that is converted into a JSON by marshal_list_with decorator
