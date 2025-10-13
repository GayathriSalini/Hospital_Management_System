from models import db

class Treatment(db.Model):
    __tablename__ = 'treatment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_id = db.Column(
        db.Integer,
        db.ForeignKey('appointment.appo_id', ondelete='CASCADE'),
        nullable=False
    )
    diagnosis = db.Column(db.String(255), nullable=True)
    prescription = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    appointment = db.relationship(
        'Appointment',
        back_populates='treatment'
    )

    def __repr__(self):
        return f"<Treatment for appointment {self.appointment_id}>"

