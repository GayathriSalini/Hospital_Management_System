from flask import Blueprint, render_template, session, redirect, url_for

doctor_bp = Blueprint('doctor',__name__, url_prefix = '/doctor')

@doctor_bp.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'user_role' in session and session['user_role'] == 'doctor':
        return render_template('doctor/dashboard.html')
    else:
        return redirect(url_for('auth.login'))