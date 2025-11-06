from models import db
from datetime import date, time 
from flask_login import UserMixin

class Patient(db.Model, UserMixin):
    __tablename__ = 'patient'
    p_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    p_email = db.Column(db.String(225), unique=True, nullable=False)
    p_name = db.Column(db.String(225), nullable=False)
    p_password = db.Column(db.String(225), nullable=False)
    p_address = db.Column(db.String(225), nullable=False)
    p_dob = db.Column(db.Date, nullable=False)
    p_tel = db.Column(db.String(15), nullable=True)

    
    appointments = db.relationship(
        'Appointment',
        back_populates='patient',
        cascade='all, delete-orphan'
    )
    
    details = db.relationship(
        'PatientDetails',
        uselist=False,
        back_populates='patient',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<Patient {self.p_name} ({self.p_email})>"


    def get_id(self):
        return str(self.p_id)