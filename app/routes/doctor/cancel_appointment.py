from flask import redirect, url_for, flash, session 
from models import Appointment, db
from . import doctor_bp
from flask_login import login_required, current_user

@doctor_bp.route('/cancel_appointment/<int:appo_id>', methods=['POST'])
@login_required
def cancel_appointment(appo_id):
    doctor_id = current_user.doc_id
    if not doctor_id :
        flash('Please login to cancel appointment', 'danger')
        return redirect(url_for('auth.login'))
    
    appointment = Appointment.query.get_or_404(appo_id)
    
    if appointment.doc_id != doctor_id:
        flash('You are not authorized to cancel this appointment', 'error')
        return redirect(url_for('doctor.dashboard'))
    
    
    appointment.status = 'Cancelled'
    db.session.commit()
    flash('Appointment cancelled successfully', 'success')
    
    return redirect(url_for('doctor.dashboard'))