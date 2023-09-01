from flask import Flask, request, render_template, redirect, url_for, jsonify # Main flask framework
from flask_sqlalchemy import SQLAlchemy  # Database setup
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity  # Web token setup
import datetime # record time for login session
import bcrypt # Hashing Password
import api_keys #Python file that contains all the keys

#Starts Flask
app = Flask(__name__)
#Importing database functions from flask
app.config['SQLALCHEMY_DATABASE_URI'] =  api_keys.db_key
#Setting up tokens
app.config['JWT_SECRET_KEY'] =   api_keys.jwt_key

#Base Version 0-python.0-html.0-CSS (denotes changes from the base version)
app.config['VERSION'] = '0.0.0'

db = SQLAlchemy(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

#The user table is created with required attributes
class Users(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(120), nullable=False)
    last_login_time = db.Column(db.DateTime)

#Function to verify credentials
def check_password(username, password):
    user = Users.query.filter_by(username=username).first()
    if user:
        return user.password == password.encode('utf-8')
    return False

#Function to keep track of login time for session time-out
def record_login_time(username):
    user = Users.query.filter_by(username=username).first()
    if user:
        user.last_login_time = datetime.datetime.now()
        db.session.commit()

# Check if the session has expired
def is_session_expired(last_login_time):
    current_time = datetime.datetime.now()
    return (current_time - last_login_time).total_seconds() > 120

#The main page routes to index.html
@app.route('/')
def index():
    return render_template('index.html')

#The function routes to the registration page for user info
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    elif request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
        else:
            raise ValueError('Username not found in request')

        if Users.query.filter_by(username=username).first():

            return jsonify({'error': 'Username already taken'}), 400
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create a new User instance and save it to the database
        new_user = Users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('index'))

#Login page to check credentials
@app.route('/login', methods=['GET','POST'])
def login():
    
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # Record the login time
            record_login_time(username)

            access_token = create_access_token(identity=username)
            return jsonify({'access_token': access_token}), 200,redirect(url_for('dashboard',usrename=username))
    return jsonify({'error': 'Invalid credentials'}), 401

#Dashboard opens the home page
@app.route('/dashboard/<username>', methods=['GET'])
def dashboard(username):
    user = Users.query.filter_by(username=username).first()
    if user:
        return render_template('dashboard.html', username=username)
    return redirect(url_for('index'))

#Main function starts the server on port 8001
if __name__ == '__main__':
    app.run(debug=True,port=8001)