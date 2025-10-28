from flask import Blueprint, render_template, session, redirect, url_for
from datetime import datetime , timedelta
from models import Appointment, Patient, Doctor, Treatment

doctor_bp = Blueprint('doctor',__name__, url_prefix = '/doctor')

@doctor_bp.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'user_role' in session and session['user_role'] == 'doctor':
        doctor_id = session['user_id']

        today = datetime.today().date()
        week_later = today + timedelta(days=7)

        daily_appointments = Appointment.query.filter_by(doctor_id=doctor_id).filter(Appointment.appo_date == today).all()
        weekly_appointments = Appointment.query.filter_by(doctor_id=doctor_id).filter(Appointment.appo_date.between(today, week_later)).all()

        return render_template('doctor/dashboard.html',
            daily_appointments=daily_appointments,
            weekly_appointments=weekly_appointments
        )
    return redirect(url_for('auth.login'))