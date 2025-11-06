from flask import Blueprint, render_template, url_for, flash, request, redirect
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Patient, Doctor, Admin
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        role = request.form.get('role')


        if role == "patient":
            email = request.form.get('p_email')
            password = request.form.get('p_password')
            user = Patient.query.filter_by(p_email=email).first()
            dashboard = 'patient.dashboard'

            if user and check_password_hash(user.p_password, password):
                login_user(user)
                return redirect(url_for(dashboard))
            else:
                flash("Invalid email or password", 'danger')
                return redirect(url_for('auth.login', active_tab=role))

        elif role == 'doctor':
            email = request.form.get('d_email')
            password = request.form.get("d_password")
            user = Doctor.query.filter_by(doc_email=email).first()
            dashboard = 'doctor.dashboard'

            if user and check_password_hash(user.doc_password, password):
                login_user(user)
                return redirect(url_for(dashboard))
            else:
                flash("Invalid email or password", 'danger')
                return redirect(url_for('auth.login', active_tab=role))

        elif role == 'admin':
            email = request.form.get('a_email')
            password = request.form.get('a_password')
            user = Admin.query.filter_by(a_email=email).first()
            dashboard = 'admin.dashboard'

            if user and check_password_hash(user.a_password, password):
                login_user(user)
                return redirect(url_for(dashboard))
            else:
                flash("Invalid email or password", "danger")
                return redirect(url_for('auth.login', active_tab=role))

        else:
            flash("Invalid role", 'danger')
            return redirect(url_for('auth.login', active_tab=role))

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        p_name = request.form['p_name']
        p_email = request.form['p_email']
        p_password = request.form['p_password']
        p_address = request.form['p_address']
        p_dob = request.form['p_dob']
        p_tel = request.form['p_tel']

        try:
            p_dob = datetime.strptime(p_dob, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format for DOB')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(p_password)

        new_patient = Patient(
            p_name=p_name,
            p_email=p_email,
            p_password=hashed_password,
            p_address=p_address,
            p_dob=p_dob,
            p_tel=p_tel
        )

        try:
            db.session.add(new_patient)
            db.session.commit()
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash("Error: Enter details Again", "danger")
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
