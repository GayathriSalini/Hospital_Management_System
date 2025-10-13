from flask import Blueprint, render_template, session, redirect, url_for

patient_bp = Blueprint('patient',__name__, url_prefix = '/patient')

@patient_bp.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'user_role' in session and session['user_role'] == 'patient':
        return render_template('patient/dashboard.html')
    else:
        return redirect(url_for('auth.login')) 