from flask import Blueprint, render_template, request, redirect, url_for, session
from models import Patient, PatientDetails, db
from . import doctor_bp
from flask_login import login_required, current_user


@doctor_bp.route('/patient/<int:patient_id>/edit_medical', methods=['GET', 'POST'])
@login_required
def edit_patient_medical(patient_id):
   
    medical_details = PatientDetails.query.filter_by(patient_id=patient_id).first()

    if request.method == 'POST':
        if not medical_details:
            medical_details = PatientDetails(patient_id=patient_id)
            db.session.add(medical_details)

        medical_details.blood_group = request.form.get('blood_group')
        medical_details.height_cm = request.form.get('height_cm')
        medical_details.weight_kg = request.form.get('weight_kg')
        medical_details.allergies = request.form.get('allergies')
        medical_details.chronic_conditions = request.form.get('chronic_conditions')

        db.session.commit()
        return redirect(url_for('doctor.dashboard')) 

    if not medical_details:
     
        class EmptyMedical:
            blood_group = None
            height_cm = None
            weight_kg = None
            allergies = None
            chronic_conditions = None
        medical_details = EmptyMedical()

    return render_template('doctor/edit_patient_medical.html', medical_details=medical_details)
