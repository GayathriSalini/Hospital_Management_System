from models import db
from datetime import time, date

class Appointment(db.Model):
    __tablename__ = 'appointment'

    appo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    p_id = db.Column(db.Integer, db.ForeignKey('patient.p_id'), nullable=False)
    doc_id = db.Column(db.Integer, db.ForeignKey('doctor.doc_id', ondelete='CASCADE'))
    appo_date = db.Column(db.Date, nullable=False)
    appo_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Booked') 

    patient = db.relationship('Patient', backref='appointments', lazy=True)
    doctor = db.relationship('Doctor', backref='appointments', lazy=True)

    def __repr__(self):
        return f"<Appointment {self.appo_id} Doctor:{self.doc_id} Patient:{self.p_id} Date:{self.appo_date} Status:{self.status}>"
