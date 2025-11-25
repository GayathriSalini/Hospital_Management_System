from flask import render_template, redirect, url_for
from datetime import date
from calendar import monthrange
from models import Treatment, Appointment, Doctor
from . import admin_bp
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from app.extensions import csrf


@csrf.exempt
@admin_bp.route('/patient_treatment_history/<int:patient_id>', methods=['GET']) 
@login_required
def ptreatment_history(patient_id):
   
    if not hasattr(current_user, 'a_email') or current_user.a_email != "admin@nhshospital.com":
        return redirect(url_for('auth.login'))
    
    today = date.today()
    first_day = today.replace(day=1)
    last_day = today.replace(day=monthrange(today.year, today.month)[1])

    treatments = Treatment.query.join(Treatment.appointment).options(
        joinedload(Treatment.appointment).joinedload(Appointment.patient)
    ).filter(
        Appointment.p_id == patient_id,
        Appointment.appo_date >= first_day,
        Appointment.appo_date <= last_day,
        Appointment.status == 'Completed'
    ).order_by(Appointment.appo_date.desc()).all()

    treatments_with_day = []
    for t in treatments:
        dt_str = t.appointment.appo_date.strftime('%Y-%m-%d')
        day_name = t.appointment.appo_date.strftime('%A')
        treatments_with_day.append((t, dt_str, day_name))

    no_treatments = len(treatments_with_day) == 0

    return render_template(
        'admin/ptreatment_history.html',
        treatments_with_day=treatments_with_day,
        patient_id=patient_id,
        no_treatments=no_treatments 
    )