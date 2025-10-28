from flask import render_template
from . import admin_bp
from models import Doctor , Specialities 

@admin_bp.route('/doctors', methods=['GET', 'POST'])
def doctors_list():
    doctors = Doctor.query.all()
    specialities = Specialities.query.all()
    return render_template('admin/doctors_list.html', doctors=doctors, specialities = specialities)
