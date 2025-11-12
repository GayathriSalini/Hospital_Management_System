from flask import request, session, redirect, url_for, flash, render_template
from models import Patient, Doctor, Appointment, DocSchedule, db
from datetime import datetime
from . import patient_bp
from flask_login import login_required, current_user



@patient_bp.route('/book_appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    patient_id = current_user.p_id
    doctors = Doctor.query.all()

    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        date_str = request.form.get('appointment_date')
        time_str = request.form.get('appointment_time')

        if not (doctor_id and date_str and time_str):
            flash('All fields are required', 'error')
            return redirect(url_for('patient.book_appointment'))

        appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        appointment_time = datetime.strptime(time_str, '%H:%M').time()

        
        leave_schedule = DocSchedule.query.filter_by(
            doc_id=doctor_id,
            schedule_date=appointment_date,
            title="On Leave"
        ).first()
        if leave_schedule:
            flash('Doctor is on leave for the selected date. Please choose another date.', 'danger')
            return redirect(url_for('patient.book_appointment'))

        schedule = DocSchedule.query.filter_by(
            doc_id=doctor_id,
            schedule_date=appointment_date,
            schedule_time=appointment_time
        ).first()

        DEFAULT_CAPACITY = 10
        if schedule:
            if hasattr(schedule, 'status') and schedule.status == 'on leave':
                flash('Doctor is on leave at this time. Please select another slot.', 'danger')
                return redirect(url_for('patient.book_appointment'))
            if schedule.nop is not None and schedule.nop <= 0:
                flash('Slot is not available - select another slot.', 'danger')
                return redirect(url_for('patient.book_appointment'))
        else:
            booked_count = Appointment.query.filter_by(
                doc_id=doctor_id,
                appo_date=appointment_date,
                appo_time=appointment_time
            ).count()

            if booked_count >= DEFAULT_CAPACITY:
                flash('Slot is full, please choose another time.', 'danger')
                return redirect(url_for('patient.book_appointment'))

        existing = Appointment.query.filter_by(
            p_id=patient_id,
            doc_id=doctor_id,
            appo_date=appointment_date,
            appo_time=appointment_time
        ).first()

        if existing:
            flash('You already have an appointment at this time.', 'error')
            return redirect(url_for('patient.book_appointment'))

        new_appt = Appointment(
            p_id=patient_id,
            doc_id=doctor_id,
            appo_date=appointment_date,
            appo_time=appointment_time,
            status='Booked'
        )

        db.session.add(new_appt)

        if schedule and schedule.nop is not None:
            schedule.nop -= 1

        db.session.commit()

        flash('Appointment booked successfully.', 'success')
        return redirect(url_for('patient.book_appointment'))

    return render_template('patient/book_appointment.html', doctors=doctors, datetime=datetime)
