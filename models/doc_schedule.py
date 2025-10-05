from models import db  
from datetime import date, time

class DocSchedule(db.Model):
    __tablename__= 'schedule'
    
    schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('doctor.doc_id'), nullable=False)
    title = db.Column(db.String(255), nullable=True)
    schedule_date = db.Column(db.Date, nullable=False)    
    schedule_time = db.Column(db.Time, nullable=True)    
    nop = db.Column(db.Integer, nullable=True)

    doctor = db.relationship('Doctor', backref='schedules', lazy=True)
    
    def __repr__(self):
        return f"<DocSchedule {self.schedule_id} Doctor:{self.doc_id} Date:{self.schedule_date}, Time:{self.schedule_time}>"
