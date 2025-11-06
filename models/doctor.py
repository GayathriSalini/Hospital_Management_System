from werkzeug.security import generate_password_hash
from models import db
from flask_login import UserMixin

class Doctor(db.Model, UserMixin):
    __tablename__ = 'doctor'
    doc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doc_email = db.Column(db.String(225), unique=True, nullable=False)
    doc_name = db.Column(db.String(225), nullable=False)
    doc_password = db.Column(db.String(225), nullable=False)
    doc_nic = db.Column(db.String(15), nullable=True)
    doc_tel = db.Column(db.String(15), nullable=True)
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialities.id', ondelete='CASCADE'), nullable=True)

 
    appointments = db.relationship(
        'Appointment',
        back_populates='doctor',
        cascade='all, delete-orphan'
    )

    schedules = db.relationship(
        'DocSchedule',
        back_populates='doctor',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    

    def __repr__(self):
        return f"<Doctor {self.doc_name} ({self.doc_email})>"

    def get_id(self):
        return str(self.doc_id)