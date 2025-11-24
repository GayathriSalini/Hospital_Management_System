from flask import redirect, url_for, flash, session 
from models import Appointment, db
from . import patient_bp
from flask_login import login_required, current_user

@patient_bp.route('/cancel_appointment/<int:appo_id>', methods=['POST'])
@login_required
def cancel_appointment(appo_id):
    patient_id = current_user.p_id
    if not patient_id :
        flash('Please login to cancel appointment', 'error')
        return redirect(url_for('auth.login'))
    
    appointment = Appointment.query.get_or_404(appo_id)
    
    if appointment.p_id != patient_id:
        flash('You are not authorized to cancel this appointment', 'error')
        return redirect(url_for('patient.dashboard'))
    
    
    appointment.status = 'Cancelled'
    db.session.commit()
   
    
    return redirect(url_for('patient.dashboard'))