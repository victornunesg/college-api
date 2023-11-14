from app import app, db
from models import Course, Student, User

# this file is used to do test with the database


# =====================================
# creates database according to the models, comment after run it for the first time
# =====================================
#
# with app.app_context():
#     db.create_all()

# =====================================
# clean tables from database
# =====================================

# with app.app_context():
#     db.drop_all()

# =====================================
# creating registers manually into the tables
# =====================================

# with app.app_context():
#     # adding new registers in db session
#     db.session.add_all([Course(name="Math"), Course(name="Science"), Course(name="History")])
#
#     # commiting changes (inserting) data into db
#     db.session.commit()
#
#     # adding students
#     db.session.add_all([
#       Student(name="Victor", course_id=1),
#       Student(name="Lucas", course_id=1),
#       Student(name="Yasmin", course_id=2)
#       ])
#
#     # commiting changes (inserting) data into db
#     db.session.commit()

# =====================================
# checking data inside the tables
# =====================================

with app.app_context():
    courses = Course.query.all()  # getting all information from the table
    students = Student.query.all()
    users = User.query.all(

    )
    print(f'\nList of courses with query.all(): {courses}')
    for course in courses:
        print(course.name)

    print(f'\nList of students with query.all(): {students}')
    for student in students:
        print(student.name)

    print(f'\nList of users with query.all(): {users}')
    for user in users:
        print(str(user.id) + ' | ' + user.username + ' | ' + user.password_hash)
