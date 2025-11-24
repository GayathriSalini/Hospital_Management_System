from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from models import Specialities, Doctor, db, Patient
from werkzeug.security import generate_password_hash
from . import admin_bp
from datetime import datetime
from flask_login import login_required, current_user
from app.forms import AddPateintForm

@admin_bp.route('/add_patient', methods=['GET','POST'])
@login_required 
def add_patient():
    if getattr(current_user, 'a_email', None) != 'admin@nhshospital.com':
        flash("Don't have permission","danger")
        return redirect(url_for('auth.login'))
    
    form = AddPateintForm()
    
    if form.validate_on_submit():
      try: 
        
        hashed_password = generate_password_hash(form.p_password.data)
        
        new_patient = Patient (
            p_name = form.p_name.data,
            p_email = form.p_email.data,
            p_password = hashed_password,
            p_address = form.p_address.data,
            p_dob = form.p_dob.data,
            p_tel = form.p_tel.data
        )
         
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
      except Exception as e:
            db.session.rollback()
            flash("Error: Enter details Again","danger")
            return redirect(url_for('admin.add_patient'))
           
    return render_template('/admin/add_patient.html',form=form)