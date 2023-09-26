from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from jwt1 import is_session_expired, record_login_time, create_access_token
from database import db, Users, checkpw, hashpw


login_blueprint = Blueprint('login', __name__)

#Login page to check credentials
@login_blueprint.route('/login', methods=['GET','POST'])
def login_route():
    
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()

        if user and password==user.password:#checkpw(password.encode('utf-8')[0:20],user.password):#check_password_hash(user.password,password):
            # Record the login time
            record_login_time(username)

            access_token = create_access_token(identity=username)
            #print(f'Version: {app.config["VERSION"]}')
            #return render_template('dashboard.html')
            return redirect(url_for('dash.dashboard',username=username,token=access_token))
    return jsonify({'error': 'Invalid credentials'}), 401
