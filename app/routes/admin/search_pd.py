from flask import render_template, request
from . import admin_bp
from models import Patient , db, Doctor, Specialities


@admin_bp.route('/admin_search', methods = ['GET'])
def admin_search():
    search_type = request.args.get('search_type', 'patient')
    query = request.args.get('query','')
    
    patients = []
    patient = None
    doctors = [] 
    
    if query:
      if search_type == 'patient':
          patients = Patient.query.filter(
                (Patient.p_name.ilike(f"%{query}%")) |
                (Patient.p_id.ilike(f"%{query}%")) |
                (Patient.p_tel.ilike(f"%{query}%"))
            ).all()
          
          if len(patients) == 1:
              patient = patients[0]
          
      else:
          doctors = db.session.query(Doctor, Specialities).join(Specialities).filter(
                (Doctor.doc_name.ilike(f"%{query}%")) |
                (Specialities.s_name.ilike(f"%{query}%")) |
                (Doctor.doc_email.ilike(f"%{query}%"))
           ).all()
           
          
    return render_template(
        'admin/search_pd.html',search_type=search_type, query= query,patient=patient, patients=patients, doctors=doctors
    )