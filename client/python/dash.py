#Dashboard opens the home page
from database import db, Users
from flask import render_template, redirect, url_for, Blueprint, request 
from jwt1 import is_session_expired, right_token
dash_blueprint = Blueprint('dash', __name__)

@dash_blueprint.route('/dashboard/<username>/<token>', methods=['GET'])
def dashboard(username,token):
    #token = request.args.get('token')
    user = Users.query.filter_by(username=username).first()
    # You can use the token for authentication or any other purpose
    if not user.tokenid:
        # Handle the case where the token is missing
        return "Token is missing", 401  # Return a 401 Unauthorized status code

    

    if user:
        # You can implement token validation logic here
        if is_session_expired(username,user.tokenid):
            return render_template('index.html')
        else:
            # Pass the token to the dashboard template (optional)
            if right_token(username,token):
                return render_template('dashboard.html', username=username)
            else:
                return "Invalid URL", 401
    else:
        #return redirect(url_for('index'))
        return render_template('index.html')
