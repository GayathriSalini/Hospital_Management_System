from flask import render_template, request, redirect, url_for, flash
from models import Appointment, db, Patient, Treatment, PatientDetails
from flask_login import login_required, current_user
from . import doctor_bp
from app.extensions import csrf


@csrf.exempt
@doctor_bp.route('/doctor/add_treatment/<int:appo_id>', methods=['GET', 'POST'])
@login_required
def add_treatment(appo_id):
    appointment = Appointment.query.get_or_404(appo_id)
    if appointment.doc_id != current_user.doc_id:
        flash("Unauthorized action", "danger")
        return redirect(url_for('doctor.view_appointment'))

    patient = Patient.query.get(appointment.p_id)
    patient_details = PatientDetails.query.filter_by(patient_id=patient.p_id).first()

    if request.method == 'POST':
        diagnosis = request.form.get('diagnosis')
        prescription = request.form.get('prescription')  
        notes = request.form.get('notes')

        treatment = Treatment(
            appointment_id=appo_id,
            diagnosis=diagnosis,
            prescription=prescription,
            notes=notes
        )
        db.session.add(treatment)

        appointment.status = 'Completed'
        db.session.commit()

      
        return redirect(url_for('doctor.view_appointment'))

    return render_template('doctor/add_treatment.html',
                           appointment=appointment,
                           patient=patient,
                           patient_details=patient_details)
