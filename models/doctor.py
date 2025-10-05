from models import db

class Doctor(db.Model):
    __tablename__ = 'doctor'
    doc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doc_email = db.Column(db.String(225), unique=True, nullable=False)
    doc_name = db.Column(db.String(225), nullable=False)
    doc_password = db.Column(db.String(225), nullable=False)
    doc_nic = db.Column(db.String(15), nullable=True)
    doc_tel = db.Column(db.String(15), nullable=True)
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialities.id'), nullable=True)

    appointments = db.relationship('Appointment', backref='doctor', lazy=True, cascade='all, delete-orphan')
    schedules = db.relationship('DocSchedule', backref='doctor', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Doctor {self.doc_name} ({self.doc_email})>"
