from flask import request, redirect, session, render_template , redirect, url_for, flash
from . import admin_bp 
from models import Doctor, db , Specialities
from werkzeug.security  import generate_password_hash, check_password_hash

@admin_bp.route('/doctors/edit/<int:doctor_id>', methods = ['GET', 'POST'])
def edit_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    specialties = Specialities.query.all()
    
    if request.method == 'POST':
        doctor.doc_name = request.form['doc_name']
        doctor.doc_email = request.form['doc_email']
        doctor.doc_tel = request.form['doc_tel']
        doctor.doc_nic = request.form['doc_nic']
        doctor.specialty_id = int(request.form['specialty_id'])        
        new_pw = request.form.get('new_password')
        
        if new_pw:
            doctor.password = generate_password_hash(new_pw)
        db.session.commit()
        return redirect(url_for('admin.doctors_list'))
    
    return render_template('admin/edit_doctor.html', doctor=doctor, specialties=specialties)
    