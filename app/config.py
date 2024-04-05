
# config.py

SQLALCHEMY_DATABASE_URI = 'mysql://scs_dev:scs_dev_pwd@localhost/scs'  # For MySQL
# OR
# SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/database_name'  # For PostgreSQL
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'your_secret_key'  # Replace with a strong and random secret key

