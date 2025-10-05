import os
from flask import Flask
from sqlalchemy import event
from sqlalchemy.engine import Engine
from models import db 

def create_app():
    app = Flask(__name__)

    os.makedirs('data', exist_ok=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/hospital_data.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return app
