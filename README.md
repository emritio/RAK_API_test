# RAK_API_testing
**Objective: To run an API that takes in login and registration using RAK device.**

## Requirements
-  Python
-  Html
-  CSS

**libraries:**  
- from flask import Flask, request, render_template, redirect, url_for, jsonify
- from flask_sqlalchemy import SQLAlchemy
- import bcrypt
- from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
- import datetime

## Introduction:
The code  is a Flask application that demonstrates user registration, login, and a basic dashboard functionality with JWT authentication and session management.

Library section:
This section imports the necessary modules and libraries used in the application:

Flask: The Flask web framework for building the application.
Flask-SQLAlchemy: An extension that integrates SQLAlchemy with Flask, used for database operations.
bcrypt: A library for securely hashing passwords.
Flask-JWT-Extended: An extension for JWT (JSON Web Token) authentication.
datetime: Python's built-in module for handling date and time.

## Flask main app:

The Flask app is created and configured with the database URI for PostgreSQL and a JWT secret key. The secret key is used for signing and verifying JWT tokens.
- SQL ALchemy for creating an instance of database in flask
- JWTManager to initialize the tokens using the flask app.

`app = Flask(__name__)`

Creating an user table and required attributes using the "class Users:"
This code defines the structure of the Users table using SQLAlchemy. It uses the db.Model base class to define the table structure. 
The last_login_time field is added to record the timestamp of the user's last login.

### Helper Functions:
```
check_password(username, password)
record_login_time(username)
is_session_expired(last_login_time)

```
### Routes and Views:

- **/** : Displays the index page using the render_template function.
- **/dashboard/<username>**: Displays the dashboard page for a specific user using the render_template function. If the user doesn't exist, they are redirected to the index page.
- **/register** : Handles user registration. If the request method is GET, it renders the registration form. If the request method is POST,
it registers the user and adds their information to the database.
- **/login** : Handles user login. If the request method is GET, it renders the login form. If the request method is POST, it checks the provided credentials,
records the login time, and generates an access token.


### /Register function:

directs the flask app to register.html.
requests data from the html file and stores it in a local variable to be later passed on to the database server through the api.
Before the passwords are stored inside the database it is being hashed  , 1-sided, and then it is stored inside the database.


### /login function:

directs the flask app to index.html
requests the data from the html file and checks the database for user and verifies the credentials to let the user in.
The session starts recording form the moment user logs in and redirects the user to the home page once the tokens expire.

## Conclusion of the application:
Overall, this code provides a basic foundation for a Flask web application with user authentication, registration, and session management using JWT. 
It also interacts with a PostgreSQL database to store user information.


Building a docker image to have all this put in a container.
Create Dockerfile alongside the main flask application mentioning the libraries and working directories.
Create a docker-compose.yml file outside the main directory and provide context in the  "./client"

process to create a container for the application
direct your terminal to the appropriate directory
type "docker build -t <image-name> ."
then type "docker run -t <image-name>" //to check if the application is running.

proceeding to push it into the RAK device using balena cli.
get back to the docker-compose.yml directory
type "balena push <fleet-name>"

application is successfully deployed in your RAK device using Balena.
Concluded.
