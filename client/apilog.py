from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
#from config import SQLALCHEMY_DATABASE_URI
import psycopg2
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime
import bcrypt
import api_keys #Python file that contains all the keys


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  api_keys.db_key
app.config['JWT_SECRET_KEY'] =   api_keys.jwt_key# Change this to a strong secret key

db = SQLAlchemy(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

class Users(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(120), nullable=False)
    last_login_time = db.Column(db.DateTime)


def check_password(username, password):
    user = Users.query.filter_by(username=username).first()
    if user:
        return user.password == password.encode('utf-8')
    return False

def record_login_time(username):
    user = Users.query.filter_by(username=username).first()
    if user:
        user.last_login_time = datetime.datetime.now()
        db.session.commit()

# Check if the session has expired
def is_session_expired(last_login_time):
    current_time = datetime.datetime.now()
    return (current_time - last_login_time).total_seconds() > 120


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard/<username>', methods=['GET'])
def dashboard(username):
    user = Users.query.filter_by(username=username).first()
    if user:
        return render_template('dashboard.html', username=username)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    elif request.method == 'POST':
        #print('going inside post')
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
        else:
            raise ValueError('Username not found in request')

        if Users.query.filter_by(username=username).first():
            #print("It also takes the query")
            return jsonify({'error': 'Username already taken'}), 400
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create a new User instance and save it to the database
        new_user = Users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('index'))


@app.route('/login', methods=['GET','POST'])
def login():
    # print("got inside login")
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        # print("got inside post")
        username = request.form['username']
        # print("No error with request: ",username)
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # Record the login time
            record_login_time(username)

            access_token = create_access_token(identity=username)
            return jsonify({'access_token': access_token}), 200,redirect(url_for('dashboard',usrename=username))
    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True,port=8000)