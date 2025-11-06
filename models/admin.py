from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from models import db 

class Admin(db.Model, UserMixin):
    __tablename__='admin'
    a_email= db.Column(db.String(225),primary_key=True,nullable=False,unique=True)
    a_password = db.Column(db.String(225), nullable=False)
        
    
    def __repr__(self):
        return f"<Admin {self.a_email}>"