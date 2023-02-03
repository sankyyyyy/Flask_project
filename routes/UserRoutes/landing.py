from flask import Flask,Blueprint,render_template

landing_bp = Blueprint("landing",__name__)

@landing_bp.route('/')
def landing():
    return render_template('landing.html')

@landing_bp.route('/doctors')
def doctors():
    return render_template('doctors.html')