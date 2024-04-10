from app import db, app
from app.models import User, Email, Folder
with app.app_context():
    db.create_all()
    print("Initialized")
