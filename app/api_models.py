from flask_restx import fields
from extensions import api

# in this file we are creating models to structure a JSON response according to api's needs

# model to structure the list of students into a JSON object
# first argument is the model Name, second is the JSON structure
student_model = api.model("Student", {
    "id": fields.Integer,
    "name": fields.String,
    # "course": fields.Nested(course_model)  # can't put both together in order to avoid a loop of circular reference
})

student_input_model = api.model("StudentInput", {
    "name": fields.String,
    "course_id": fields.Integer,
})

course_model = api.model("Course", {
    "id": fields.Integer,
    "name": fields.String,
    "students": fields.Nested(student_model),
})

course_input_model = api.model("CourseInput", {
    "name": fields.String,
})


