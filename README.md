# College API

---

In this project an API was developed using Flask RestX library (a web application framework written in Python). The objective was: elaborate from scratch a RESTful API to be used at any educational institution.

You can do requests do get data related to the registered courses, students and also users allowed to perform the requests that demand authorization token.

It is also possible to insert, update and delete data from the database using POST, PUT and DELETE requests. 

The SQLite database connection was made using SQLAlchemy library.

## Funcionalities

---

- Login and registration
- GET/PUT/POST/DELETE requisitions
- JSON Web Token authorization to specific endpoints
- SQLite database integrated

The development was done using mainly:

- Python (back-end)

Main Pyhton libraries used:

- Flask RestX
- Flask SQLAlchemy
- Flask JWT Extended
- Werkzeug Security

## Project Structure

---

```shell
college-api/
├── app
│   ├── __init__.py
│   ├── api_models.py
│   ├── extensions.py
│   ├── main.py
│   ├── models.py
│   ├── resources.py
├── images
│   ├── ...
├── instance
    ├── db.sqlite3
```


## Screenshots

---
![home.png](images%2Fhome.png)

![login1.png](images%2Flogin1.png)

![login2.png](images%2Flogin2.png)

![request.png](images%2Frequest.png)