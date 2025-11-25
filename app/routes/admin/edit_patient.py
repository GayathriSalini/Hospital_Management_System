from flask import request, redirect, session, render_template , redirect, url_for, flash
from . import admin_bp 
from datetime import datetime
from models import Patient, db , Specialities
from werkzeug.security  import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from app.extensions import csrf


@csrf.exempt
@admin_bp.route('/patients/edit/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def edit_patient(patient_id):
    if not hasattr(current_user, 'a_email') or current_user.a_email != "admin@nhshospital.com":
       
        return redirect(url_for('auth.login'))
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
        return redirect(url_for('admin.patients_list'))

    return render_template('admin/edit_patient.html', patient=patient)