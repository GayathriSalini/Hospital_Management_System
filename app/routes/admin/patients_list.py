from flask import render_template
from . import admin_bp
from models import Patient

@admin_bp.route('/patients', methods=['GET', 'POST'])
def patients_list():
    patients = Patient.query.all()
    return render_template('admin/patients_list.html', patients=patients)
