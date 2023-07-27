from flask_restx import fields
from extensions import api

# in this file we are creating models to structure a JSON response according to api's needs

# model to structure the list of courses into a JSON object
# first argument is the model Name, second is the JSON structure
course_model = api.model("Course", {
    "id": fields.Integer,
    "name": fields.String
    # "students":
})
