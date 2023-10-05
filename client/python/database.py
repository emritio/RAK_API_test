from flask_sqlalchemy import SQLAlchemy # Database setup
from sqlalchemy import create_engine
import api_keys #Python file that contains all the keys
import datetime
#from werkzeug.security import generate_password_hash, check_password_hash
from bcrypt import hashpw,gensalt,checkpw
db=SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = api_keys.db_key
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

#The user table is created with required attributes
class Users(db.Model):
    #id=db.Column(db.Integer, autoincrement=True, unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(400), nullable=False)
    #register_time=db.Column(db.DateTime)
    tokenid=db.Column(db.String(300),unique=True)
    last_login_time = db.Column(db.DateTime)

    def __init__(self, username, password, last_login_time=None,tokenid=None):
        self.username = username
        #self.password = generate_password_hash(password,method='scrypt')
        self.salt=gensalt()
        self.password=password#hashpw(password.encode('utf-8'),self.salt)[0:20]
        self.tokenid=tokenid
        #self.register_time=datetime.datetime.now()
        self.last_login_time = last_login_time


#Function to verify credentials
'''def check_password(username, password):
    user = Users.query.filter_by(username=username).first()
    if user:
        return user.password == password.encode('utf-8')
    return False'''
