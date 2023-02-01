from flask import Flask
from flask_bootstrap import Bootstrap
from routes.AdminRoutes import admin
from routes.UserRoutes import home, login, logout,register,bookslot,qrcode

app = Flask(__name__)
app.config["DEBUG"] = True
Bootstrap(app)

app.register_blueprint(register.register_bp)
app.register_blueprint(login.login_bp)
app.register_blueprint(home.home_bp)
app.register_blueprint(logout.logout_bp)
app.register_blueprint(admin.admin_bp)
app.register_blueprint(bookslot.bookslot_bp)
app.register_blueprint(qrcode.qrcode_bp)


app.secret_key = 'mysecretkeywhichissecret'
log.start()

if __name__ == '__main__':
    app.run(debug=True)