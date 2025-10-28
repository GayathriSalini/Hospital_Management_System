from flask import Blueprint, render_template, request
from . import admin_bp 
from datetime import datetime
from models import Appointment, Patient, Doctor , Specialities

@admin_bp.route('/appointments', methods = ['GET'])
def list_appointments():
    q = request.args.get('q')
    query = Appointment.query.join(Patient).join(Doctor).join(Specialities, Doctor.specialty_id == Specialities.id)

    
    if q:
        like = f"%{q}%"
        query = query.filter((
            Patient.p_name.islike(like) |
            Doctor.doc_name.islike(like) |
            Specialities.s_name.ilike(like)
        ))
        
    appointments = query.order_by(Appointment.appo_date.desc()).all()
    return render_template('admin/appointment.html',appointments=appointments, q=q)

