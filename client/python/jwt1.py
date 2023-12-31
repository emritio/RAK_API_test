from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity  # Web token setup
import datetime # record time for login session
import api_keys #Python file that contains all the keys
from database import db, Users


jwt = JWTManager()

def init_jwt(app):
    app.config['JWT_SECRET_KEY'] =   api_keys.jwt_key
    jwt.init_app(app)

#Function to keep track of login time for session time-out
def record_login_time(username):
    user = Users.query.filter_by(username=username).first()
    if user:
        user.last_login_time = datetime.datetime.now()
        user.tokenid=create_access_token(identity=username)
        user.online=True
        db.session.commit() #db is constructor object
        return user.tokenid #c1

# Check if the session has expired
def is_session_expired(username,tokenid):
    user=Users.query.filter_by(username=username).first()
    current_time = datetime.datetime.now()
    n1=user.tokenid==tokenid 
    n2= (current_time - user.last_login_time).total_seconds() >6000
    return n1 and n2

def right_token(username,tokenid):
    user=Users.query.filter_by(username=username).first()
    if user.tokenid==tokenid and user.tokenid!=None:
        return True
    else:
        return False


def protected_route():
    current_user = get_jwt_identity()
    return f"Welcome, {current_user}! This is a protected route."

def authenticated(username, password):
    user = Users.query.filter_by(username=username, password=password).first()
    return user is not None