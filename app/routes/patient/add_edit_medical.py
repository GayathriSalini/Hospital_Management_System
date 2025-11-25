from . import patient_bp
from flask import request, redirect, session, render_template, url_for
from models import PatientDetails, db
from flask_login import login_required, current_user
from app.extensions import csrf


@csrf.exempt

@patient_bp.route('/medical/edit', methods=['GET', 'POST'])
@login_required 
def add_edit_medical():
        patient_id = current_user.p_id

        medical_details = PatientDetails.query.filter_by(patient_id=patient_id).first()

        if request.method == 'POST':


            if not medical_details:
                medical_details = PatientDetails(patient_id=patient_id)
                db.session.add(medical_details)

            medical_details.blood_group = request.form['blood_group']
            medical_details.height_cm = request.form['height_cm']
            medical_details.weight_kg = request.form['weight_kg']
            medical_details.allergies = request.form['allergies']
            medical_details.chronic_conditions = request.form['chronic_conditions']


            db.session.commit()
            return redirect(url_for('patient.dashboard'))

      
        if not medical_details:
            class EmptyMedical:
                blood_group = None
                height_cm = None
                weight_kg = None
                allergies = None
                chronic_conditions = None
            medical_details = EmptyMedical()

        return render_template('patient/add_edit_medical.html', medical_details=medical_details)


