from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models import Appointment, db
from datetime import datetime
from . import patient_bp
from flask_login import login_required, current_user
from app.extensions import csrf

@csrf.exempt
@patient_bp.route('/edit_appointment/<int:appo_id>', methods=['GET', 'POST'])
@login_required
def edit_appointment(appo_id):
    patient_id = current_user.p_id
    if not patient_id:
        
        flash('Please login to edit appointment', 'error')
        return redirect(url_for('auth.login'))

    appointment =  Appointment.query.get_or_404(appo_id)
    if appointment.p_id != patient_id:
        flash('Unauthorized access to edit this appointment', 'error')
        
        return redirect(url_for('patient.dashboard'))

    if request.method == 'POST':
        date_str = request.form.get('appo_date')
        
        time_str = request.form.get('appo_time')
        status = request.form.get('status')

        try:
            new_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            new_time = datetime.strptime(time_str, '%H:%M').time()
        except Exception:
            flash('Invalid date or time format', 'error')
            return redirect(url_for('patient.edit_appointment', appo_id=appo_id))

     
        appointment.appo_date = new_date
        
        appointment.appo_time = new_time
        appointment.status = status
        db.session.commit()

        flash('Appointment updated successfully', 'success')
        return redirect(url_for('patient.dashboard'))


    return render_template('patient/edit_appointment.html', appointment=appointment)
