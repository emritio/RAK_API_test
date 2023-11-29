from flask_sqlalchemy import SQLAlchemy # Database setup
from sqlalchemy import create_engine
import api_keys #Python file that contains all the keys
import datetime
from bcrypt import hashpw,gensalt,checkpw
db=SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = api_keys.db_key
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    #The user table is created with required attributes
class Users(db.Model):

    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(400), nullable=False)
    tokenid=db.Column(db.String(300),unique=True)
    last_login_time = db.Column(db.DateTime)
    online=db.Column(db.String(10))


    def __init__(self, username, password, online=False, last_login_time=None, tokenid=None):
        self.username = username
        self.salt=gensalt()
        self.tokenid=tokenid
        self.last_login_time = last_login_time
        self.online=online


class SystemMetrics(db.Model):
    metric_id=db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(300), db.ForeignKey('users.username'), nullable=False)
    cpu_utilization = db.Column(db.Float, nullable=False)
    ram_utilization = db.Column(db.Float, nullable=False)
    disk_utilization = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime)
    

    def __init__(self,user,cpu, ram, disk, tstamp):
        self.username=user
        self.timestamp=tstamp
        self.cpu_utilization=cpu
        self.ram_utilization=ram
        self.disk_utilization=disk
        

