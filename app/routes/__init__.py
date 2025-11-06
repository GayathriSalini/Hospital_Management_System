from .main_routes import main_bp
from .auth_routes import auth_bp

from app.routes.admin import admin_bp
import app.routes.admin.dashboard 
import app.routes.admin.doctors_list
import app.routes.admin.patients_list
import app.routes.admin.add_doctor
import app.routes.admin.add_patient
import app.routes.admin.edit_doctor
import app.routes.admin.edit_patient
import app.routes.admin.blacklist_pd
import app.routes.admin.search_pd
import app.routes.admin.appointment

from app.routes.patient import patient_bp
import app.routes.patient.dashboard
import app.routes.patient.edit_data
import app.routes.patient.add_edit_medical
import app.routes.patient.search_doctor
import app.routes.patient.book_appoinment
import app.routes.patient.see_docAvalability
import app.routes.patient.cancel_appointment
import app.routes.patient.edit_appointment
import app.routes.patient.reschedule_appointment


from app.routes.doctor import doctor_bp
import app.routes.doctor.dashboard 
import app.routes.doctor.doc_avalability
import app.routes.doctor.search_patient
import app.routes.doctor.view_appointment
import app.routes.doctor.update_status
import app.routes.doctor.add_treatment


def register_routes(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(admin_bp)
