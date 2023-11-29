from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from jwt1 import record_login_time
from database import Users, checkpw
from Device_details import utility  


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
        print(password.encode('utf-8').decode(),"\n ppppp\n", user.password.encode('utf-8'))

        if user and checkpw(password.encode('utf-8'),user.password.encode('utf-8')):#check_password_hash(user.password,password):
            # Record the login time
            token=record_login_time(username)
            
            utility(username)
            
            return redirect(url_for('dash.dashboard',username=username, token=token))
    return jsonify({'error': 'Invalid credentials'}), 401
