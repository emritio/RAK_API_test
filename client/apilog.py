from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
#from config import SQLALCHEMY_DATABASE_URI
import psycopg2


def check_password(username, password):
    user = Users.query.filter_by(username=username).first()
    if user:
        return user.password == password
    return False

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@172.17.0.1:5432/postgres'
db = SQLAlchemy(app)

class Users(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(120), nullable=False)

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
        
        # Create a new User instance and save it to the database
        new_user = Users(username=username, password=password)
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

        if check_password(username, password):
            return redirect(url_for('dashboard', username=username))
    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True,port=8001)
