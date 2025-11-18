from flask import request, session, redirect, url_for, flash, render_template
from models import Patient, Doctor, Appointment, DocSchedule, db
from datetime import datetime, time, timedelta
from . import patient_bp
from flask_login import login_required, current_user


def get_shift_end_time(schedule_date, schedule_time):
    default_start = time(9, 0)
    start_time = schedule_time or default_start
    start_dt = datetime.combine(schedule_date, start_time)
    end_dt = start_dt + timedelta(hours=8)
    return end_dt.time()


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
            flash('All detail Required', 'danger')
            return redirect(url_for('patient.book_appointment'))

        try:
            appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            appointment_time = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            return redirect(url_for('patient.book_appointment'))

    
        leave_schedule = DocSchedule.query.filter_by(
            doc_id=doctor_id,
            schedule_date=appointment_date,
            title="On Leave"
        ).first()
        if leave_schedule:
            flash('Doctor is on leave  on the selected date.', 'danger')
            return redirect(url_for('patient.book_appointment'))

     
     
        schedules = DocSchedule.query.filter_by(
            doc_id=doctor_id,
            schedule_date=appointment_date
        ).all()

       
        default_start_time = time(9, 0)
        default_end_time = (datetime.combine(appointment_date, default_start_time) + timedelta(hours=8)).time()

       
        within_shift = False

        for schedule in schedules:
     
            if schedule.title == "On Leave":
                continue

            start_time = schedule.schedule_time or default_start_time
            end_time = get_shift_end_time(appointment_date, start_time)

           
            if start_time <= appointment_time < end_time:
                within_shift = True
                matching_schedule = schedule
                break

        if not schedules:
           
            if not (default_start_time <= appointment_time < default_end_time):
                flash('Booked time is outside the doctors working hours ', 'danger')
                return redirect(url_for('patient.book_appointment'))
          
          
            matching_schedule = None
            within_shift = True

        if not within_shift:
            flash('Booked appointment time is outside the doctors available shift hours.', 'danger')
            return redirect(url_for('patient.book_appointment'))

    
        DEFAULT_CAPACITY = 20

        if matching_schedule:
            if matching_schedule.nop is not None and matching_schedule.nop <= 0:
                flash('Slot is not available, select another slot.', 'danger')
                return redirect(url_for('patient.book_appointment'))
        else:
        
            
            booked_count = Appointment.query.filter_by(
                doc_id=doctor_id,
                appo_date=appointment_date,
                appo_time=appointment_time
            ).count()

            if booked_count >= DEFAULT_CAPACITY:
                flash('Slot is full, please choose another date.', 'danger')
                return redirect(url_for('patient.book_appointment'))

       
        time_appointment = timedelta(minutes=3)
        request_time = datetime.combine(appointment_date,appointment_time)
        
        doc_appointments= Appointment.query.filter_by(
            doc_id=doctor_id,
            appo_date=appointment_date,
            status="Booked"
        ).all()
       
        for appt in doc_appointments:
            existing_time = datetime .combine(appt.appo_date, appt.appo_time)
            if abs((request_time - existing_time).total_seconds())< time_appointment.total_seconds():
                flash("Book in another this slot is already booked","danger")
                return redirect(url_for('patient.book_appointment'))
       
       
       
       
        existing = Appointment.query.filter_by(
            p_id=patient_id,
            doc_id=doctor_id,
            appo_date=appointment_date,
            appo_time=appointment_time
        ).first()

        if existing:
            flash('You already have an appointment at this time.', 'danger')
            return redirect(url_for('patient.book_appointment'))
        
        new_appt = Appointment(
            p_id=patient_id,
            doc_id=doctor_id,
            appo_date=appointment_date,
            appo_time=appointment_time,
            status='Booked'
        )
        db.session.add(new_appt)
 
        if matching_schedule and matching_schedule.nop is not None:
            matching_schedule.nop -= 1

        db.session.commit()

        flash('Appointment booked successfully.', 'success')
        return redirect(url_for('patient.book_appointment'))

    return render_template('patient/book_appointment.html', doctors=doctors, datetime=datetime)
