from flask import flash, redirect, url_for, render_template, request
from . import patient_bp 
from datetime import datetime
from models import Appointment, Patient
from flask_login import login_required, current_user
from app.extensions import csrf

@csrf.exempt
@patient_bp.route('/appointments', methods=['GET','POST'])
@login_required
def appointments():
    patient_id = current_user.p_id 
    appointments = Appointment.query.filter_by(p_id=patient_id).order_by(
        Appointment.appo_date.desc(),
        Appointment.appo_time.desc()
    ).all()
    return render_template('patient/view_appointment.html', appointments=appointments, patient_id=patient_id)