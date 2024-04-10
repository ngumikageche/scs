import unittest
from app import app, db
from app.models import User, Email, Folder, Blacklist
from datetime import datetime

class TestModels(unittest.TestCase):

    def setUp(self):
        # Establish the application context
        self.app_context = app.app_context()
        self.app_context.push()

        # Create the tables
        db.create_all()

    def tearDown(self):
        # Remove the database after testing
        db.session.remove()

        # Pop the application context
        self.app_context.pop()

    def test_user_creation(self):
        # Test creating a user
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()

        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'testuser')
        self.assertEqual(User.query.first().email, 'test@example.com')

    def test_email_creation(self):
        # Test creating an email
        email = Email(sender='sender@example.com', subject='Test Subject', content='Test Content', classification='Test Classification')
        db.session.add(email)
        db.session.commit()

        self.assertEqual(Email.query.count(), 1)
        self.assertEqual(Email.query.first().sender, 'sender@example.com')
        self.assertEqual(Email.query.first().subject, 'Test Subject')

    def test_folder_creation(self):
        # Test creating a folder
        folder = Folder(name='Test Folder')
        db.session.add(folder)
        db.session.commit()

        self.assertEqual(Folder.query.count(), 1)
        self.assertEqual(Folder.query.first().name, 'Test Folder')

    def test_blacklist_creation(self):
        # Test creating a blacklist entry
        blacklist = Blacklist(type='email', value='test@example.com')
        db.session.add(blacklist)
        db.session.commit()

        self.assertEqual(Blacklist.query.count(), 1)
        self.assertEqual(Blacklist.query.first().type, 'email')
        self.assertEqual(Blacklist.query.first().value, 'test@example.com')

if __name__ == '__main__':
    unittest.main()
