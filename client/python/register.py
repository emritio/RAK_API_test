from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from database import db, Users
import bcrypt

reg_blueprint = Blueprint('register', __name__)
#The function routes to the registration page for user info
@reg_blueprint.route('/register', methods=['GET', 'POST'])
def register_route():
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
        salt=bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        hashed_password2=hashed_password.decode('utf-8')
        a=b'1001'
        print(len(a))
        print(hashed_password)
        print(hashed_password2,"\n",len(hashed_password2),"\n")
        # Create a new User instance and save it to the database
        new_user = Users(username=username, password=hashed_password2)
        db.session.add(new_user)
        db.session.commit()

        
        return render_template('index.html')
        #return redirect(url_for('index.html'))
