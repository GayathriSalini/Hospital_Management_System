import os
from flask import Flask
from sqlalchemy import event
from sqlalchemy.engine import Engine
from models import db, Admin
from app.routes import register_routes
from werkzeug.security import generate_password_hash


def create_app():
    app = Flask(__name__,template_folder='templates',static_folder='static')

    
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

  
    db_path = os.path.join(base_dir, 'hospital_data.sqlite3')
    print("DB path:", db_path)
    
   
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-very-secret-key'

    db.init_app(app)
    register_routes(app)

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return app

def create_default_admin():
    admin_email = "admin@nhshospital.com"
    admin_password = "admin@NHShospital"
    
    if not Admin.query.filter_by(a_email = admin_email).first():
        admin = Admin(a_email = admin_email)
        admin.a_password = generate_password_hash(admin_password)
        db.session.add(admin)
        db.session.commit()
        print("default admin user created")
    else:
        print("admin already exists")