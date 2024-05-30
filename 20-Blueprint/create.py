
from app import create_app, db
from models.user import User

app = create_app()

with app.app_context():
    db.create_all()
    print("Database created!")