from .main_routes import main_bp
from .auth_routes import auth_bp
from .patient.dashboard import patient_bp
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

from .doctor.dashboard import doctor_bp

def register_routes(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(admin_bp)
