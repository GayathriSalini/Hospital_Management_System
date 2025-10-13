from flask import Blueprint, render_template, session, redirect, url_for
from models import Doctor, Patient, Appointment
from . import admin_bp 


@admin_bp.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'user_role' in session and session['user_role'] == 'admin':
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
    
    
