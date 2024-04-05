from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the Flask application instance
app = Flask(__name__)

# Load configuration from config.py
app.config.from_pyfile('config.py')

# Initialize the SQLAlchemy extension with the Flask application instance
db = SQLAlchemy(app)

# Import routes after creating the Flask app instance
from app import routes
