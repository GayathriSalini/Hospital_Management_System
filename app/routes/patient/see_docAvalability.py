from  flask import request , session, redirect, url_for, flash, render_template
from models import Patient, Doctor, DocSchedule, db
from . import patient_bp

@patient_bp.route('/doctor_availability/<int:doc_id>')
def doc_availability(doc_id):
    doctor = Doctor.query.get_or_404(doc_id)
    schedules = DocSchedule.query.filter_by(doc_id=doc_id).order_by(DocSchedule.schedule_date, DocSchedule.schedule_time).all()
    return render_template('patient/doc_availability.html', doctor=doctor, schedules=schedules)
