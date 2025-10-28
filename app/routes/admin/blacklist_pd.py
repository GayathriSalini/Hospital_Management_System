from flask import render_template, url_for, flash, request, redirect
from . import admin_bp
from models import db, Patient, Doctor

@admin_bp.route('/blacklist_search', methods=['GET'])
def blacklist_search():
    search_type = request.args.get('search_type', 'patient')
    query = request.args.get('query', '').strip()

    patients = []
    doctors = []

    if search_type == 'patient' and query:
        patients = Patient.query.filter(
            (Patient.p_name.ilike(f"%{query}%")) |
            (Patient.p_id.ilike(f"%{query}%")) |
            (Patient.p_tel.ilike(f"%{query}%"))
        ).all()

    elif search_type == 'doctor' and query:
        doctors = Doctor.query.filter(
            (Doctor.doc_id.ilike(f"%{query}%")) |
            (Doctor.doc_name.ilike(f"%{query}%")) |
            (Doctor.doc_email.ilike(f"%{query}%"))
        ).all()

    return render_template('admin/blacklist_pd.html', search_type=search_type, query=query, patients=patients, doctors=doctors)


@admin_bp.route('/blacklist/<user_type>/<int:user_id>', methods=['POST'])
def delete_pd(user_type, user_id):
    if user_type == 'patient':
        user = Patient.query.get(user_id)
    elif user_type == 'doctor':
        user = Doctor.query.get(user_id)
    else:
        flash('Invalid user type.', 'danger')
        return redirect(url_for('admin.blacklist_search'))

    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f'{user_type.capitalize()} deleted successfully.', 'success')
    else:
        flash(f'{user_type.capitalize()} not found.', 'danger')

    return redirect(url_for('admin.blacklist_search'))
