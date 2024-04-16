from app import db, app
from app.models import User, Email, Folder
with app.app_context():
    db.create_all()
    # Check if there are any existing users
    existing_user = User.query.first()
    if not existing_user:
        # If no users exist, create the first user as admin
        admin_user = User(username='admin', email='admin@example.com')
        admin_user.set_password('admin_password')
        admin_user.is_admin = True
        db.session.add(admin_user)
        db.session.commit()
    print("Initialized")
