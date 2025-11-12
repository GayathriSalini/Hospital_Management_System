from flask import render_template, redirect , url_for
from . import admin_bp
from models import Patient
from flask_login import login_required, current_user


@admin_bp.route('/patients', methods=['GET', 'POST'])
@login_required
def patients_list():
    if not hasattr(current_user, 'a_email') or current_user.a_email != "admin@nhshospital.com":
     
        return redirect(url_for('auth.login'))
    patients = Patient.query.all()
    return render_template('admin/patients_list.html', patients=patients)
