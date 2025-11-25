from flask import render_template, request, redirect, url_for
from . import admin_bp
from models import Patient, Doctor, Specialities, db
from flask_login import login_required, current_user
from app.extensions import csrf


@csrf.exempt
@admin_bp.route('/admin_search', methods=['GET'])
@login_required
def admin_search():

    if not hasattr(current_user, 'a_email') or current_user.a_email != "admin@nhshospital.com":
        return redirect(url_for('auth.login'))

    search_type = request.args.get('search_type', 'patient')
    query = request.args.get('query', '').strip()
    doctor_search_by = request.args.get('doctor_search_by', 'name')

    patients = []
    doctors = []
    speciality_selected = None

    specialties_list = Specialities.query.order_by(Specialities.s_name).all()
 
    if query:
        if search_type == 'patient':
          
            if query.isdigit():
                patients = Patient.query.filter(Patient.p_id == int(query)).all()
            else:
                patients = Patient.query.filter(
                    (Patient.p_name.ilike(f'%{query}%')) |
                    (Patient.p_tel.ilike(f'%{query}%'))
                ).all()
                

        elif search_type == 'doctor':
    
            if doctor_search_by == 'name':
                doctors = Doctor.query.filter(Doctor.doc_name.ilike(f"%{query}%")).all()
            elif doctor_search_by == 'id':
                doctors = Doctor.query.filter(Doctor.doc_id == int(query)).all()
            elif doctor_search_by == 'specialty':
       
                try:
                    speciality_id = int(query)
                    speciality_selected = Specialities.query.get(speciality_id)
                    if speciality_selected:
                        doctors = Doctor.query.filter_by(specialty_id=speciality_id).all()
                    else:
                        doctors = []
                except ValueError:
                    doctors = []

    return render_template(
        'admin/search_pd.html',
        search_type=search_type,
        query=query,
        doctor_search_by=doctor_search_by,
        patients=patients,
        doctors=doctors,
        specialties_list=specialties_list,
        speciality_selected=speciality_selected
    )
