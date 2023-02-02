from flask import Flask,render_template,request,redirect,url_for,session,flash,Response,Blueprint
from database import connect_to_database
import qr_code
from datetime import date


bookslot_bp = Blueprint('bookslot',__name__)


@bookslot_bp.route('/bookslot',methods = ['POST', 'GET'])
def book_slot():
    connection = connect_to_database()
    cur = connection.cursor(buffered=True)
    try:
        if not session.get("id"):
            return redirect(url_for("login.login"))
        if request.method == "GET":
            today_time = date.today()
            cur.execute("select slot_time from slots where slot_user is NULL and date=%s",(today_time,))
            my_data = []
            for i in cur:
                my_data.append(i[0])
            return render_template("bookslot.html",data = my_data,today_date= today_time )

        if request.method == "POST":
            result = request.form["submit"]
            id = session.get('id')
            username = session.get('username')
            cur.execute("select * from slots where slot_user=%s",(username,))
            account = cur.fetchone()
            if account:
                flash("you can only book one slot in one day")
                return redirect(url_for('bookslot.book_slot'))
            else:
                data = {"username":username,"slot":result}
                img = qr_code.my_qr(data)
                cur.execute("update slots set slot_user=%s,qr_img =%s where slot_time =%s",(username,img,result))
                connection.commit()
                session['slot'] = result
                flash("slot booked succesfully")
                return redirect(url_for("bookslot.book_slot"))
    except Exception as e:
        return str(e)
    finally:
        cur.close()

@bookslot_bp.route('/cancel_slot',methods=['GET','POST'])
def cancel_by_user():
    connection = connect_to_database()
    cur = connection.cursor(buffered=True)
    try:
        if request.method=='GET':
            username = session.get("username")
            cur.execute("select * from accounts where username=%s",(username,))
            account = cur.fetchone()
            cur.execute("select slot_time,date from slots where slot_user=%s",(username,))
            slot_account = cur.fetchone()
            return render_template("status.html",username=username,account = account,slot_account=slot_account)

        if request.method =='POST':
            username = session.get("username")
            cur.execute("select * from slots where slot_user=%s",(username,))
            account = cur.fetchone()
            if account:
                cur.execute("update lineup.slots set slot_user=NULL, is_confirmed=0 ,qr_img=NULL where slot_user=%s",(username,))
                connection.commit()
            return redirect(url_for('bookslot.cancel_by_user'))
    except Exception as e:
        return str(e)
    finally:
        cur.close()