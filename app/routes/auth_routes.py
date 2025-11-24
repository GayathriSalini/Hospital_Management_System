from flask import Blueprint,session, render_template, url_for, flash, request, redirect
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Patient, Doctor, Admin
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import PatientRegisterForm, PatientLoginForm, DoctorLoginForm, AdminLoginForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    active_tab = request.args.get('active_tab') or 'patient'
    patient_form = PatientLoginForm(prefix='patient')
    doctor_form = DoctorLoginForm(prefix='doctor')
    admin_form = AdminLoginForm(prefix="admin")
    
    if active_tab== 'patient' and patient_form.validate_on_submit():
        user = Patient.query.filter_by(p_email=patient_form.email.data).first()
        if user and check_password_hash(user.p_password, patient_form.password.data):
            login_user(user)
            return redirect(url_for('patient.dashboard'))
        flash("Invalid email or password", 'danger')
        
       
    elif active_tab== 'doctor' and doctor_form.validate_on_submit():
        user = Doctor.query.filter_by(doc_email=doctor_form.email.data).first()
        if user and check_password_hash(user.doc_password, doctor_form.password.data):
            login_user(user)
            return redirect(url_for('doctor.dashboard'))
        flash("Invalid email or password", 'danger') 
        
    elif active_tab== 'admin' and admin_form.validate_on_submit():
        user = Admin.query.filter_by(a_email=admin_form.email.data).first()
        if user and check_password_hash(user.a_password, admin_form.password.data):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        flash("Invalid email or password", 'danger') 
            
            
    return render_template(
        'auth/login.html',
        active_tab=active_tab,
        patient_form=patient_form,
        doctor_form=doctor_form,
        admin_form=admin_form
    )



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = PatientRegisterForm()
    if form.validate_on_submit():
    
          hashed_password = generate_password_hash(form.p_password.data)

          new_patient = Patient(
               p_name=form.p_name.data,
               p_email=form.p_email.data,
              p_password=hashed_password,
              p_address=form.p_address.data,
              p_dob=form.p_dob.data,
              p_tel=form.p_tel.data
           )
  
          try:
              db.session.add(new_patient)
              db.session.commit()
              return redirect(url_for('auth.login'))
          except Exception as e:
              db.session.rollback()
              flash("Error: Enter details Again", "danger")
              return redirect(url_for('auth.register'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))
