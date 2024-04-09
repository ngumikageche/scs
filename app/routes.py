from flask import render_template, jsonify, request, redirect, url_for, flash
from app import app, db
from app.models import User
from app.models import Folder
from app.models import Email
from app.models import Blacklist
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Placeholder data (replace with actual backend logic)
mails = []
blacklist = []
whitelist = []
marked_emails = []
blacklist = []
screening_list = []
# Render templates...
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/mail_filtering')
def mail_filtering():
    emails = Email.query.all()
    return render_template('mail_filtering.html', emails=emails)

@app.route('/mail_screening')
def mail_screening():
    return render_template('mail_screening.html')

@app.route('/mail_marking')
def mail_marking():
    return render_template('mail_marking.html')

@app.route('/mail_archiving')
def mail_archiving():
    return render_template('mail_archiving.html')

@app.route('/user_management')
def user_management():
    return render_template('user_management.html')

@app.route('/emails')
def show_emails():
    emails = Email.query.all()  # Retrieve all emails from the database
    return render_template('emails.html', emails=emails)

@app.route('/blacklist')
def view_blacklist():
    blacklisted_items = Blacklist.query.all()
    return render_template('blacklist.html', blacklisted_items=blacklisted_items)

# Backend API endpoints
@app.route('/api/user/add', methods=['POST'])
def add_user():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        if username and email:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({'error': 'User with this email already exists'}), 400
            new_user = User(username=username, email=email)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User added successfully'}), 201
        else:
            return jsonify({'error': 'Missing username or email'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users')
def get_users():
    users = User.query.all()
    user_list = [{'username': user.username, 'email': user.email} for user in users]
    return jsonify(user_list)


# Initialize the trained classifier (same as before)
vectorizer = CountVectorizer()
classifier = MultinomialNB()
pipeline = Pipeline([('vectorizer', vectorizer), ('classifier', classifier)])

# Sample dataset of labeled emails (for demonstration purposes)
emails = [
    {"sender": "sender1@example.com", "subject": "Discount Offer", "content": "Get 50% off today!"},
    {"sender": "sender2@example.com", "subject": "Important Update", "content": "Please review the attached document."},
    {"sender": "spam@example.com", "subject": "You've won a prize!",
     "content": "Congratulations! You've won $1,000,000!"},
    {"sender": "sender3@example.com", "subject": "Meeting Reminder",
     "content": "Don't forget about our meeting tomorrow."},
    {"sender": "spam@example.com", "subject": "Limited Time Offer", "content": "Buy now and get a free gift!"},
]
labels = [0, 0, 1, 0, 1]
text_data = [email["subject"] + " " + email["content"] for email in emails]
pipeline.fit(text_data, labels)

@app.route('/add_email', methods=['POST'])
def add_email():
    if request.method == 'POST':
        sender = request.form['sender']
        subject = request.form['subject']
        content = request.form['content']

        # Create a new Email instance and add it to the database
        new_email = Email(
            sender=sender,
            subject=subject,
            content=content
        )
        db.session.add(new_email)
        db.session.commit()

        flash('Email added successfully!', 'success')  # Flash a success message

        return redirect(url_for('mail_filtering'))  # Redirect to the homepage after adding email
    return render_template('add_email.html')

email_filters = []
"""
add_email_filter(): 

"""

@app.route('/api/email/filter', methods=['POST'])
def add_email_filter():
    
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        if not email or not isinstance(email, str) or '@' not in email:
            return jsonify({'error': 'Invalid email address'}), 400
        email_filters.append(email)
        return jsonify({'message': 'Email filter added successfully.'}), 200
    else:
        return jsonify({'error': 'Method not allowed'}), 405

@app.route('/filter_email', methods=['POST'])
def filter_email():
    if request.method == 'POST':
        email_id = request.form['email_id']
        classification = request.form['classification']

        # Update the classification in the database for the selected email
        email = Email.query.get(email_id)
        if email:
            email.classification = classification
            db.session.commit()
            return jsonify({'message': 'Email classified successfully'})

        return jsonify({'error': 'Email not found'}), 404

    # Fetch emails from the database
    emails = Email.query.all()

    return render_template('mail_filtering.html', emails=emails)

@app.route('/classify_email', methods=['POST'])
def classify_email():
    email_id = request.form['email_id']
    classification = request.form['classification']

    # Update the classification in the database for the selected email
    email = Email.query.get(email_id)
    if email:
        email.classification = classification
        db.session.commit()
        flash('Email has been classified successfully', 'success')
        return redirect(url_for('mail_filtering'))  # Redirect to the mail filtering page after classification

    flash('Email not found', 'error')
    return redirect(url_for('mail_filtering'))




# Route to handle email classification requests
# @app.route('/api/email/classify', methods=['POST'])
# def classify_email():
#     data = request.json
#     email_subject = data.get('subject')
#     email_content = data.get('content')

#     # Combine subject and content into a single text
#     email_text = email_subject + " " + email_content

#     # Use the trained classifier to classify the email
#     classification = pipeline.predict([email_text])[0]

#     # Return the classification result as a JSON response
#     return jsonify({'classification': 'spam' if classification == 1 else 'not spam'})

# Route to add an email address/content to the screening list
@app.route('/api/screening/add', methods=['POST'])
def add_to_screening_list():
    data = request.json
    entry = data.get('entry')
    if entry:
        screening_list.append(entry)
        return jsonify({'message': 'Added to screening list successfully'}), 200
    else:
        return jsonify({'error': 'Missing entry'}), 400

# Route to remove an email address/content from the screening list
@app.route('/api/screening/remove', methods=['POST'])
def remove_from_screening_list():
    data = request.json
    entry = data.get('entry')
    if entry:
        if entry in screening_list:
            screening_list.remove(entry)
            return jsonify({'message': 'Removed from screening list successfully'}), 200
        else:
            return jsonify({'message': 'Entry not found in screening list'}), 404
    else:
        return jsonify({'error': 'Missing entry'}), 400

# Function to check if an email should be screened
def should_screen_email(email):
    for entry in screening_list:
        if entry in email["sender"] or entry in email["subject"] or entry in email["content"]:
            return True
    return False

# Route to handle incoming emails and perform screening
@app.route('/api/email/screen', methods=['POST'])
def screen_email():
    data = request.json
    email = {
        "sender": data.get('sender'),
        "subject": data.get('subject'),
        "content": data.get('content')
    }
    if should_screen_email(email):
        return jsonify({'message': 'Email screened and blocked'}), 200
    else:
        return jsonify({'message': 'Email not screened'}), 200

# Route to mark an email as important or with specific tags/colors
@app.route('/api/email/mark', methods=['POST'])
def mark_email():
    data = request.json
    email_id = data.get('email_id')
    mark_type = data.get('mark_type')  # e.g., important, tag color
    if email_id and mark_type:
        # Store marking information for the email
        marked_emails.append({'email_id': email_id, 'mark_type': mark_type})
        return jsonify({'message': 'Email marked successfully'}), 200
    else:
        return jsonify({'error': 'Missing email ID or mark type'}), 400
    


# Route to retrieve marked emails
@app.route('/api/emails/marked')
def get_marked_emails():
    return jsonify(marked_emails)
# Backend API endpoints
# Add routes for archiving emails
@app.route('/api/mail/archive', methods=['POST'])
def archive_mail():
    data = request.json
    mail_id = data.get('mail_id')
    folder_id = data.get('folder_id')
    if mail_id and folder_id:
        email = Email.query.get(mail_id)
        if email:
            folder = Folder.query.get(folder_id)
            if folder:
                email.folder_id = folder_id
                db.session.commit()
                return jsonify({'message': 'Mail archived successfully'}), 200
            else:
                return jsonify({'error': 'Folder not found'}), 404
        else:
            return jsonify({'error': 'Email not found'}), 404
    else:
        return jsonify({'error': 'Missing mail ID or folder ID'}), 400

@app.route('/api/mail/folder/<int:folder_id>', methods=['GET'])
def get_emails_in_folder(folder_id):
    folder = Folder.query.get(folder_id)
    if folder:
        emails = Email.query.filter_by(folder_id=folder_id).all()
        email_list = [{'id': email.id, 'subject': email.subject, 'content': email.content} for email in emails]
        return jsonify(email_list), 200
    else:
        return jsonify({'error': 'Folder not found'}), 404
# Blacklist management function
@app.route('/api/blacklist/add', methods=['POST'])
def add_to_blacklist():
    data = request.json
    email = data.get('email')  # Assuming the key in the JSON is 'email'
    
    if email:
        # Check if the email is already blacklisted
        existing_entry = Blacklist.query.filter_by(value=email).first()
        if existing_entry:
            return jsonify({'error': 'Email already exists in blacklist'}), 400
        
        # If not, add it to the blacklist
        new_blacklist_item = Blacklist(type='email', value=email)
        db.session.add(new_blacklist_item)
        db.session.commit()
        return jsonify({'message': 'Email added to blacklist successfully'}), 200
    else:
        return jsonify({'error': 'Missing email'}), 400
    
def is_blacklisted(blacklist_type, value):
    blacklisted_items = Blacklist.query.filter_by(type=blacklist_type).all()
    for item in blacklisted_items:
        if item.value == value:
            return True
    return False

def process_email(email):
    if is_blacklisted('email', email.sender):
        email.classification = 'spam'

@app.route('/api/blacklist/remove', methods=['POST'])
def remove_from_blacklist():
    # Implement blacklist removal logic here
    # Users can remove email addresses or content from the blacklist
    data = request.json
    entry = data.get('entry')
    if entry:
        if entry in blacklist:
            blacklist.remove(entry)
            return jsonify({'message': 'Removed from blacklist successfully'}), 200
        else:
            return jsonify({'message': 'Entry not found in blacklist'}), 404
    else:
        return jsonify({'error': 'Missing entry'}), 400
# Render templates...


# Other routes...

# Whitelist management function
@app.route('/api/whitelist/add', methods=['POST'])
def add_to_whitelist():
    data = request.json
    entry = data.get('entry')
    if entry:
        if entry not in whitelist:
            whitelist.append(entry)
            return jsonify({'message': 'Added to whitelist successfully'}), 200
        else:
            return jsonify({'message': 'Entry already exists in whitelist'}), 400
    else:
        return jsonify({'error': 'Missing entry'}), 400

@app.route('/api/whitelist/remove', methods=['POST'])
def remove_from_whitelist():
    data = request.json
    entry = data.get('entry')
    if entry:
        if entry in whitelist:
            whitelist.remove(entry)
            return jsonify({'message': 'Removed from whitelist successfully'}), 200
        else:
            return jsonify({'message': 'Entry not found in whitelist'}), 404
    else:
        return jsonify({'error': 'Missing entry'}), 400

