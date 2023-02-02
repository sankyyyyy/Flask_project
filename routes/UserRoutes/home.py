from flask import Flask,render_template,Blueprint
from database import connect_to_database

home_bp = Blueprint('home',__name__)

@home_bp.route('/home',methods=["GET"])
def home():
    connection = connect_to_database()
    cur = connection.cursor(buffered=True)
    try:
        cur.execute("show databases")
        return render_template('home.html')
    except Exception as e:
        return str(e)
    finally:
        cur.close()
