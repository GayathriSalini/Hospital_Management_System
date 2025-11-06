from flask import  render_template, request , redirect , url_for , flash
from models import Appointment, db, Patient
from datetime import date
from flask_login import login_required, current_user
from . import doctor_bp


@doctor_bp.route('/doctor/mark_status/<int:appo_id>/<string:status>', methods=['POST'])
@login_required
def mark_status(appo_id, status):
    appointment = Appointment.query.get_or_404(appo_id)

   
    if appointment.doc_id != current_user.doc_id:
        flash("Unauthorized action", "danger")
        return redirect(url_for('doctor.view_appointment'))

    if status in ['Completed', 'Cancelled']:
        appointment.status = status
        db.session.commit()
        flash(f"Appointment marked as {status}", "success")
    else:
        flash("Invalid status", "danger")

    return redirect(url_for('doctor.view_appointment'))