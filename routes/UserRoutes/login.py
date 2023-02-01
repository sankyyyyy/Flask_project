from flask import Flask,render_template,request,redirect,url_for,session,flash,Response,Blueprint
from database import connect_to_database
from werkzeug.security import check_password_hash

login_bp = Blueprint('login',__name__)

login_bp.secret_key = 'mysecretkeywhichissecret'


@login_bp.route('/login',methods=["GET","POST"])
def login():
    connection = connect_to_database()
    cur = connection.cursor(buffered=True)
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        cur.execute("select id,username,pass from accounts where username=%s",(username,))
        account = cur.fetchone()


        if account and check_password_hash(account[2], password):
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            if session.get("username") == "admin":
                return redirect(url_for("admin.admin"))
            return redirect(url_for("home.home"))
        else:
            flash("invalid credintials","error")
            return redirect(url_for("login.login"))
    return render_template('/login.html')

