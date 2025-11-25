from flask import request, redirect, session, render_template , redirect, url_for, flash
from . import patient_bp
from datetime import datetime
from models import Patient, db , Specialities
from werkzeug.security  import generate_password_hash, check_password_hash
from app.extensions import csrf


@csrf.exempt
@patient_bp.route('/patients/edit/<int:patient_id>', methods=['GET', 'POST'])
def edit_data(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    if request.method == 'POST':
        patient.p_name = request.form['p_name']
        patient.p_email = request.form['p_email']
        patient.p_tel = request.form['p_tel']

        dob_str = request.form['p_dob']
        if dob_str:
            patient.p_dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

        patient.p_address = request.form['p_address']
        new_pw = request.form.get('new_password')

        if new_pw:
            patient.password = generate_password_hash(new_pw)

        db.session.commit()
        return redirect(url_for('patient.dashboard'))

    return render_template('patient/edit_data.html', patient=patient)
