from flask import Blueprint, render_template, request
from . import admin_bp 
from datetime import datetime
from models import Appointment, Patient, Doctor , Specialities

@admin_bp.route('/appointments', methods = ['GET'])
def list_appointments():
    q = request.args.get('q')
    # Use outer joins so appointments are not dropped when doctor or speciality is missing
    query = Appointment.query.join(Patient).outerjoin(Doctor).outerjoin(Specialities, Doctor.specialty_id == Specialities.id)

    
    if q:
        like = f"%{q}%"
        # use ilike for case-insensitive matching and ensure correct method name
        query = query.filter((
            Patient.p_name.ilike(like) |
            Doctor.doc_name.ilike(like) |
            Specialities.s_name.ilike(like)
        ))
        
    appointments = query.order_by(Appointment.appo_date.desc()).all()
    for appt in appointments:
       appt.id = appt.appo_id
       appt.patient_name = appt.patient.p_name if appt.patient else 'N/A'
       appt.doctor_name = appt.doctor.doc_name if appt.doctor else 'N/A'
       appt.specialization = appt.doctor.speciality.s_name if appt.doctor and appt.doctor.speciality else 'N/A'
       appt.appointment_date = appt.appo_date.strftime('%Y-%m-%d') if appt.appo_date else 'N/A'
       appt.appointment_time = appt.appo_time.strftime('%H:%M') if appt.appo_time else 'N/A'

    
    
    return render_template('admin/appointment.html',appointments=appointments, q=q)

