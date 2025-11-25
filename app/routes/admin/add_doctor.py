from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from models import Specialities, Doctor, db
from werkzeug.security import generate_password_hash
from . import admin_bp
from flask_login import login_required, current_user
from app.forms import AddDoctorForm
    

@admin_bp.route('/add_doctor', methods=['GET', 'POST'])
@login_required
def add_doctor():
    if getattr(current_user, 'a_email', None) != 'admin@nhshospital.com':
        return redirect(url_for('auth.login'))
    
    specialties = Specialities.query.all()
    form = AddDoctorForm()
    form.specialty_id.choices = [(s.id, s.s_name) for s in specialties]
    
    if form.validate_on_submit():
        if Doctor.query.filter_by(doc_email=form.doc_email.data).first():
            flash("Doctor with this email already exists", "danger")
            return redirect(url_for('admin.add_doctor'))
        new_doc = Doctor(
            doc_name=form.doc_name.data,
            doc_email=form.doc_email.data,
            doc_password=generate_password_hash(form.doc_password.data),
            doc_nic=form.doc_nic.data,
            doc_tel=form.doc_tel.data,
            specialty_id=form.specialty_id.data
        )
        db.session.add(new_doc)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_doctor.html', form=form)