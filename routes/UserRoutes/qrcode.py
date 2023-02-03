from flask import Flask,redirect,url_for,session,flash,Response,Blueprint
from database import connect_to_database
from datetime import datetime
import cv2,json

qrcode_bp = Blueprint('qrcode',__name__)


qr_data_set = []

def gen():
    qr_detector = cv2.QRCodeDetector()

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        data, bbox, rectified_image = qr_detector.detectAndDecode(frame)
        if data:
            if len(qr_data_set) < 1:
                qr_data_set.append(data)
                cap.release() 
        ret, jpeg = cv2.imencode('.jpg', frame)
        if ret:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            print("Frame not captured")  

@qrcode_bp.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@qrcode_bp.route('/confirm_qr')
def confirm_qr():
    connection = connect_to_database()
    cur = connection.cursor(buffered=True)
    try:
        if qr_data_set:
            username_session = session.get("username")
            account = qr_data_set[0]
            account = json.loads(account)
            username = account['username']
            if username == username_session:
                slot = account['slot']
                slot = datetime.strptime(slot, "%H:%M")
                slot = slot.strftime("%H:%M")
                cur.execute("select * from slots where slot_user=%s and slot_time=%s",(username,slot))
                user = cur.fetchone()
                if user:
                    qr_data_set.clear()
                    cur.execute("update slots set is_confirmed=True where slot_time=%s and slot_user=%s",(slot,username))
                    connection.commit()
                    flash("Your Appointment Confirmed succesfully","succsess")
                    return redirect(url_for('login.login'))
                else:
                    qr_data_set.clear()
                    flash("You haven't booked appointment yet!","error")
                    return redirect(url_for('home.home'))

            else:
                qr_data_set.clear()
                flash("Username is not matching!","error")
                return redirect(url_for('home.home'))
    except Exception as e:
        return str(e)
    finally:
        cur.close()
    return redirect(url_for('home.home'))
