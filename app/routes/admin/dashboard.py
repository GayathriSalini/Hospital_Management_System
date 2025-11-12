from flask import Blueprint, render_template, session, redirect, url_for
from models import Doctor, Patient, Appointment
from . import admin_bp 
from flask_login import login_required, current_user

@admin_bp.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    if getattr(current_user, 'a_email', None) == 'admin@nhshospital.com':
        total_doctors = Doctor.query.count()
        total_patients = Patient.query.count()
        total_appointments = Appointment.query.count()
        
        return render_template(
            'admin/dashboard.html',
            total_doctors=total_doctors,
            total_patients=total_patients,
            total_appointments=total_appointments
        )
   
    else:
        return redirect(url_for('auth.login'))
    
    
