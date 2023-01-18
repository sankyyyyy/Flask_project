from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
from flask_qrcode import QRcode
import qr_code

app = Flask(__name__)
app.config["DEBUG"] = True
QRcode(app)

app.secret_key = 'mysecretkeywhichissecret'
# database connection
try:
    connection = mysql.connector.connect(host="localhost",user="sanket",passwd="sanket",database="lineup",auth_plugin='mysql_native_password')
    # print(connection)
except Exception as e:
    print(e)

cur = connection.cursor(buffered=True)



@app.route('/register',methods=["GET","POST"])
def register():
    msg = ''
    if request.method == 'POST':
        print(request.form)
        cur.execute("select * from accounts where username=%s",(request.form['username'],))
        account = cur.fetchone()
        if account:
            msg = "Account already exsist!"
        else:
            cur.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (request.form['username'], request.form['password'], request.form['email'], request.form['name']))
            connection.commit()
        return redirect(url_for("login"))
 
    return render_template("register.html",msg = msg)
 
@app.route('/',methods=["GET","POST"])
def home():
    try:
        cur.execute("show databases")
        if request.method=="POST":
            result = request.form["result"]
            print(result)
            a=""
            b=[]
            for i in range(len(result)):
                if result[i] == "=" or result[i] == ",":
                    b.append(a)
                    a= ""
                    continue
                a+=result[i]
            b.append(a)
            username = b[1]
            slot = b[3]
            print(username)
            print(slot)
            cur.execute("update slots set is_confirmed=True where slot_no=%s and slot_user=%s",(slot,username))
            connection.commit()
            return f"{request.form}"
        return render_template('home.html',data = cur)
    except Exception as e:
        print(e)
        return "it's not you it's us sorry"

@app.route('/login',methods=["GET","POST"])
def login():
    msg = "not logged in"
    if request.method == "POST":
        print(request.form)
        cur.execute("select id,username,pass from accounts where username=%s and pass=%s",(request.form['username'],request.form['password']))
        account = cur.fetchone()
        print(account)
        if account:
            msg = "login succsesful"
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
        else:
            msg = "invalid credintials"
    if msg == "invalid credintials" or msg == "not logged in":
        return render_template("login.html",data = msg)
    elif msg == "login succsesful":
        return redirect(url_for("home",msg = msg))


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/admin',methods = ['POST', 'GET'])
def admin():
    id = session.get("id")
    username = session.get("username")
    # if username != "admin":
    #     return "you're not admin"
    cur.execute("select qr_img from slots")
    binary_data = []
    for i in cur:
        # print(i[0])
        if i[0] != None:
            # print(i[0])
            img = qr_code.binary_to_file(i[0])
            binary_data.append(img)
        else:
            binary_data.append(i[0])
    # print(binary_data)
    # img = qr_code.binary_to_file(binary_data)
    data = []
    cur.execute("select slot_no,slot_user,is_confirmed,qr_img from slots")
    i = 0
    for slot_no,slot_user,is_confirmed,img_qr in cur:
        temp = [slot_no,slot_user,is_confirmed,binary_data[i]]
        i+=1
        data.append(temp)
    # print(data)

    return render_template("admin.html",data = data,id = id,username=username)


@app.route('/del',methods=['POST','GET'])
def del_it():
    if request.method == 'POST':
        print(request.form)
        slot = request.form["Served"]
        cur.execute("delete from slots where slot_no=%s",(slot,))
        connection.commit()
    return redirect(url_for("admin"))

@app.route('/bookslot',methods = ['POST', 'GET'])
def book_slot():
    if not session.get("id"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    print("inside book_slot")

    if request.method == "GET":
        cur.execute("select slot_no from slots where slot_user is NULL")
        my_data = []
        for i in cur:
            my_data.append(i[0])
        return render_template("bookslot.html",data = my_data)

    if request.method == "POST":
        result = request.form["submit"]
        id = session.get('id')
        username = session.get('username')
        print(id,username)
        print(result)
        cur.execute("select * from slots where slot_user=%s",(username,))
        account = cur.fetchone()
        if account:
            return "you can book only one slot in one day"
        else:
            img = qr_code.my_qr(f'username={username},slot={result}')
            cur.execute("update slots set slot_user=%s,qr_img =%s where slot_no =%s",(username,img,result))
            connection.commit()
            return "slot book succsefully"



# this route will add new slots it will only accsesible from admin
# only admin can add new slots
@app.route("/ininitiateslot",methods = ['POST'])
def ininitiateslot():
    result = request.form
    time = result["start"]
    time = int(time[0:2]) %12
    try:
        for i in range(5):
            cur.execute("insert into slots(slot_no) values(%s)",(time,))
            time = time %12 +1
        connection.commit()
    except Exception as e:
        print(e)
    return redirect("/")



if __name__ == '__main__':
    app.run(debug=True)
