from app import db
from datetime import datetime
 # Import the db instance

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True) 

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
    def get_id(self):
        return str(self.id)
    
    def is_authenticated(self):
        return True  # Assuming all users are authenticated
    
    def is_active(self):
        return True  # Assuming all users are active

    def is_anonymous(self):
        return False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    classification = db.Column(db.String(20), nullable=True)  # New column for classification status
    is_important = db.Column(db.Boolean, default=False)  # Check if this column is defined correctly
    is_archived = db.Column(db.Boolean, default=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'), nullable=True)
    folder = db.relationship('Folder', backref=db.backref('emails', lazy=True))

    def __repr__(self):
        return f"Email('{self.sender}', '{self.subject}')"

class Folder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Folder('{self.name}')"
    
class Blacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # Type of blacklisted item (e.g., email, domain)
    value = db.Column(db.String(255), nullable=False)  # Value of the blacklisted item (e.g., email address, domain)

    def __repr__(self):
        return f"Blacklist('{self.type}', '{self.value}')"