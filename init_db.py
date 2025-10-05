from app import create_app
from models import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Tables dropped and recreated successfully")

