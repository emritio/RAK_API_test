from flask import Flask # Main flask framework
from apilog import apilog_blueprint
from register import reg_blueprint
from login import login_blueprint
from jwt1 import init_jwt
from dash import dash_blueprint
from database import init_db
from logout import logout_blueprint

#Starts Flask
app = Flask(__name__)

#Base Version 0-python.0-html.0-CSS (denotes changes from the base version)
app.config['VERSION'] = '0.0.0'

init_db(app)
init_jwt(app)

#Main function starts the server on port 8000
if __name__ == '__main__':
    app.register_blueprint(apilog_blueprint)
    app.register_blueprint(reg_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(dash_blueprint)
    app.register_blueprint(logout_blueprint)
    app.run(debug=True,port=8000,host='0.0.0.0')

