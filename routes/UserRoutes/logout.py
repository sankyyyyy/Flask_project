from flask import Flask,redirect,url_for,session,Blueprint


logout_bp = Blueprint('logout',__name__)

@logout_bp.route('/logout')
def logout():
    try:
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
        return redirect(url_for('login.login'))
    except Exception as e:
        return str(e)