from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from models import Specialities, Doctor, db
from werkzeug.security import generate_password_hash
from . import admin_bp
from flask_login import login_required, current_user

@admin_bp.route('/add_doctor', methods=['GET', 'POST'])
@login_required
def add_doctor():
    if getattr(current_user, 'a_email', None) != 'admin@nhshospital.com':
        return redirect(url_for('auth.login'))
    
    specialties = Specialities.query.all()
    
    
    if request.method == 'POST':
        doc_name = request.form.get('doc_name')
        doc_email = request.form.get('doc_email')
        password = request.form.get('doc_password')
        doc_password = generate_password_hash(password)
        doc_nic = request.form.get('doc_nic')
        doc_tel = request.form.get('doc_tel')
        specialty_id = request.form.get('specialty_id')
        
        if Doctor.query.filter_by(doc_email=doc_email).first():
            flash("Doctor with this email already exists", "danger")
            return redirect(url_for('admin.add_doctor'))
        
        new_doc = Doctor(
            doc_name=doc_name,
            doc_email=doc_email,
            doc_password=doc_password,
            doc_nic = doc_nic,
            doc_tel = doc_tel,
            specialty_id=specialty_id,
        )
        
        db.session.add(new_doc)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/add_doctor.html', specialties=specialties)
