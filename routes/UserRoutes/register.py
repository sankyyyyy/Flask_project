from flask import Flask,render_template,request,redirect,url_for,session,flash,Response,Blueprint
from database import connect_to_database
from werkzeug.security import generate_password_hash, check_password_hash

register_bp = Blueprint('register', __name__)

register_bp.secret_key = 'mysecretkeywhichissecret'

@register_bp.route('/register',methods=["GET","POST"])
def register():
    connection = connect_to_database()
    cur = connection.cursor(buffered=True)
    try:
        if request.method == 'POST':
            cur.execute("select * from accounts where username=%s",(request.form['username'],))
            account = cur.fetchone()
            if account:
                flash("This Username is taken","error")
            else:
                password = request.form['password']
                hashed_password = generate_password_hash(password)
                cur.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (request.form['username'],hashed_password, request.form['email'], request.form['name']))
                connection.commit()
                flash("Registration succsesfull","message")
                return redirect(url_for("login.login"))
        return render_template("/register.html")
    except Exception as e:
        print(e)
        return str(e)
    finally:
        cur.close()