from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from models import Specialities, Doctor, db, Patient
from werkzeug.security import generate_password_hash
from . import admin_bp
from datetime import datetime
from flask_login import login_required, current_user

@admin_bp.route('/add_patient', methods=['GET','POST'])
@login_required 
def add_patient():
    if getattr(current_user, 'a_email', None) != 'admin@nhshospital.com':
        flash("Don't have permission","danger")
        return redirect(url_for('auth.login'))
    
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
            flash('Invalid date format for DOB ')
            return redirect(url_for('admin.add_patient'))
        
        hashed_password = generate_password_hash(p_password)
        
        new_patient = Patient (
            p_name = p_name,
            p_email = p_email,
            p_password = hashed_password,
            p_address = p_address,
            p_dob = p_dob,
            p_tel = p_tel
        )
        
        try : 
            db.session.add(new_patient)
            db.session.commit()
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash("Error: Enter details Again","danger")
            """ flash(f'Error: {str(e)}') """
            return redirect(url_for('admin.add_patient'))
           
    return render_template('/admin/add_patient.html')