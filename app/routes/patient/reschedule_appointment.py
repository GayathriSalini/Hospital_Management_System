from flask import render_template, request, redirect, url_for, flash
from models import Appointment, DocSchedule, db
from . import patient_bp
from datetime import datetime
from flask_login import login_required, current_user


@patient_bp.route('/reschedule_appointment/<int:appo_id>', methods=['GET', 'POST'])
@login_required
def reschedule_appointment(appo_id):
    patient_id = current_user.p_id
    if not patient_id:

        return redirect(url_for('auth.login'))

    appointment = Appointment.query.get_or_404(appo_id)
    if appointment.p_id != patient_id:
      
        return redirect(url_for('patient.dashboard'))

    if request.method == 'POST':
        date_str = request.form.get('appo_date')
        time_str = request.form.get('appo_time')

        if not date_str or not time_str:
 
            return redirect(url_for('patient.reschedule_appointment', appo_id=appo_id))

        try:
            new_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            new_time = datetime.strptime(time_str, '%H:%M').time()
        except Exception:
      
            return redirect(url_for('patient.reschedule_appointment', appo_id=appo_id))

        doctor_id = appointment.doc_id
        schedule = DocSchedule.query.filter_by(
            doc_id=doctor_id,
            schedule_date=new_date,
            schedule_time=new_time
        ).first()

        if not schedule or (schedule.nop is not None and schedule.nop <= 0):
   
            return redirect(url_for('patient.reschedule_appointment', appo_id=appo_id))

        existing = Appointment.query.filter(
            Appointment.p_id == patient_id,
            Appointment.appo_date == new_date,
            Appointment.appo_time == new_time,
            Appointment.appo_id != appo_id
        ).first()

        if existing:

            return redirect(url_for('patient.reschedule_appointment', appo_id=appo_id))

        old_date = appointment.appo_date
        old_time = appointment.appo_time

        
        appointment.appo_date = new_date
        appointment.appo_time = new_time

      
        old_schedule = DocSchedule.query.filter_by(
            doc_id=doctor_id,
            schedule_date=old_date,
            schedule_time=old_time
        ).first()
        if old_schedule and old_schedule.nop is not None:
            old_schedule.nop += 1

        if schedule.nop is not None:
            schedule.nop -= 1

        try:
            db.session.commit()
            flash('Appointment rescheduled successfully', 'success')
        except Exception:
            db.session.rollback()
            flash('Failed to reschedule appointment. Please try again.', 'error')
            return redirect(url_for('patient.reschedule_appointment', appo_id=appo_id))

        return redirect(url_for('patient.dashboard'))

    return render_template('patient/reschedule_appointment.html', appointment=appointment)
