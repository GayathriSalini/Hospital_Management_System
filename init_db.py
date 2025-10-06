from app import create_app
from models import db
from sqlalchemy import text
 

app = create_app()

with app.app_context():
    result = db.session.execute(text("PRAGMA foreign_keys")).fetchone()
    print("Foreign keys enforcement:", result[0])
    
    db.drop_all()
    print("Tables dropped successfully")

    
    db.create_all()
    print("Tables created successfully")
