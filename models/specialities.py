from models import db

class Specialities(db.Model):
    __tablename__ = 'specialities'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    s_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    doctors = db.relationship('Doctor', backref='speciality', lazy=True)

    def __repr__(self):
        return f"<Speciality {self.s_name}>"


