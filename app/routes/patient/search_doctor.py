from flask import Blueprint, request, render_template
from models import Doctor, Specialities
from . import patient_bp
from flask_login import login_required, current_user

@patient_bp.route('/search_doctor', methods=['GET'])
@login_required
def search_doctor():
    search_by = request.args.get('search_by', 'name')
    query = request.args.get('query', '').strip()
    
  
    specialities_list = Specialities.query.order_by(Specialities.s_name).all()
    doctors = []
    speciality_selected = None

    if query:
        if search_by == 'name':
            doctors = Doctor.query.filter(Doctor.doc_name.ilike(f'%{query}%')).all()
        elif search_by == 'speciality':
            try:
                speciality_id = int(query)
                speciality_selected = Specialities.query.get(speciality_id)
                if speciality_selected:
                    doctors = Doctor.query.filter_by(specialty_id=speciality_id).all()
            except ValueError:
                doctors = []
        else:
            doctors = []

    return render_template(
        'patient/search_doctor_book.html',
        doctors=doctors,
        search_by=search_by,
        query=query,
        specialities_list=specialities_list,
        speciality_selected=speciality_selected
    )
