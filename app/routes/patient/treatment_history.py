from flask import  render_template
from datetime import date
from calendar import monthrange
from models import Treatment, Appointment, Doctor
from . import patient_bp
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload

@patient_bp.route('/treatment_history', methods=['GET'])
@login_required
def treatment_history():
    patient_id = current_user.p_id


    today = date.today()
    first_day = today.replace(day=1)
    last_day = today.replace(day=monthrange(today.year, today.month)[1])


    treatments = Treatment.query.join(Treatment.appointment).options(
        joinedload(Treatment.appointment).joinedload(Appointment.doctor)
    ).filter(
        Appointment.p_id == patient_id,
        Appointment.appo_date >= first_day,
        Appointment.appo_date <= last_day,
        Appointment.status == 'Completed'
    ).order_by(Appointment.appo_date.asc()).all()


    treatments_with_day = []
    for t in treatments:
        dt_str = t.appointment.appo_date.strftime('%Y-%m-%d')  # Corrected here
        day_name = t.appointment.appo_date.strftime('%A')
        treatments_with_day.append((t, dt_str, day_name))


    return render_template(
        'patient/treatment_history.html',
        treatments_with_day=treatments_with_day,
        patient_id=patient_id,
    )
