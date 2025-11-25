from flask import render_template, redirect, url_for
from . import admin_bp
from models import Doctor , Specialities 
from flask_login import login_required, current_user
from app.extensions import csrf


@csrf.exempt
@admin_bp.route('/doctors', methods=['GET', 'POST'])
@login_required
def doctors_list():
    if not hasattr(current_user, 'a_email') or current_user.a_email != "admin@nhshospital.com":
        return redirect(url_for('auth.login'))
    
    
    doctors = Doctor.query.all()
    specialities = Specialities.query.all()
    return render_template('admin/doctors_list.html', doctors=doctors, specialities = specialities)
