from flask import render_template, request, redirect, url_for, flash
from models import Appointment, db, Patient, Treatment
from flask_login import login_required, current_user
from . import doctor_bp


@doctor_bp.route('/doctor/add_treatment/<int:appo_id>', methods=['GET', 'POST'])
@login_required
def add_treatment(appo_id):
    appointment = Appointment.query.get_or_404(appo_id)

    if appointment.doc_id != current_user.doc_id:
        flash("Unauthorized action", "danger")
        return redirect(url_for('doctor.view_appointment'))  
    patient = Patient.query.get(appointment.p_id)  

    if request.method == 'POST':
        diagnosis = request.form.get('diagnosis')
        treatment_desc = request.form.get('treatment')
        prescriptions = request.form.get('prescriptions')

        treatment = Treatment(
            appointment_id=appo_id,
            doctor_id=current_user.doc_id,
            patient_id=patient.p_id,
            diagnosis=diagnosis,
            treatment=treatment_desc,
            prescriptions=prescriptions
        )
        db.session.add(treatment)
        appointment.status = 'Completed'
        db.session.commit()
        flash('Treatment added and appointment marked as Completed.', 'success')
        return redirect(url_for('doctor.view_appointment'))

    return render_template('add_treatment.html', appointment=appointment, patient=patient)
