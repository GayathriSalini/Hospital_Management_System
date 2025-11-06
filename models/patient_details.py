from models import db


class PatientDetails(db.Model):
    __tablename__ = 'patient_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.p_id'), unique=True, nullable=False)

    blood_group = db.Column(db.String(10), nullable=True)   
    height_cm = db.Column(db.Float, nullable=True)          
    weight_kg = db.Column(db.Float, nullable=True)           
    allergies = db.Column(db.Text, nullable=True)
    chronic_conditions = db.Column(db.Text, nullable=True)

    patient = db.relationship('Patient', back_populates='details')



