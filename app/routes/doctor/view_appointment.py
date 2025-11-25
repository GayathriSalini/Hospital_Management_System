from flask import render_template
from models import Appointment
from datetime import date
from flask_login import login_required, current_user
from . import doctor_bp
from app.extensions import csrf


@csrf.exempt
@doctor_bp.route('/appointments', methods=['GET'])
@login_required
def view_appointment():
    today = date.today()
    daily_appointments = Appointment.query.filter_by(doc_id=current_user.doc_id, appo_date=today).all()
    return render_template('doctor/view_appointment.html', daily_appointments=daily_appointments)
