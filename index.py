from flask import Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create a Blueprint for Page 1
index_bp = Blueprint('index_bp', __name__)

# Initialize a separate SQLAlchemy instance for Page 1
db = SQLAlchemy()

class SurveyResponseIndex(db.Model):
    __tablename__ = 'survey_response_index'
    # Use a string column for the primary key to allow alphanumeric IDs.
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # New columns for reference information
    ref_id = db.Column(db.String(50), nullable=True)
    ref_link = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    age = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    alarm_usage = db.Column(db.String(50), nullable=False)
    alarm_choice = db.Column(db.String(50), nullable=True)
    other_alarm = db.Column(db.String(255), nullable=True)

@index_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        ref_id_input = request.form.get('ref_id')  # Reference ID from user (optional)
        ref_link = request.form.get('ref_link')
        email = request.form.get('email')
        age = request.form.get('age')
        gender = request.form.get('gender')
        alarm_usage = request.form.get('alarmUsage')
        alarm_choice = request.form.get('alarmChoice')
        other_alarm = request.form.get('otherAlarm')

        # Check required fields: name, email, age, gender, and alarm_usage.
        if not all([name, email, age, gender, alarm_usage]):
            return "Error: Name, Email, Age, Gender, and Alarm Usage are required!", 400

        # Determine the final_id.
        # If a reference ID is provided, use it. Otherwise, auto-generate a new numeric ID.
        if ref_id_input and ref_id_input.strip():
            final_id = ref_id_input.strip()
            ref_id_value = final_id
        else:
            # Auto-generate the new ID by considering only existing numeric IDs.
            all_records = SurveyResponseIndex.query.all()
            numeric_ids = [int(record.id) for record in all_records if record.id.isdigit()]
            if numeric_ids:
                new_numeric_id = max(numeric_ids) + 1
            else:
                new_numeric_id = 1
            final_id = str(new_numeric_id)
            ref_id_value = final_id

        # Check for uniqueness of the final_id
        if SurveyResponseIndex.query.get(final_id):
            return "Error: This ID already exists. Please choose a different reference ID.", 400

        # Create a new response with the chosen ID
        new_response = SurveyResponseIndex(
            id=final_id,
            name=name,
            ref_id=ref_id_value,
            ref_link=ref_link,
            email=email,
            age=age,
            gender=gender,
            alarm_usage=alarm_usage,
            alarm_choice=alarm_choice,
            other_alarm=other_alarm
        )

        db.session.add(new_response)
        db.session.commit()
        print("Page 1 response saved!")
        return redirect(url_for('index_bp.responses'))
    
    return render_template('index.html')

@index_bp.route('/responses')
def responses():
    responses = SurveyResponseIndex.query.all()
    return render_template('response1.html', responses=responses)
