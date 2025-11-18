from flask import abort, render_template, session, redirect, url_for
from models import Patient, Appointment, PatientDetails  ,Treatment
from datetime import datetime, date
from . import patient_bp
from flask_login import login_required, current_user
from collections import Counter 

@patient_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
        if not isinstance(current_user, Patient):
            abort(403)
        patient_id = current_user.p_id
        
        patient = Patient.query.filter_by(p_id=patient_id).first()
        details = PatientDetails.query.filter_by(patient_id=patient_id).first()
        
        today = date.today()
        now = datetime.now().time()
        upcoming_appointments = Appointment.query.filter(
            Appointment.p_id == current_user.p_id,
            Appointment.status.notin_(["Completed", "Cancelled"]),
            Appointment.appo_date >= date.today()
        ).order_by(Appointment.appo_date.asc(), Appointment.appo_time.asc()).all()
    
        
    
        """ CHART """
        current_year = datetime.now().year
        appointments_with_treatment = Appointment.query.join(Treatment).filter(
            Appointment.p_id == patient_id,
            Appointment.appo_date.between(f"{current_year}-01-01", f"{current_year}-12-31")
        ).all()
    
      
        months = [appt.appo_date.month for appt in appointments_with_treatment]
    

        counts_by_month = Counter(months)
    
        labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        data = [counts_by_month.get(i, 0) for i in range(1, 13)]
    
        return render_template('patient/dashboard.html',
                               patient=patient,
                               details=details,
                               upcoming_appointments=upcoming_appointments,
                               treatment_months=labels,
                               treatment_counts=data)
 
