from .main_routes import main_bp
from .auth_routes import auth_bp 
from .patient.dashboard import patient_bp
from app.routes.admin import admin_bp
from .doctor.dashboard import doctor_bp


def register_routes(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(admin_bp)
    
    