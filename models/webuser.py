from models import db
from werkzeug.security import generate_password_hash, check_password_hash

class WebUser(db.Model):
    __tablename__ = 'webuser'

    email = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) 
    usertype = db.Column(db.String(1), nullable=False)  # 'a' = admin, 'd' = doctor, 'p' = patient
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<WebUser {self.email} type:{self.usertype}>"
