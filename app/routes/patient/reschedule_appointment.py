from flask import render_template, request, redirect, url_for, flash
from models import Appointment, DocSchedule, db
from . import patient_bp
from datetime import datetime, time, timedelta
from flask_login import login_required, current_user


def get_shift_end_time(schedule_date, schedule_time):
    default_start = time(9, 0)
    start_time = schedule_time or default_start
    start_dt = datetime.combine(schedule_date, start_time)
    end_dt = start_dt + timedelta(hours=8)
    return end_dt.time()


@patient_bp.route('/reschedule_appointment/<int:appo_id>', methods=['GET', 'POST'])
@login_required
def reschedule_appointment(appo_id):
    patient_id = current_user.p_id
    if not patient_id:
        return redirect(url_for('auth.login'))

    appointment = Appointment.query.get_or_404(appo_id)
    if appointment.p_id != patient_id:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('patient.dashboard'))

    selected_date = request.args.get('selected_date', appointment.appo_date.strftime('%Y-%m-%d'))

    available_slots = []

    try:
        selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except Exception:
        flash('Invalid date format.', 'error')
        selected_date_obj = appointment.appo_date

    leave_schedule = DocSchedule.query.filter_by(
        doc_id=appointment.doc_id,
        schedule_date=selected_date_obj,
        title='On Leave'
    ).first()

    if leave_schedule:
       
        available_slots = []
    else:
        all_schedules = DocSchedule.query.filter_by(
            doc_id=appointment.doc_id,
            schedule_date=selected_date_obj
        ).all()

        if all_schedules:
            available_slots = [s.schedule_time.strftime('%H:%M')
                              for s in all_schedules
                              if s.title != 'On Leave' and (s.nop is None or s.nop > 0)]
        else:
         
         
            available_slots = [appointment.appo_time.strftime('%H:%M')]

    if request.method == 'POST':
        date_str = request.form.get('appo_date')
        time_str = request.form.get('appo_time')

        if not date_str or not time_str:
            flash('Please select both date and time.', 'error')
            return render_template('patient/reschedule_appointment.html',
                                   appointment=appointment,
                                   selected_date=selected_date,
                                   available_slots=available_slots)

        try:
            new_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            new_time = datetime.strptime(time_str, '%H:%M').time()
        except Exception as e:
            flash(f'Invalid date/time format: {str(e)}', 'danger')
            return render_template('patient/reschedule_appointment.html',
                                   appointment=appointment,
                                   selected_date=selected_date,
                                   available_slots=available_slots)

    
    
        leave_check = DocSchedule.query.filter_by(
            doc_id=appointment.doc_id,
            schedule_date=new_date,
            title='On Leave'
        ).first()
        if leave_check:
            flash('Doctor is on leave on this date.', 'danger')
            return render_template('patient/reschedule_appointment.html',
                                   appointment=appointment,
                                   selected_date=selected_date,
                                   available_slots=available_slots)

   
   
        doctor_id = appointment.doc_id
        schedule = DocSchedule.query.filter_by(
            doc_id=doctor_id,
            schedule_date=new_date,
            schedule_time=new_time
        ).first()

        DEFAULT_SHIFT_START = time(9, 0)
        DEFAULT_SHIFT_END = (datetime.combine(new_date, DEFAULT_SHIFT_START) + timedelta(hours=8)).time()

      
        if schedule:
            start_time = schedule.schedule_time or DEFAULT_SHIFT_START
            shift_end = get_shift_end_time(new_date, start_time)
            if not (start_time <= new_time < shift_end):
                flash('Selected time is outside the doctor shift hours.', 'danger')
                return render_template('patient/reschedule_appointment.html',
                                       appointment=appointment,
                                       selected_date=selected_date,
                                       available_slots=available_slots)

            if schedule.nop is not None and schedule.nop <= 0:
                flash('Selected slot is not available. Please choose another slot.', 'danger')
                return render_template('patient/reschedule_appointment.html',
                                       appointment=appointment,
                                       selected_date=selected_date,
                                       available_slots=available_slots)
        else:
            
          
            if not (DEFAULT_SHIFT_START <= new_time < DEFAULT_SHIFT_END):
                flash('Selected time is outside the doctor working hours (09:00 to 17:00).', 'danger')
                return render_template('patient/reschedule_appointment.html',
                                       appointment=appointment,
                                       selected_date=selected_date,
                                       available_slots=available_slots)

    
        existing = Appointment.query.filter(
            Appointment.p_id == patient_id,
            Appointment.appo_date == new_date,
            Appointment.appo_time == new_time,
            Appointment.appo_id != appo_id
        ).first()

        if existing:
            flash('You already have an appointment at this time.', 'danger')
            return render_template('patient/reschedule_appointment.html',
                                   appointment=appointment,
                                   selected_date=selected_date,
                                   available_slots=available_slots)


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

        if schedule and schedule.nop is not None and schedule.nop > 0:
            schedule.nop -= 1
        elif schedule is None:
           
            pass
        else:
            flash('Selected slot is no longer available.', 'danger')
            return render_template('patient/reschedule_appointment.html',
                                   appointment=appointment,
                                   selected_date=selected_date,
                                   available_slots=available_slots)

        try:
            db.session.commit()
            flash('Appointment rescheduled successfully.', 'success')
            return redirect(url_for('patient.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to reschedule appointment: {str(e)}', 'danger')
            return render_template('patient/reschedule_appointment.html',
                                   appointment=appointment,
                                   selected_date=selected_date,
                                   available_slots=available_slots)

    return render_template('patient/reschedule_appointment.html',
                           appointment=appointment,
                           selected_date=selected_date,
                           available_slots=available_slots)
