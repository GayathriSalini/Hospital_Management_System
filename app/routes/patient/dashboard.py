from flask import Blueprint, render_template, session, redirect, url_for
from models import Patient, Appointment, PatientDetails  # Adjust import paths as needed
from datetime import datetime, date
from . import patient_bp
from flask_login import login_required, current_user

@patient_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
        patient_id = current_user.p_id
        
        
        patient = Patient.query.filter_by(p_id=patient_id).first()
       
        
        details = PatientDetails.query.filter_by(patient_id=patient_id).first()
        
        today = date.today()
        now = datetime.now().time()
        upcoming_appointments = Appointment.query.filter(
            Appointment.p_id == patient_id,
            Appointment.appo_date >= today
        ).order_by(Appointment.appo_date.asc(), Appointment.appo_time.asc()).all()
        
        
        
        return render_template('patient/dashboard.html',
                               patient=patient,
                               details=details,
                               upcoming_appointments=upcoming_appointments)
 
