from database import db, Users
from flask import Blueprint, redirect, url_for, request

logout_blueprint = Blueprint('logout', __name__)


@logout_blueprint.route('/logout')
def logout_route():
    print('before')
    usern=request.args.get('uname')
    print('after usern:', usern)
    user=Users.query.filter_by(username=usern).first()
    # Invalidate the user's session token
    if user:
        user.tokenid = None
        user.online = False

    db.session.commit() 

    # Redirect the user to the login page
    return redirect(url_for('apilog.index'))
