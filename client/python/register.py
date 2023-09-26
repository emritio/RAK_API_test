from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from database import db, Users

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
        #hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create a new User instance and save it to the database
        new_user = Users(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return render_template('index.html')
        #return redirect(url_for('index.html'))
