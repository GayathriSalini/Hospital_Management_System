from flask import redirect, url_for, flash, request
from models import Appointment, db
from . import admin_bp
from flask_login import login_required, current_user


@admin_bp.route('/cancel_appointment/<int:appo_id>', methods=['GET','POST'])
@login_required
def cancel_appointment(appo_id):
   
    if not hasattr(current_user, 'a_email') or current_user.a_email != "admin@nhshospital.com":
        return redirect(url_for('auth.login'))

    appointment = Appointment.query.get_or_404(appo_id)



    appointment.status = 'Cancelled'
    db.session.commit()
    

   
    return redirect(url_for('admin.list_appointments'))
