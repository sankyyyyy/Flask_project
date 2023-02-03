from flask import Flask,render_template,request,redirect,url_for,session,flash,Response,Blueprint
from database import connect_to_database
import qr_code as qr_code
from datetime import datetime,timedelta,date

admin_bp = Blueprint('admin',__name__)


@admin_bp.route('/admin',methods = ['POST', 'GET'])
def admin():
    connection = connect_to_database()
    cur = connection.cursor(buffered=True)
    try:
        id = session.get("id")
        username = session.get("username")
        if username != "admin":
            flash("You're not admin,please login with admin credentials","error")
            return redirect(url_for("login.login"))
        cur.execute("select qr_img from slots")
        binary_data = []
        for i in cur:
            if i[0] != None:
                img = qr_code.binary_to_file(i[0])
                binary_data.append(img)
            else:
                binary_data.append(i[0])
        data = []
        cur.execute("select slot_time,slot_user,is_confirmed,qr_img from slots")
        i = 0
        for slot_no,slot_user,is_confirmed,img_qr in cur:
            temp = [slot_no,slot_user,is_confirmed,binary_data[i]]
            i+=1
            data.append(temp)
        return render_template("admin.html",data = data,id = id,username=username)
    except Exception as e:
        return str(e)
    finally:
        cur.close()


@admin_bp.route('/del',methods=['POST','GET'])
def del_it():
    connection = connect_to_database()
    cur = connection.cursor(buffered=True)
    try:
        if request.method == 'POST':
            slot = request.form["Served"]
            slot = datetime.strptime(slot, "%H:%M")
            slot = slot.strftime("%H:%M")
            cur.execute("delete from slots where slot_time=%s",(slot,))
            connection.commit()
        return redirect(url_for("admin.admin"))
    except Exception as e:
        return str(e)
    finally:
        cur.close()


# this route will add new slots it will only accsesible from admin
# only admin can add new slots
@admin_bp.route("/ininitiateslot",methods = ['POST'])
def ininitiateslot():
    connection = connect_to_database()
    cur = connection.cursor(buffered=True)
    try:
        result = request.form
        time = result["start"]
        time = datetime.strptime(time, "%H:%M")
        time_str = time.strftime("%H:%M")
        for i in range(5):
            cur.execute("insert into slots(slot_time) values(%s)",(time_str,))
            time_str = datetime.strptime(time_str,'%H:%M')
            time_str = time_str + timedelta(minutes=15)
            time_str = time_str.strftime('%H:%M')
        connection.commit()
        return redirect(url_for("admin.admin"))
    except Exception as e:
        return str(e)
    finally:
        cur.close()
