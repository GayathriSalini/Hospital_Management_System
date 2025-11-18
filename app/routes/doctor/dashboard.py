from flask import Blueprint, render_template, session, redirect, url_for
from datetime import datetime, timedelta
from models import Appointment, Patient, Doctor, Treatment, DocSchedule, Specialities
from . import doctor_bp
from flask_login import login_required, current_user
from sqlalchemy import distinct
from collections import Counter

@doctor_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    doctor_id = current_user.doc_id
    today = datetime.today().date()
    week_later = today + timedelta(days=7)

    daily_appointments = Appointment.query.filter(
        Appointment.doc_id == doctor_id,
        Appointment.appo_date == today,
        Appointment.status != 'Cancelled'
    ).all()
    
    

    weekly_appointments = Appointment.query.filter(
        Appointment.doc_id == doctor_id,
        Appointment.appo_date.between(today, week_later),
        Appointment.status != 'Cancelled'
    ).all()

    schedules = DocSchedule.query.filter(
        DocSchedule.doc_id == doctor_id,
        DocSchedule.schedule_date.between(today, week_later)
    ).order_by(DocSchedule.schedule_date, DocSchedule.schedule_time).all()

    doctor = Doctor.query.get(doctor_id)
    specialty = None
    if doctor and doctor.specialty_id:
        specialty = Specialities.query.filter_by(id=doctor.specialty_id).first()


    total_patients = Patient.query.join(Appointment).filter(
        Appointment.doc_id == doctor_id
    ).distinct().all()
    
    
    
    """ Chart """
    fixed_labels = ["Booked", "Completed", "Cancelled"]
    actual_counts = Counter([appt.status for appt in weekly_appointments])
    status_counts = {label: actual_counts.get(label, 0) for label in fixed_labels}
    status_data = [status_counts[label] for label in fixed_labels]
    

    return render_template('doctor/dashboard.html',
                           daily_appointments=daily_appointments,
                           weekly_appointments=weekly_appointments,
                           doctor=doctor,
                           schedules=schedules,
                           specialty=specialty,
                           total_patients=total_patients,
                           status_counts=status_counts,
                           status_data=status_data,
                           status_labels=fixed_labels 
                                                 )
        
        
        