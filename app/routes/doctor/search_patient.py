from flask import Blueprint, render_template, request, redirect, url_for, session
from models import Patient, Appointment, Treatment
from . import doctor_bp
from flask_login import login_required, current_user

@doctor_bp.route('/patient_search', methods=['GET'])
@login_required
def search_patient():
    query = request.args.get('query', '').strip()
    patients = []

    if query.isdigit():
      patients = Patient.query.filter(Patient.p_id == int(query)).all()
    else:
       patients = Patient.query.filter(
        (Patient.p_name.ilike(f'%{query}%')) |
        (Patient.p_tel.ilike(f'%{query}%'))
      ).all()

    


    return render_template('doctor/search_patient.html', patients=patients, query=query)


""" @doctor_bp.route('/patient/<int:patient_id>/treatments', methods=['GET'])
def patient_treatments(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    treatments = (
        Treatment.query.join(Appointment).
        filter(Appointment.patient_id == patient_id).
        order_by(Treatment.id.desc()).all()
    )

    return render_template('doctor/patient_treatments.html', patient=patient, treatments=treatments)

 """