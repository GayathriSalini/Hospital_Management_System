import os
from flask import Flask
from sqlalchemy import event
from sqlalchemy.engine import Engine
from models import db


def create_app():
    app = Flask(__name__)

    # Get the root project directory (hospital_management_System)
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # Database path in the root folder
    db_path = os.path.join(base_dir, 'hospital_data.sqlite3')
    print("DB path:", db_path)

    # Flask config
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Enable foreign key constraints in SQLite
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return app
