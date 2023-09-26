#Dashboard opens the home page
from database import db, Users
from flask import render_template, redirect, url_for, Blueprint, request 
from jwt1 import is_session_expired
dash_blueprint = Blueprint('dash', __name__)

@dash_blueprint.route('/dashboard/<username>', methods=['GET'])
def dashboard(username):
    token = request.args.get('token')

    # You can use the token for authentication or any other purpose
    if not token:
        # Handle the case where the token is missing
        return "Token is missing", 401  # Return a 401 Unauthorized status code

    user = Users.query.filter_by(username=username).first()

    if user:
        # You can implement token validation logic here
        if is_session_expired(user.last_login_time):
            return render_template('index.html')
        else:
            # Pass the token to the dashboard template (optional)
            return render_template('dashboard.html', username=username, token=token)
    else:
        return redirect(url_for('index'))
