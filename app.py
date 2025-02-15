from flask import Flask, render_template, request, redirect, url_for, flash,  send_from_directory
import pymysql
import re
from flask import session
import random
from flask import request, jsonify
import os 
from werkzeug.utils import secure_filename
import time
from flask import  abort
import sys
import traceback
import logging
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
import json

app = Flask(__name__)




# Define your upload folder path
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_UPLOADS'] = os.path.join(os.getcwd(), 'uploads')  # For storing uploads

# Create the folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])




app = Flask(__name__)
app.secret_key = 'mayank'
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])  # Required for flashing messages

# Database connection details
db_config = {
    'host': 'postgresql://appraisal_system_user:Eu9ywvu98jkaX7oINgYBvlBs7AGuEt3Z@dpg-cuo5egggph6c73dikkb0-a/appraisal_system',
    'user': 'root',
    'password': '123456',
    'database': 'appraisal_system'
    
}

# Function to connect to the database using PyMySQL
# Function to connect to the database using PyMySQL
def connect_to_database():
    try:
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],  # Ensure there's a comma here
           
        )
        print("Database connection successful!")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


# Route to serve home.html
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['userId']
        email_prefix = request.form['emailPrefix']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        role = request.form['role']
        department = request.form['department']

        # Construct the full email with the domain
        gmail = email_prefix + '@apsit.edu.in'

        # Validate User ID, Role, Department (all are compulsory)
        if not user_id or not role or not department:
            flash("User ID, Role, and Department are required fields!", "error")
            return redirect(url_for('register'))

        # Validate email is within @apsit.edu.in domain
        email_regex = r'^[a-zA-Z0-9._%+-]+@apsit\.edu\.in$'
        if not re.match(email_regex, gmail):
            flash("Please enter a valid APSIT email address!", "error")
            return redirect(url_for('register'))

        # Validate password and confirm password match
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('register'))

        

        # Temporarily store registration data in session
        session['register_data'] = {
            'user_id': user_id,
            'gmail': gmail,  # Storing full email address
            'password': password,
            'role': role,
            'department': department
        }

        # Redirect to details form to complete registration
        return redirect(url_for('details'))

    return render_template('signup.html')



@app.route('/details', methods=['GET', 'POST'])
def details():
    if 'register_data' not in session:
        flash("Please complete the registration form first.", "error")
        return redirect(url_for('register'))

    if request.method == 'POST':
        # Get the registration data from the session
        register_data = session.get('register_data')
        user_id = register_data['user_id']

        # Get details form data
        name = request.form['facultyName']
        designation = request.form['designation']
        doj = request.form['doj']
        dob = request.form['dob']
        qualifications = request.form['qualifications']
        experience = request.form['experience']

        # Validate form data
        if not name or not designation or not doj or not dob:
            flash("All fields are required!", "error")
            return redirect(url_for('details'))

        # Now store all data in the database (register + details)
        connection = connect_to_database()
        if connection is None:
            flash("Could not connect to the database.", "error")
            return redirect(url_for('details'))

        cursor = connection.cursor()

        try:
            query = """
            INSERT INTO users (userid, gmail, password, role, dept, name, designation, d_o_j, dob, edu_q, exp) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                register_data['user_id'], register_data['gmail'], register_data['password'], register_data['role'], 
                register_data['department'], name, designation, doj, dob, qualifications, experience
            ))
            connection.commit()
            flash("Registration successful!", "success")

            # Clear the session after successful registration
            session.pop('register_data', None)
        except Exception as e:
            print(f"Error inserting data into the database: {e}")
            flash(f"An error occurred while registering. Error: {str(e)}", "error")
        finally:
            cursor.close()
            connection.close()

        # Redirect to login or dashboard after successful registration
        return redirect(url_for('login'))

    return render_template('details.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Fetch the username part from the form input
        username = request.form['loginId']
        # Add the fixed domain to create the full email
        gmail = f"{username}@apsit.edu.in"
        password = request.form['password']

        # Connect to the database and check credentials
        connection = connect_to_database()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE gmail=%s AND password=%s",
                (gmail, password)
            )
            user = cursor.fetchone()  # Fetch the user details

        connection.close()

        if user:
            # Store user information in session
            session['user_id'] = user[0]  # Assuming user ID is the first column
            session['role'] = user[3]  # Assuming 'role' is the 4th column

            role = user[3]

            # Redirect based on user role
            if role == "Higher Authority":
                flash('Login successful! Redirecting to higher authority landing.', 'info')
                return redirect(url_for('highlanding'))
            elif role == "Faculty":
                flash('Login successful! Redirecting to instructions.', 'info')
                return redirect(url_for('landing'))
            elif role == "Principal":
                flash('Login successful! Redirecting to principal staff view.', 'info')
                return render_template('principlestaff.html')
        else:
            flash('Invalid credentials, please try again.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    # Clear the session to log out the user
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))



@app.route('/instructions')
def instructions():
    user_id = session.get('user_id')
    return render_template('instructions.html')

'''@app.route('/submit_academic_year', methods=['POST'])
def submit_academic_year():
    # Get the selected academic year from the form
    selected_academic_year = request.form['academicYear']
    user_id = session.get('user_id')

    # Connect to the database
    connection = connect_to_database()
    with connection.cursor() as cursor:
        # Fetch the department of the user from the users table
        cursor.execute("SELECT dept FROM users WHERE userid = %s", (user_id,))
        user_department = cursor.fetchone()

        if not user_department:
            return "Department not found for the user.", 400  # Error handling if department is not found
        else:
            department = user_department[0]  # Extract the department value

        # Check if the form for the selected academic year already exists for the user
        cursor.execute("SELECT form_id FROM acad_years WHERE user_id = %s AND acad_years = %s", 
                       (user_id, selected_academic_year))
        existing_form = cursor.fetchone()

        if existing_form:
            form_id = existing_form[0]
            
            # Delete related records from all relevant tables if the form already exists
            tables = [
                'certifications', 'contribution_to_society', 'copyright', 'department_act',
                'external_projects', 'feedback', 'form1_tot', 'form2_tot', 'form3_tot',
                'institute_act', 'mem_uni', 'resource_person', 'self_imp', 'students_feedback',
                'teaching_process', 'total'
            ]
            for table in tables:
                cursor.execute(f"DELETE FROM {table} WHERE form_id = %s", (form_id,))
            
            # Also delete from the acad_years table
            cursor.execute("DELETE FROM acad_years WHERE form_id = %s", (form_id,))
            connection.commit()

        else:
            # Generate a random 6-digit form ID (ensure uniqueness by checking the database)
            form_id = random.randint(100000, 999999)
            cursor.execute("SELECT COUNT(*) FROM acad_years WHERE form_id = %s", (form_id,))
            count = cursor.fetchone()[0]

            # Regenerate form ID if it already exists
            while count > 0:
                form_id = random.randint(100000, 999999)
                cursor.execute("SELECT COUNT(*) FROM acad_years WHERE form_id = %s", (form_id,))
                count = cursor.fetchone()[0]

            # Insert the new form ID and academic year into the acad_years table
            cursor.execute(
                "INSERT INTO acad_years (form_id, user_id, acad_years) VALUES (%s, %s, %s)",
                (form_id, user_id, selected_academic_year)
            )
            connection.commit()

    connection.close()

    # Redirect to the form page, passing the form ID and department
    return redirect(url_for('form_page', form_id=form_id, department=department))'''



@app.route('/submit_academic_year', methods=['POST'])
def submit_academic_year():
    selected_academic_year = request.form['academicYear']
    user_id = session.get('user_id')

    connection = connect_to_database()
    with connection.cursor() as cursor:
        cursor.execute("SELECT dept FROM users WHERE userid = %s", (user_id,))
        department = cursor.fetchone()

        if not department:
            return "Department not found for the user.", 400

        department = department[0]

        # Check if the form already exists for the user and academic year
        cursor.execute(
            "SELECT form_id FROM acad_years WHERE user_id = %s AND acad_years = %s",
            (user_id, selected_academic_year),
        )
        existing_form = cursor.fetchone()

        if existing_form:
            form_id = existing_form[0]

            # Fetch existing teaching process data
            cursor.execute(
                """
                SELECT semester, course_code, classes_scheduled, classes_held,
                       (classes_held / classes_scheduled) * 5 AS totalpoints
                FROM teaching_process WHERE form_id = %s
                """,
                (form_id,),
            )
            teaching_data = cursor.fetchall()

            # Fetch existing feedback data
            cursor.execute(
                """
                SELECT semester, course_code, total_points, points_obtained, uploads
                FROM students_feedback WHERE form_id = %s
                """,
                (form_id,),
            )
            feedback_data = cursor.fetchall()

        else:
            form_id = random.randint(100000, 999999)
            cursor.execute("SELECT COUNT(*) FROM acad_years WHERE form_id = %s", (form_id,))
            while cursor.fetchone()[0] > 0:
                form_id = random.randint(100000, 999999)

            cursor.execute(
                "INSERT INTO acad_years (form_id, user_id, acad_years) VALUES (%s, %s, %s)",
                (form_id, user_id, selected_academic_year),
            )
            connection.commit()
            teaching_data = []  # Empty data if form is new
            feedback_data = []

    connection.close()

    return render_template(
        'from.html',
        department=department,
        form_id=form_id,
        user_id=user_id,
        teaching_data=teaching_data,
        feedback_data=feedback_data,
    )




@app.route('/form/<int:form_id>')
def form_page(form_id):
    user_id = session.get('user_id')

    # Fetch the department again in case you need it or pass it through the URL
    department = request.args.get('department')

    # Render the template and pass form_id, user_id, and department
    return render_template('from.html', form_id=form_id, user_id=user_id, department=department)


@app.route('/save-form-data', methods=['POST'])
def save_form_data():
    conn = None
    cursor = None
    try:
        # Extract form data
        teaching_data = request.form.get('teachingData')
        form_id = request.form.get('formId')
        feedback_entries = request.form.getlist('feedback[]')

        # Convert teaching and feedback data to Python objects
        teaching_data = teaching_data and eval(teaching_data)
        feedback_entries = [eval(entry) for entry in feedback_entries]

        # Connect to the database
        conn = connect_to_database()
        cursor = conn.cursor()

        # Process teaching data
        for row in teaching_data:
            # Check if the course_code already exists for this form_id
            cursor.execute("""
                SELECT srno FROM teaching_process WHERE form_id = %s AND course_code = %s
            """, (form_id, row['course']))
            existing_row = cursor.fetchone()

            if existing_row:
                # Update the srno for the existing course_code
                cursor.execute("""
                    UPDATE teaching_process
                    SET srno = %s, semester = %s, classes_scheduled = %s, classes_held = %s, totalpoints = %s
                    WHERE form_id = %s AND course_code = %s
                """, (row['srno'], row['semester'], row['scheduled'], row['held'], row['points'], form_id, row['course']))
            else:
                # Insert new row if course_code does not exist
                cursor.execute("""
                    INSERT INTO teaching_process (form_id, srno, semester, course_code, classes_scheduled, classes_held, totalpoints)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (form_id, row['srno'], row['semester'], row['course'], row['scheduled'], row['held'], row['points']))

        # Process feedback data
        for index, entry in enumerate(feedback_entries):
            srno = entry['srno']
            semester = str(entry['semester'])
            course = entry['course']
            total_points = entry['totalPoints']
            points_obtained = entry['pointsObtained']

            # Handle file upload if available
            upload_path = None
            file_key = f'files[{index}]'
            file = request.files.get(file_key)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                upload_path = filepath

            # Check if the course_code already exists for this form_id
            cursor.execute("""
                SELECT srno FROM students_feedback WHERE form_id = %s AND course_code = %s
            """, (form_id, course))
            existing_feedback = cursor.fetchone()

            if existing_feedback:
                # Update the srno and other fields for the existing course_code
                cursor.execute("""
                    UPDATE students_feedback
                    SET srno = %s, semester = %s, total_points = %s, points_obtained = %s, uploads = %s
                    WHERE form_id = %s AND course_code = %s
                """, (srno, semester, total_points, points_obtained, upload_path, form_id, course))
            else:
                # Insert new row if course_code does not exist
                cursor.execute("""
                    INSERT INTO students_feedback (form_id, srno, semester, course_code, total_points, points_obtained, uploads)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (form_id, srno, semester, course, total_points, points_obtained, upload_path))

        # Commit the transaction
        conn.commit()
        print("Teaching Data:", teaching_data)
        print("Feedback Entries:", feedback_entries)
        return jsonify({'status': 'success', 'message': 'Data saved successfully!'})

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error: {e}")
        print("Teaching Data:", teaching_data)
        print("Feedback Entries:", feedback_entries)

        return jsonify({'status': 'error', 'message': 'An error occurred while saving data.'}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()




@app.route('/delete-teaching-row', methods=['POST'])
def delete_teaching_row():
    conn = None
    cursor = None
    try:
        srno = request.form.get('srno')
        form_id = request.form.get('form_id')
        if not srno or not form_id:
            return jsonify({'status': 'error', 'message': 'Sr. No. and Form ID are required'}), 400

        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM teaching_process WHERE srno = %s AND form_id = %s
        """, (srno, form_id))
        conn.commit()

        return jsonify({'status': 'success', 'message': f'Teaching row with Sr. No. {srno} and Form ID {form_id} deleted successfully.'})

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred while deleting the teaching row.'}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/delete-feedback-row', methods=['POST'])
def delete_feedback_row():
    conn = None
    cursor = None
    try:
        srno = request.form.get('srno')
        form_id = request.form.get('form_id')
        if not srno or not form_id:
            return jsonify({'status': 'error', 'message': 'Sr. No. and Form ID are required'}), 400

        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM students_feedback WHERE srno = %s AND form_id = %s
        """, (srno, form_id))
        conn.commit()

        return jsonify({'status': 'success', 'message': f'Feedback row with Sr. No. {srno} and Form ID {form_id} deleted successfully.'})

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred while deleting the feedback row.'}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/reset-form', methods=['POST'])
def reset_form():
    conn = None
    cursor = None
    try:
        # Extract form_id from request
        form_id = request.form.get('formId')
        if not form_id:
            return jsonify({'status': 'error', 'message': 'formId is required'}), 400

        # Connect to the database
        conn = connect_to_database()
        cursor = conn.cursor()

        # Delete all rows associated with the form_id from both tables
        cursor.execute("DELETE FROM teaching_process WHERE form_id = %s", (form_id,))
        cursor.execute("DELETE FROM students_feedback WHERE form_id = %s", (form_id,))

        # Commit changes
        conn.commit()

        return jsonify({'status': 'success', 'message': 'All rows reset successfully.'})

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred while resetting the form.'}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



@app.route('/save-total-points', methods=['POST'])
def save_total_point():
    try:
        data = request.get_json()
        form_id = data['form_id']
        total = data['total']
        teaching = data['teaching']
        feedback = data['feedback']

        connection = connect_to_database()
        cursor = connection.cursor()

        sql = """
            INSERT INTO form1_tot (form_id, total, teaching, feedback)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE total = VALUES(total), teaching = VALUES(teaching), feedback = VALUES(feedback)
        """
        cursor.execute(sql, (form_id, total, teaching, feedback))  # Include all four parameters

        connection.commit()

        return jsonify({"success": True, "message": "Total points saved successfully."})

    except Exception as e:
        connection.rollback()
        print(f"Error saving total points: {e}")
        return jsonify({"success": False, "message": "An error occurred while saving total points."}), 500

    finally:
        cursor.close()
        connection.close()


@app.route('/form2/<int:form_id>')
def form2_page(form_id):
    return render_template('form2.html', form_id=form_id)

# Upload parameters
UPLOAD_FOLDER = r'C:\Users\mayank salvi\Desktop\appraisal system\uploads'

ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Helper to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Helper function to check allowed extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

MAX_FILE_SIZE = 3 * 1024 * 1024  # 1 MB
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Allow up to 100 MB


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    files = request.files.getlist('file')  # Get all uploaded files
    uploaded_files = []

    for file in files:
        if file.filename == '':
            return jsonify({'error': 'No file selected for upload'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': f'Invalid file type for {file.filename}. Only PDF and DOCX are allowed.'}), 400

        # Check the file size
        if len(file.read()) > MAX_FILE_SIZE:
            return jsonify({'error': f'File {file.filename} exceeds the 1 MB limit.'}), 400
        file.seek(0)  # Reset file pointer after reading

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        uploaded_files.append(filename)

    return jsonify({'filenames': uploaded_files}), 200


@app.route('/save-form2-data', methods=['POST'])
def save_form2_data():
    print(f'Total request size: {sys.getsizeof(request.data)} bytes')
    
    form_id = request.form.get('formId')
    conn = connect_to_database()
    cursor = conn.cursor()

    print("Received form ID:", form_id)  # Debug: Print received form ID

    try:
        # Process Department Activities
        department_activities = []
        for key, value in request.form.items():
            if key.startswith('departmentActivities'):
                index = int(key.split('[')[1].split(']')[0])  # Extract index from field name
                while len(department_activities) <= index:
                    department_activities.append({})
                field_name = key.split(']')[1].strip('[').strip(']')
                department_activities[index][field_name] = value

        print("Department Activities:", department_activities)  # Debug: Print department activities

        # Process Institute Activities
        institute_activities = []
        for key, value in request.form.items():
            if key.startswith('instituteActivities'):
                index = int(key.split('[')[1].split(']')[0])
                while len(institute_activities) <= index:
                    institute_activities.append({})
                field_name = key.split(']')[1].strip('[').strip(']')
                institute_activities[index][field_name] = value

        print("Institute Activities:", institute_activities)  # Debug: Print institute activities

        # Save Department Activities with file uploads
        for i, activity in enumerate(department_activities):
            semester = activity.get('semester')
            activity_name = activity.get('activity')
            points = activity.get('points')
            order_copy = activity.get('orderCopy')
            file = request.files.get(f'departmentActivities[{i}][file]')

            print(f"Processing Department Activity {i}:", activity)  # Debug: Print each activity

            # Handle file upload if it exists
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)  # Save file to the uploads directory
                upload_path = filepath  # Store the full path in the database
            else:
                upload_path = None

            # Insert into the database
            cursor.execute(
                "INSERT INTO department_act (form_id, semester, activity, points, order_cpy, uploads) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (form_id, semester, activity_name, points, order_copy, upload_path)
            )
            print(f"Inserted into department_act: {form_id}, {semester}, {activity_name}, {points}, {order_copy}, {upload_path}")

        # Save Institute Activities with file uploads
        for i, activity in enumerate(institute_activities):
            semester = activity.get('semester')
            activity_name = activity.get('activity')
            points = activity.get('points')
            order_copy = activity.get('orderCopy')
            file = request.files.get(f'instituteActivities[{i}][file]')

            print(f"Processing Institute Activity {i}:", activity)  # Debug: Print each activity

            # Handle file upload if it exists
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                upload_path = filepath
            else:
                upload_path = None

            # Insert into the database
            cursor.execute(
                "INSERT INTO institute_act (form_id, semester, activity, points, order_cpy, uploads) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (form_id, semester, activity_name, points, order_copy, upload_path)
            )
            print(f"Inserted into institute_act: {form_id}, {semester}, {activity_name}, {points}, {order_copy}, {upload_path}")

        # Commit the changes
        conn.commit()
        return jsonify({'message': 'Form2 data saved successfully!'}), 200

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")  # Print the error for debugging
        return jsonify({'message': 'Error saving Form2 data.'}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/save-2total-points', methods=['POST'])
def save_2total_points():
    connection = None
    cursor = None
    try:
        data = request.get_json()
        form_id = data.get('form_id')
        total = data.get('total')
        dept = data.get('dept')
        institute = data.get('institute')

        print(f"Received data: form_id={form_id}, total={total}, dept={dept}, institute={institute}")

        if not form_id or total is None: 
            return jsonify({"success": False, "message": "Invalid form ID or total points."}), 400

        connection = connect_to_database()
        cursor = connection.cursor()

        sql = """
                INSERT INTO form2_tot (form_id, total, dept, institute)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE total = VALUES(total), dept = VALUES(dept), institute = VALUES(institute)
             """
        print(f"SQL Executing: {sql} with values {(form_id, total, dept, institute)}")
        cursor.execute(sql, (form_id, total, dept, institute))

        connection.commit()
        return jsonify({"success": True, "message": "Total points saved successfully."})

    except Exception as e:
        if connection: 
            connection.rollback()
        print(f"Error saving total points: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()




MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB limit


app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Utility to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route to handle form 3
@app.route('/form3/<int:form_id>', methods=['GET', 'POST'])
def form3_page(form_id):
    if request.method == 'POST':
        # Handle Self-Assessment Points
        points = request.form.get('selfAssessment')

        # File upload handling
        category = request.form.get('category')
        file = request.files.get('file')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if category == 'self-improvement':
                file.save(os.path.join(app.config['UPLOAD_FOLDER_UPLOADS'], filename))
                # Store in the database under doc1
                conn = connect_to_database()
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO acr (form_id, doc1, points) VALUES (%s, %s, %s)",
                        (form_id, filename, points)
                    )
                    conn.commit()
                conn.close()
                flash('Self-Improvement Initiatives file uploaded successfully.', 'success')
            elif category == 'representing-college':
                file.save(os.path.join(app.config['UPLOAD_FOLDER_UPLOADS'], filename))
                # Store in the database under doc2
                conn = connect_to_database()
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO acr (form_id, doc2, points) VALUES (%s, %s, %s)",
                        (form_id, filename, points)
                    )
                    conn.commit()
                conn.close()
                flash('Representing College in External Environment file uploaded successfully.', 'success')
        else:
            flash('Invalid file or file type. Only PDF or DOCX files under 1MB are allowed.', 'danger')

    return render_template('form3.html', form_id=form_id)


@app.route('/save-form3-data', methods=['POST'])
def save_form3_data():
    conn = cursor = None
    try:
        print("==> Starting /save-form3-data request...")

        # Debugging: Check request form and files data
        print("Request form data:", request.form)
        print("Request files:", request.files)

        # Retrieve formId
        form_id = request.form.get('formId')
        if not form_id:
            raise ValueError("Form ID is missing")
        print(f"Form ID: {form_id}")

        # Connect to the database
        conn = connect_to_database()
        cursor = conn.cursor()
        print("==> Connected to the database")

        # Process selfImprovementTable data
        self_improvement_data = request.form.getlist('selfImprovement[]')
        for entry in self_improvement_data:
            data = eval(entry)
            print(f"Inserting into self_imp: {data}")
            cursor.execute(""" 
                INSERT INTO self_imp (form_id, title, month, name_of_conf, issn, co_auth, link) 
                VALUES (%s, %s, %s, %s, %s, %s, %s) 
            """, (form_id, data['title'], data['monthYear'], data['conference'], 
                  data['isbn'], data['coAuthors'], data['link']))

        # Process certificationTable data
        certification_data = request.form.getlist('certification[]')
        for entry in certification_data:
            data = eval(entry)
            print(f"Inserting into certifications: {data}")
            if 'name' in data and data['name']:
                file = request.files.get(f"certificationFile[]")
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    print(f"File saved at: {filepath}")
                    cursor.execute("""
                        INSERT INTO certifications (form_id, name, uploads) 
                        VALUES (%s, %s, %s) 
                    """, (form_id, data['name'], filepath))

        # Process titleTable data
        title_data = request.form.getlist('title[]')
        for entry in title_data:
            data = eval(entry)
            print(f"Inserting into copyright: {data}")
            cursor.execute(""" 
                INSERT INTO copyright (form_id, name, month, reg_no) 
                VALUES (%s, %s, %s, %s) 
            """, (form_id, data['name'], data['monthYear'], data['registration']))

        # Process resourcePersonTable data
        resource_data = request.form.getlist('resourcePerson[]')
        for entry in resource_data:
            data = eval(entry)
            print(f"Inserting into resource_person: {data}")
            if data:  # Only insert if data is not empty
                cursor.execute("""
                    INSERT INTO resource_person (form_id, name, dept, name_oi, num_op) 
                    VALUES (%s, %s, %s, %s, %s) 
                """, (form_id, data['topic'], data['department'], data['institute'], data['participants']))

        # Process universityCommitteeTable data
        committee_data = request.form.getlist('universityCommittee[]')
        for entry in committee_data:
            data = eval(entry)
            print(f"Inserting into mem_uni: {data}")
            if data:  # Only insert if data is not empty
                cursor.execute("""
                    INSERT INTO mem_uni (form_id, name, roles, designation) 
                    VALUES (%s, %s, %s, %s) 
                """, (form_id, data['committee'], data['responsibilities'], data['designation']))

        # Process externalProjectsTable data
            project_data = request.form.getlist('externalProjects[]')
            for entry in project_data:
                data = eval(entry)
                print(f"Inserting into external_projects: {data}")
                
                if data:  # Only insert if data is not empty
                    # Insert into external_projects with form_id included
                    print(f"Inserting into external_projects: {data}")
                    cursor.execute("""
                        INSERT INTO external_projects (form_id, role, `desc`, contribution, university, duration, comments) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (form_id, data['role'], data['description'], data['contribution'], 
                        data['university'], data['duration'], data['comments']))



        # Process contributionTable data
        contribution_data = request.form.getlist('contribution[]')
        for entry in contribution_data:
            data = eval(entry)
            print(f"Inserting into contribution_to_society: {data}")
            if data:  # Only insert if data is not empty
                file = request.files.get(f"contributionFile[]")
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    print(f"File saved at: {filepath}")
                    cursor.execute("""
                        INSERT INTO contribution_to_society (form_id, semester, activity, points, order_cpy, uploads) 
                        VALUES (%s, %s, %s, %s, %s, %s) 
                    """, (form_id, data['semester'], data['activity'], data['points'], 
                          data['orderCopy'], filepath))

        # Commit the transaction
        conn.commit()
        return jsonify(status='success', message='Data saved successfully')

    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()  # Rollback in case of error
        return jsonify(status='error', message=str(e))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



@app.route('/save-3total-points', methods=['POST'])
def save_3total_points():
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        # Get data from the request
        data = request.get_json()
        form_id = data.get('form_id')
        total = data.get('total')
        acr = data.get('acr')
        society = data.get('society')

        print(f"Received data: form_id={form_id}, total={total}, acr={acr}, society={society}")

        # Validate form_id and total
        if not form_id or total is None:
            return jsonify({"success": False, "message": "Invalid form data"}), 400

        
        cursor = connection.cursor()

        # Insert or update total points data into the forms table
        insert_query = """
            INSERT INTO form3_tot (form_id, total, acr, society)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                total = VALUES(total), 
                acr = VALUES(acr), 
                society = VALUES(society)
        """
        cursor.execute(insert_query, (form_id, total, acr, society))

        # Commit the changes to the database
        connection.commit()

        return jsonify({"success": True, "message": "Total points saved successfully!"})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "An error occurred while saving data"}), 500

    finally:
        # Ensure the cursor and connection are closed properly
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route('/review/<form_id>')
def review(form_id):
    # Initialize all variables to ensure they have default values
    teaching_data, feedback_data, dept_act_data, inst_act_data = [], [], [], []
    points_data = {}
    user_data = {}
    self_improvement_data = []
    certification_data = []
    title_data = []
    resource_data = []
    committee_data = []
    project_data = []
    contribution_data = []

    # Connect to the database
    connection = connect_to_database()

    if connection:
        try:
            with connection.cursor() as cursor:
                # Fetch user_id, acad_years, name, and dept based on form_id
                sql_user_acad = """
                SELECT user_id, acad_years FROM acad_years WHERE form_id = %s
                """
                cursor.execute(sql_user_acad, (form_id,))
                user_acad_result = cursor.fetchone()

                if user_acad_result:
                    user_id, selected_year = user_acad_result  # Unpack the result
                else:
                    flash('No data found for the provided form ID.', 'warning')
                    return redirect(url_for('review', form_id=form_id))  # Pass form_id

                # Fetch user details from the users table, including name and dept
                sql_user = """
                SELECT userid, gmail, dept, name, designation, d_o_j, dob, edu_q, exp
                FROM users
                WHERE userid = %s
                """
                cursor.execute(sql_user, (user_id,))
                user_data = cursor.fetchone()

                # Unpack user data
                if user_data:
                    user_name = user_data[3]  # Name
                    user_dept = user_data[2]  # Department
                else:
                    flash('User not found.', 'warning')
                    return redirect(url_for('review', form_id=form_id))

                # Fetch teaching process data
                sql = """
                    SELECT semester, course_code, classes_scheduled, classes_held,
                    (classes_held/classes_scheduled)*5 AS totalpoints
                    FROM teaching_process WHERE form_id = %s
                """
                cursor.execute(sql, (form_id,))
                teaching_data = cursor.fetchall()

                # Fetch student feedback data including uploads
                sql = """
                    SELECT semester, course_code, total_points, points_obtained, uploads
                    FROM students_feedback WHERE form_id = %s
                """
                cursor.execute(sql, (form_id,))
                feedback_data = cursor.fetchall()

                # Fetch department activity data
                sql = """
                    SELECT semester, activity, points, order_cpy, uploads
                    FROM department_act WHERE form_id = %s
                """
                cursor.execute(sql, (form_id,))
                dept_act_data = cursor.fetchall()

                # Fetch institute activity data
                sql = """
                    SELECT semester, activity, points, order_cpy, uploads
                    FROM institute_act WHERE form_id = %s
                """
                cursor.execute(sql, (form_id,))
                inst_act_data = cursor.fetchall()

                # Fetch self-improvement data
                sql = "SELECT title, month, name_of_conf, issn, co_auth, link FROM self_imp WHERE form_id = %s"
                cursor.execute(sql, (form_id,))
                self_improvement_data = cursor.fetchall()

                # Fetch certification data
                sql = "SELECT name, uploads FROM certifications WHERE form_id = %s"
                cursor.execute(sql, (form_id,))
                certification_data = cursor.fetchall()

                # Fetch title data
                sql = "SELECT name, month, reg_no FROM copyright WHERE form_id = %s"
                cursor.execute(sql, (form_id,))
                title_data = cursor.fetchall()

                # Fetch resource person data
                sql = "SELECT name, dept, name_oi, num_op FROM resource_person WHERE form_id = %s"
                cursor.execute(sql, (form_id,))
                resource_data = cursor.fetchall()

                # Fetch university committee data
                sql = "SELECT name, roles, designation FROM mem_uni WHERE form_id = %s"
                cursor.execute(sql, (form_id,))
                committee_data = cursor.fetchall()

                # Fetch external projects data
                sql = "SELECT role, `desc`, contribution, university, duration, comments FROM external_projects WHERE form_id = %s"
                cursor.execute(sql, (form_id,))
                project_data = cursor.fetchall()

                # Fetch contribution data
                sql = "SELECT semester, activity, points, order_cpy, uploads FROM contribution_to_society WHERE form_id = %s"
                cursor.execute(sql, (form_id,))
                contribution_data = cursor.fetchall()

                # Fetch points for Final Score table
                cursor.execute("SELECT teaching, feedback FROM form1_tot WHERE form_id = %s", (form_id,))
                form1_tot = cursor.fetchone()

                cursor.execute("SELECT dept, institute FROM form2_tot WHERE form_id = %s", (form_id,))
                form2_tot = cursor.fetchone()

                cursor.execute("SELECT acr, society FROM form3_tot WHERE form_id = %s", (form_id,))
                form3_tot = cursor.fetchone()

                # Populate points_data with proper integer casting
                points_data = {
                    'teaching': int(form1_tot[0]) if form1_tot and form1_tot[0] else 0,
                    'feedback': int(form1_tot[1]) if form1_tot and form1_tot[1] else 0,
                    'dept': int(form2_tot[0]) if form2_tot and form2_tot[0] else 0,
                    'institute': int(form2_tot[1]) if form2_tot and form2_tot[1] else 0,
                    'acr': int(form3_tot[0]) if form3_tot and form3_tot[0] else 0,
                    'society': int(form3_tot[1]) if form3_tot and form3_tot[1] else 0,
                }

                # Calculate the total points safely
                total_points = sum(points_data.values())

                # Insert or update the total in the 'total' table with name and dept
                sql_total = """
                    INSERT INTO total (form_id, user_id, acad_years, total, name, dept)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE total = VALUES(total), name = VALUES(name), dept = VALUES(dept)
                """
                cursor.execute(sql_total, (form_id, user_id, selected_year, total_points, user_name, user_dept))

                # Commit the transaction
                connection.commit()

        except Exception as e:
            connection.rollback()
            flash(f"An error occurred: {str(e)}", 'danger')
            return redirect(url_for('review', form_id=form_id))  # Correct redirect
        finally:
            connection.close()

    # Render the template with all the fetched data
    return render_template(
        'reviewform.html',
        teaching_data=teaching_data,
        feedback_data=feedback_data,
        dept_act_data=dept_act_data,
        inst_act_data=inst_act_data,
        points_data=points_data,
        self_improvement_data=self_improvement_data,
        certification_data=certification_data,
        title_data=title_data,
        resource_data=resource_data,
        committee_data=committee_data,
        project_data=project_data,
        contribution_data=contribution_data,
        user_data=user_data,
        selected_year=selected_year,
        form_id=form_id
    )





@app.route('/finalscore/<int:form_id>')
def finalscore_page(form_id):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            # Fetch user_id from acad_years table based on form_id
            cursor.execute("SELECT user_id FROM acad_years WHERE form_id = %s", (form_id,))
            acad_info = cursor.fetchone()

            if not acad_info:
                return "Error: No user ID found for the given form ID", 404

            user_id = acad_info[0]

            return render_template('finalscore.html', form_id=form_id, user_id=user_id)
    finally:
        connection.close()



@app.route('/get_scores/<form_id>', methods=['GET'])
def get_scores(form_id):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            # Fetch user_id and acad_year from acad_years table based on form_id
            cursor.execute("SELECT user_id, acad_years FROM acad_years WHERE form_id = %s", (form_id,))
            acad_info = cursor.fetchone()

            if not acad_info:
                return jsonify({'error': 'No academic year or user ID found for the given form ID'}), 404

            user_id, acad_years = acad_info

            # Fetch scores from form1_tot
            cursor.execute("SELECT teaching, feedback FROM form1_tot WHERE form_id = %s", (form_id,))
            form1_tot = cursor.fetchone()

            # Fetch scores from form2_tot
            cursor.execute("SELECT dept, institute FROM form2_tot WHERE form_id = %s", (form_id,))
            form2_tot = cursor.fetchone()

            # Fetch scores from form3_tot
            cursor.execute("SELECT acr, society FROM form3_tot WHERE form_id = %s", (form_id,))
            form3_tot = cursor.fetchone()

            # Prepare response data
            response = {
                'user_id': user_id,
                'acad_years': acad_years,
                'teaching': form1_tot[0] if form1_tot else 0,
                'feedback': form1_tot[1] if form1_tot else 0,
                'dept': form2_tot[0] if form2_tot else 0,
                'institute': form2_tot[1] if form2_tot else 0,
                'acr': form3_tot[0] if form3_tot else 0,
                'society': form3_tot[1] if form3_tot else 0,
            }

            return jsonify(response)
    finally:
        connection.close()

@app.route('/save_total_points', methods=['POST'])
def save_fac_total_points():
    data = request.json
    total_points = data['totalPoints']
    form_id = data['formId']
    user_id = data['userId']

    print(f"Received total_points: {total_points}, form_id: {form_id}, user_id: {user_id}")

    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            # Fetch the academic year from the acad_years table
            cursor.execute("SELECT acad_years FROM acad_years WHERE form_id = %s", (form_id,))
            acad_data = cursor.fetchone()

            if not acad_data:
                return jsonify({'error': 'Academic year not found for the given form ID'}), 404

            acad_years = acad_data[0]  # Extract acad_years

            print(f"Saving: form_id={form_id}, user_id={user_id}, acad_years={acad_years}, total_points={total_points}")

            # Insert the total points into the forms table
            query = """
                INSERT INTO forms (form_id, user_id, acad_years, fac_total) 
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE fac_total = VALUES(fac_total)
            """
            cursor.execute(query, (form_id, user_id, acad_years, total_points))
            connection.commit()

            return jsonify({'message': 'Total points saved successfully!'}), 200
    except Exception as e:
        print(f"Error saving total points: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()


@app.route('/landing')
def landing():
    user_id = session.get('user_id')
    return render_template('landingpage.html')

@app.route('/pastforms', methods=['GET'])
def render_pastforms():
    user_id = session.get('user_id')
    connection = connect_to_database()
    
    try:
        with connection.cursor() as cursor:
            # Query to check for entries in the acad_years table for the given user_id
            query = "SELECT COUNT(*) FROM acad_years WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            
            # Check the count of entries
            if result[0] == 0:
                flash('You have no past forms filled.', 'warning')  # Flash message for user
                return redirect(url_for('landing'))  # Redirect to another route, e.g., home or dashboard
            
            # If there are entries, render the pastforms.html page with the teaching_data
            return render_template('pastforms.html', teaching_data=[], selected_year=None)
    
    finally:
        connection.close()

@app.route('/pastforms/search', methods=['POST'])
def search_pastforms():
    user_id = session.get('user_id')
    selected_year = request.form.get('academicYear')

    # Connect to the database
    connection = connect_to_database()

    # Initialize all data variables
    teaching_data, feedback_data, dept_act_data, inst_act_data, society_data = [], [], [], [], []
    self_improvement_data, certification_data, title_data, resource_data = [], [], [], []
    committee_data, project_data, contribution_data = [], [], []
    points_data = {}  # Store points for criteria
    acr_data = {}     # Store ACR data (if needed)

    try:
        with connection.cursor() as cursor:
            # Fetch the form_id from acad_years table
            sql = "SELECT form_id FROM acad_years WHERE user_id = %s AND acad_years = %s"
            cursor.execute(sql, (user_id, selected_year))
            result = cursor.fetchone()

            if result:
                form_id = result[0]

                # Fetch teaching process data
                sql = """
                    SELECT semester, course_code, classes_scheduled, classes_held,
                    (classes_held/classes_scheduled)*5 AS totalpoints
                    FROM teaching_process WHERE form_id = %s
                """
                cursor.execute(sql, (form_id,))
                teaching_data = cursor.fetchall()

                # Fetch student feedback data including uploads
                sql = """
                    SELECT semester, course_code, total_points, points_obtained, uploads
                    FROM students_feedback WHERE form_id = %s
                """
                cursor.execute(sql, (form_id,))
                feedback_data = cursor.fetchall()

                # Fetch department activity data
                sql = """
                    SELECT semester, activity, points, order_cpy, uploads
                    FROM department_act WHERE form_id = %s
                """
                cursor.execute(sql, (form_id,))
                dept_act_data = cursor.fetchall()

                # Fetch institute activity data
                sql = """
                    SELECT semester, activity, points, order_cpy, uploads
                    FROM institute_act WHERE form_id = %s
                """
                cursor.execute(sql, (form_id,))
                inst_act_data = cursor.fetchall()

                # Fetch self-improvement data
                sql = "SELECT title, month, name_of_conf, issn, co_auth, link FROM self_imp WHERE form_id = %s"
                cursor.execute(sql, (form_id,))
                self_improvement_data = cursor.fetchall()

                # Fetch certification data
                sql = "SELECT name, uploads FROM certifications WHERE form_id = %s"
                cursor.execute(sql, (form_id,))
                certification_data = cursor.fetchall()

                # Fetch title data
                sql = "SELECT name, month, reg_no FROM copyright WHERE form_id = %s"
                cursor.execute(sql, (form_id,))
                title_data = cursor.fetchall()

                # Fetch resource person data
                sql = "SELECT name, dept, name_oi, num_op FROM resource_person WHERE form_id = %s"
                cursor.execute(sql, (form_id,))
                resource_data = cursor.fetchall()

                # Fetch university committee data
                sql = "SELECT name, roles, designation FROM mem_uni WHERE form_id = %s"
                cursor.execute(sql, (form_id,))
                committee_data = cursor.fetchall()

                # Fetch external projects data
                sql = """
                    SELECT role, `desc`, contribution, university, duration, comments
                    FROM external_projects WHERE form_id = %s
                """
                cursor.execute(sql, (form_id,))
                project_data = cursor.fetchall()

                # Fetch contribution to society data
                sql = """
                    SELECT semester, activity, points, order_cpy, uploads
                    FROM contribution_to_society WHERE form_id = %s
                """
                cursor.execute(sql, (form_id,))
                contribution_data = cursor.fetchall()

                # Fetch points for final score table
                cursor.execute("SELECT teaching, feedback FROM form1_tot WHERE form_id = %s", (form_id,))
                form1_tot = cursor.fetchone()

                cursor.execute("SELECT dept, institute FROM form2_tot WHERE form_id = %s", (form_id,))
                form2_tot = cursor.fetchone()

                cursor.execute("SELECT acr, society FROM form3_tot WHERE form_id = %s", (form_id,))
                form3_tot = cursor.fetchone()

                # Populate points_data with proper integer casting
                points_data = {
                    'teaching': int(form1_tot[0]) if form1_tot and form1_tot[0] else 0,
                    'feedback': int(form1_tot[1]) if form1_tot and form1_tot[1] else 0,
                    'dept': int(form2_tot[0]) if form2_tot and form2_tot[0] else 0,
                    'institute': int(form2_tot[1]) if form2_tot and form2_tot[1] else 0,
                    'acr': int(form3_tot[0]) if form3_tot and form3_tot[0] else 0,
                    'society': int(form3_tot[1]) if form3_tot and form3_tot[1] else 0,
                }

    except Exception as e:
        flash(f'An error occurred while fetching data: {str(e)}', 'danger')

    finally:
        connection.close()

    # Render the template with all the fetched data
    return render_template(
        'pastforms.html',
        teaching_data=teaching_data,
        feedback_data=feedback_data,
        dept_act_data=dept_act_data,
        inst_act_data=inst_act_data,
        society_data=society_data,
        points_data=points_data,
        self_improvement_data=self_improvement_data,
        certification_data=certification_data,
        title_data=title_data,
        resource_data=resource_data,
        committee_data=committee_data,
        project_data=project_data,
        contribution_data=contribution_data,
        selected_year=selected_year
    )


# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Ensure the filename is safe and exists in the upload directory
    safe_filename = os.path.basename(filename)  # Prevent directory traversal attacks
    file_path = os.path.join(UPLOAD_FOLDER, safe_filename)

    try:
        if os.path.exists(file_path):
            return send_from_directory(UPLOAD_FOLDER, safe_filename, as_attachment=False)
        else:
            abort(404, description="File not found")
    except Exception as e:
        abort(500, description=f"Server error: {str(e)}")


@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/highlanding')
def highlanding():
    user_id = session.get('user_id')
    print(f"User ID from session: {user_id}")

    if user_id:
        connection = connect_to_database()

        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT dept FROM users WHERE userid = %s"
                    print(f"Executing SQL: {sql} with user_id: {user_id}")
                    cursor.execute(sql, (user_id,))
                    result = cursor.fetchone()
                    print(f"Result fetched from DB: {result}")

                    if result:
                        # Adjust here based on how the result is structured
                        department = result[0]  # Accessing department based on index
                        print(f"Department fetched from DB: {department}")
                    else:
                        department = None

            except Exception as e:
                print(f"Error querying database: {e}")
                department = None
            finally:
                connection.close()  # Ensure the connection is closed

        else:
            department = None

        print(f"Department fetched: {department}")
        return render_template('highlanding.html', department=department)

    return redirect(url_for('login'))

@app.route('/stafflist')
def stafflist():
    user_id = session.get('user_id')
    department = request.args.get('department')
    print(f"Department received: {department}")

    connection = connect_to_database()
    users = []

    if connection:
        try:
            with connection.cursor() as cursor:
                # Fetch only users with the role 'Faculty'
                sql = "SELECT name, gmail, userid FROM users WHERE dept = %s AND role = 'Faculty'"
                cursor.execute(sql, (department,))
                users = cursor.fetchall()
                print(f"Users fetched from DB: {users}")
        except Exception as e:
            print(f"Error querying database: {e}")
        finally:
            connection.close()

    return render_template('stafflist.html', department=department, users=users)


@app.route('/hodpastform')
def hodpastform():
    points_data = {
    'teaching': 0,
    'feedback': 0,
    'dept': 0,
    'institute': 0,
    'acr': 0,
    'society': 0
}
    user_id = request.args.get('userid')
    session['user_id'] = user_id  # Store the user_id in session
    
    user_name = request.args.get('name')
    session['user_name'] = user_name
    return render_template('hodpastform.html', user_id=user_id ,user_name=user_name, points_data= points_data)



@app.route('/search_pastforms', methods=['POST'])
def search_pastforms2():
    points_data = {
    'teaching': 0,
    'feedback': 0,
    'dept': 0,
    'institute': 0,
    'acr': 0,
    'society': 0
}
    # Retrieve user details from the session and academic year from the form
    user_id = session.get('user_id')
    selected_year = request.form.get('academicYear')
    user_name = session.get('user_name')
    if not user_id or not selected_year:
        flash("User ID or Academic Year is missing!", "danger")
        return redirect(url_for('hodpastform'))

    # Initialize data containers
    teaching_data, feedback_data, dept_act_data, inst_act_data = [], [], [], []
    society_data, points_data, acr_data = {}, {}, {}
    self_improvement_data, certification_data, title_data = [], [], []
    resource_data, committee_data, project_data, contribution_data = [], [], [], []

    # Connect to the database
    connection = connect_to_database()

    if connection:
        try:
            with connection.cursor() as cursor:
                # Fetch form_id for the given user and academic year
                cursor.execute(
                    "SELECT form_id FROM acad_years WHERE user_id = %s AND acad_years = %s",
                    (user_id, selected_year)
                )
                result = cursor.fetchone()

                if not result:
                    flash("No data found for the selected academic year.", "warning")
                    return redirect(url_for('hodpastform'))

                form_id = result[0]  # Extract form_id

                # Fetch teaching process data
                cursor.execute("""
                    SELECT semester, course_code, classes_scheduled, classes_held,
                           (classes_held / classes_scheduled) * 5 AS totalpoints
                    FROM teaching_process
                    WHERE form_id = %s
                """, (form_id,))
                teaching_data = cursor.fetchall()

                # Fetch student feedback data including uploaded documents
                cursor.execute("""
                    SELECT semester, course_code, total_points, points_obtained, uploads
                    FROM students_feedback
                    WHERE form_id = %s
                """, (form_id,))
                feedback_data = cursor.fetchall()

                # Fetch departmental activities data
                cursor.execute("""
                    SELECT semester, activity, points, order_cpy, uploads
                    FROM department_act
                    WHERE form_id = %s
                """, (form_id,))
                dept_act_data = cursor.fetchall()

                # Fetch institute activities data
                cursor.execute("""
                    SELECT semester, activity, points, order_cpy, uploads
                    FROM institute_act
                    WHERE form_id = %s
                """, (form_id,))
                inst_act_data = cursor.fetchall()

                # Fetch self-improvement data
                cursor.execute("SELECT title, month, name_of_conf, issn, co_auth, link FROM self_imp WHERE form_id = %s", (form_id,))
                self_improvement_data = cursor.fetchall()

                # Fetch certification data
                cursor.execute("SELECT name, uploads FROM certifications WHERE form_id = %s", (form_id,))
                certification_data = cursor.fetchall()

                # Fetch title data
                cursor.execute("SELECT name, month, reg_no FROM copyright WHERE form_id = %s", (form_id,))
                title_data = cursor.fetchall()

                # Fetch resource person data
                cursor.execute("SELECT name, dept, name_oi, num_op FROM resource_person WHERE form_id = %s", (form_id,))
                resource_data = cursor.fetchall()

                # Fetch university committee data
                cursor.execute("SELECT name, roles, designation FROM mem_uni WHERE form_id = %s", (form_id,))
                committee_data = cursor.fetchall()

                # Fetch external projects data
                cursor.execute("SELECT role, `desc`, contribution, university, duration, comments FROM external_projects WHERE form_id = %s", (form_id,))
                project_data = cursor.fetchall()

                # Fetch contribution data
                cursor.execute("SELECT semester, activity, points, order_cpy, uploads FROM contribution_to_society WHERE form_id = %s", (form_id,))
                contribution_data = cursor.fetchall()

                # Fetch points for Final Score table
                cursor.execute("SELECT teaching, feedback FROM form1_tot WHERE form_id = %s", (form_id,))
                form1_tot = cursor.fetchone()

                cursor.execute("SELECT dept, institute FROM form2_tot WHERE form_id = %s", (form_id,))
                form2_tot = cursor.fetchone()

                cursor.execute("SELECT acr, society FROM form3_tot WHERE form_id = %s", (form_id,))
                form3_tot = cursor.fetchone()

                # Populate points_data with proper integer casting
                points_data = {
                    'teaching': int(form1_tot[0]) if form1_tot and form1_tot[0] else 0,
                    'feedback': int(form1_tot[1]) if form1_tot and form1_tot[1] else 0,
                    'dept': int(form2_tot[0]) if form2_tot and form2_tot[0] else 0,
                    'institute': int(form2_tot[1]) if form2_tot and form2_tot[1] else 0,
                    'acr': int(form3_tot[0]) if form3_tot and form3_tot[0] else 0,
                    'society': int(form3_tot[1]) if form3_tot and form3_tot[1] else 0,
                }

        except Exception as e:
            flash(f"Error fetching data: {str(e)}", "danger")
        finally:
            connection.close()

    # Render the template with all the fetched data
    return render_template(
        'hodpastform.html',
        teaching_data=teaching_data,
        feedback_data=feedback_data,
        dept_act_data=dept_act_data,
        inst_act_data=inst_act_data,
        society_data=society_data,
        points_data=points_data,
        self_improvement_data=self_improvement_data,
        certification_data=certification_data,
        title_data=title_data,
        resource_data=resource_data,
        committee_data=committee_data,
        project_data=project_data,
        contribution_data=contribution_data,
        selected_year=selected_year,
        user_name=user_name, user_id=user_id
    )


@app.route('/submit_assessment', methods=['POST'])
def submit_assessment():
    # Fetch JSON data from the request
    data = request.get_json()

    # Debugging: Print incoming data
    print("Incoming Data:", data)

    # Ensure data is not None
    if data is None:
        return jsonify({"status": "error", "message": "Invalid JSON data"}), 400

    # Fetch user_id and acad_years from the data
    user_id = data.get('user_id')
    acad_years = data.get('acad_years')

    # Extract feedback and assessment values with integer conversion
    feedback = data.get('feedback', '')  # Retrieve feedback

    # Ensure all `hodas` fields are integers. Default to 0 if missing or invalid.
    def get_int_value(key):
        try:
            return int(data.get(key, 0))  # Safely convert to int, default to 0
        except (ValueError, TypeError):
            return 0  # Handle invalid values gracefully

    hodas1 = get_int_value('hodas1')
    hodas2 = get_int_value('hodas2')
    hodas3 = get_int_value('hodas3')
    hodas4 = get_int_value('hodas4')
    hodas5 = get_int_value('hodas5')
    hodas6 = get_int_value('hodas6')

    # Calculate the total of hodas values
    hodtotal = hodas1 + hodas2 + hodas3 + hodas4 + hodas5 + hodas6
    print(f"Calculated Total (hodtotal): {hodtotal}")

    # Connect to the database
    connection = connect_to_database()
    cursor = connection.cursor()

    # Fetch form_id from acad_years table
    cursor.execute(
        "SELECT form_id FROM acad_years WHERE user_id = %s AND acad_years = %s", 
        (user_id, acad_years)
    )
    result = cursor.fetchone()
    form_id = result[0] if result else None

    if form_id:
        try:
            # Insert or update data in the relevant tables
            cursor.execute(""" 
                INSERT INTO form1_tot (form_id, hodas1, hodas2) 
                VALUES (%s, %s, %s) 
                ON DUPLICATE KEY UPDATE hodas1 = %s, hodas2 = %s
            """, (form_id, hodas1, hodas2, hodas1, hodas2))

            cursor.execute(""" 
                INSERT INTO form2_tot (form_id, hodas3, hodas4) 
                VALUES (%s, %s, %s) 
                ON DUPLICATE KEY UPDATE hodas3 = %s, hodas4 = %s
            """, (form_id, hodas3, hodas4, hodas3, hodas4))

            cursor.execute(""" 
                INSERT INTO form3_tot (form_id, hodas5, hodas6) 
                VALUES (%s, %s, %s) 
                ON DUPLICATE KEY UPDATE hodas5 = %s, hodas6 = %s
            """, (form_id, hodas5, hodas6, hodas5, hodas6))

            # Insert or update feedback
            cursor.execute(""" 
                INSERT INTO feedback (form_id, feedback)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE feedback = %s
            """, (form_id, feedback, feedback))

            # Insert or update the hodtotal in the 'total' table
            cursor.execute(""" 
                INSERT INTO total (form_id, hodtotal) 
                VALUES (%s, %s) 
                ON DUPLICATE KEY UPDATE hodtotal = %s
            """, (form_id, hodtotal, hodtotal))

            # Commit the transaction
            connection.commit()

            return jsonify({"status": "success"})

        except Exception as e:
            print(f"Error: {str(e)}")
            connection.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500

    else:
        print(f"No form_id found for user_id: {user_id} and acad_years: {acad_years}")
        return jsonify({"status": "error", "message": "Form ID not found"}), 404


@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    department = request.args.get('department')
    return render_template('dashboard.html', department = department)

# Your existing routes and database connection logic
@app.route('/get_top_performers', methods=['POST'])
def get_top_performers():
    acad_years = request.json['academic_year']
    dept = request.json['department']

    print(f"Received academic year: {acad_years}, department: {dept}")  # Debug log

    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, total FROM total
        WHERE acad_years = %s AND dept = %s
        ORDER BY total DESC
        LIMIT 5
    """, (acad_years, dept))

    results = cursor.fetchall()
    print(f"Query Results: {results}")  # Debug log

    top_performers = [{'name': row[0], 'total': row[1]} for row in results]

    while len(top_performers) < 5:
        top_performers.append({'name': '', 'total': 0})

    cursor.close()
    return jsonify(top_performers)

# Add the after_request handler here to prevent caching
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response



@app.route('/principlestaff')
def principlestaff():
    
    user_id = request.args.get('userid')
    session['user_id'] = user_id  # Store the user_id in session
    
    user_name = request.args.get('name')
    session['user_name'] = user_name
    return render_template('principlestaff.html')


@app.route('/filter_staff', methods=['GET'])
def filter_staff():
    department = request.args.get('department', '')
    print(f"Department received: {department}")

    connection = connect_to_database()
    users = []

    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT name, gmail, userid 
                    FROM users 
                    WHERE dept = %s AND role = 'Faculty'
                """
                cursor.execute(sql, (department,))
                users = cursor.fetchall()
                print(f"Users fetched from DB: {users}")
        except Exception as e:
            print(f"Error querying database: {e}")
        finally:
            connection.close()

    return jsonify({'users': users})


@app.route('/principlepastform')
def principlepastform():
    points_data = {
    'teaching': 0,
    'feedback': 0,
    'dept': 0,
    'institute': 0,
    'acr': 0,
    'society': 0
}
    assessments = {
                    'hodas1':0,
                    'hodas2': 0,
                    'hodas3': 0,
                    'hodas4':0,
                    'hodas5': 0,
                    'hodas6': 0,
                }
    user_id = session.get('user_id')
    department = request.args.get('department')
    user_id = request.args.get('userid')
    session['user_id'] = user_id  # Store the user_id in session
    
    user_name = request.args.get('name')
    session['user_name'] = user_name
    return render_template('principlepast.html', user_name=user_name, user_id=user_id, department = department , points_data = points_data, assessments = assessments)


@app.route('/principle_pastforms', methods=['POST'])
def principle_pastforms():
    points_data = {
        'teaching': 0,
        'feedback': 0,
        'dept': 0,
        'institute': 0,
        'acr': 0,
        'society': 0
    }
   
    assessments = {
                    'hodas1':0,
                    'hodas2': 0,
                    'hodas3': 0,
                    'hodas4':0,
                    'hodas5': 0,
                    'hodas6': 0,
                }

    # Retrieve user details from session and academic year from the form
    user_id = session.get('user_id')
    selected_year = request.form.get('academicYear')
    user_name = session.get('user_name')

    if not user_id or not selected_year:
        flash("User ID or Academic Year is missing!", "danger")
        return redirect(url_for('principlepastform'))

    # Initialize data containers
    teaching_data, feedback_data, dept_act_data, inst_act_data = [], [], [], []
    society_data, points_data, acr_data = {}, {}, {}
    self_improvement_data, certification_data, title_data = [], [], []
    resource_data, committee_data, project_data, contribution_data = [], [], [], []
    hodas_data = {}  # Container for HOD-specific data
    extra_feedback = []  # Container for feedback from the 'feedback' table

    # Connect to the database
    connection = connect_to_database()

    if connection:
        try:
            with connection.cursor() as cursor:
                # Fetch form_id for the given user and academic year
                cursor.execute(
                    "SELECT form_id FROM acad_years WHERE user_id = %s AND acad_years = %s",
                    (user_id, selected_year)
                )
                result = cursor.fetchone()

                if not result:
                    flash("No data found for the selected academic year.", "warning")
                    return redirect(url_for('principlepastform'))

                form_id = result[0]  # Extract form_id

                # Fetch teaching process data
                cursor.execute("""
                    SELECT semester, course_code, classes_scheduled, classes_held,
                           (classes_held / classes_scheduled) * 5 AS totalpoints
                    FROM teaching_process
                    WHERE form_id = %s
                """, (form_id,))
                teaching_data = cursor.fetchall()

                # Fetch student feedback data including uploaded documents
                cursor.execute("""
                    SELECT semester, course_code, total_points, points_obtained, uploads
                    FROM students_feedback
                    WHERE form_id = %s
                """, (form_id,))
                feedback_data = cursor.fetchall()

                # Fetch departmental activities data
                cursor.execute("""
                    SELECT semester, activity, points, order_cpy, uploads
                    FROM department_act
                    WHERE form_id = %s
                """, (form_id,))
                dept_act_data = cursor.fetchall()

                # Fetch institute activities data
                cursor.execute("""
                    SELECT semester, activity, points, order_cpy, uploads
                    FROM institute_act
                    WHERE form_id = %s
                """, (form_id,))
                inst_act_data = cursor.fetchall()

                # Fetch self-improvement data
                cursor.execute("SELECT title, month, name_of_conf, issn, co_auth, link FROM self_imp WHERE form_id = %s", (form_id,))
                self_improvement_data = cursor.fetchall()

                # Fetch certification data
                cursor.execute("SELECT name, uploads FROM certifications WHERE form_id = %s", (form_id,))
                certification_data = cursor.fetchall()

                # Fetch title data
                cursor.execute("SELECT name, month, reg_no FROM copyright WHERE form_id = %s", (form_id,))
                title_data = cursor.fetchall()

                # Fetch resource person data
                cursor.execute("SELECT name, dept, name_oi, num_op FROM resource_person WHERE form_id = %s", (form_id,))
                resource_data = cursor.fetchall()

                # Fetch university committee data
                cursor.execute("SELECT name, roles, designation FROM mem_uni WHERE form_id = %s", (form_id,))
                committee_data = cursor.fetchall()

                # Fetch external projects data
                cursor.execute("SELECT role, `desc`, contribution, university, duration, comments FROM external_projects WHERE form_id = %s", (form_id,))
                project_data = cursor.fetchall()

                # Fetch contribution data
                cursor.execute("SELECT semester, activity, points, order_cpy, uploads FROM contribution_to_society WHERE form_id = %s", (form_id,))
                contribution_data = cursor.fetchall()

                # Fetch points for Final Score table
                cursor.execute("SELECT teaching, feedback, hodas1, hodas2 FROM form1_tot WHERE form_id = %s", (form_id,))
                form1_tot = cursor.fetchone()
                print("Fetched Form1 Totals:", form1_tot)

                cursor.execute("SELECT dept, institute, hodas3, hodas4 FROM form2_tot WHERE form_id = %s", (form_id,))
                form2_tot = cursor.fetchone()
                print("Fetched Form2 Totals:", form2_tot)

                cursor.execute("SELECT acr, society, hodas5, hodas6 FROM form3_tot WHERE form_id = %s", (form_id,))
                form3_tot = cursor.fetchone()
                print("Fetched Form3 Totals:", form3_tot)


                # Populate points_data with proper integer casting
                points_data = {
                    'teaching': int(form1_tot[0]) if form1_tot and form1_tot[0] else 0,
                    'feedback': int(form1_tot[1]) if form1_tot and form1_tot[1] else 0,
                    'dept': int(form2_tot[0]) if form2_tot and form2_tot[0] else 0,
                    'institute': int(form2_tot[1]) if form2_tot and form2_tot[1] else 0,
                    'acr': int(form3_tot[0]) if form3_tot and form3_tot[0] else 0,
                    'society': int(form3_tot[1]) if form3_tot and form3_tot[1] else 0,
                }

              # Store HOD-specific data with integer conversion
                assessments = {
                    'hodas1': int(form1_tot[2]) if form1_tot and form1_tot[2] is not None else 0,
                    'hodas2': int(form1_tot[3]) if form1_tot and form1_tot[3] is not None else 0,
                    'hodas3': int(form2_tot[2]) if form2_tot and form2_tot[2] is not None else 0,
                    'hodas4': int(form2_tot[3]) if form2_tot and form2_tot[3] is not None else 0,
                    'hodas5': int(form3_tot[2]) if form3_tot and form3_tot[2] is not None else 0,
                    'hodas6': int(form3_tot[3]) if form3_tot and form3_tot[3] is not None else 0,
                }
                
                 # Fetch additional feedback from the 'feedback' table
                cursor.execute("""
                    SELECT feedback FROM feedback WHERE form_id = %s
                """, (form_id,))
                
                extra_feedback_row = cursor.fetchone()  # Use fetchone() to get the first row

# Convert to string directly
                if extra_feedback_row and extra_feedback_row[0] is not None:
                    extra_feedback = extra_feedback_row[0]  # This will give you the string directly
                else:
                    extra_feedback = ""  
                  

        except Exception as e:
            flash(f"Error fetching data: {str(e)}", "danger")
        finally:
            connection.close()

    # Render the template with all the fetched data
    return render_template(
        'principlepast.html',
        assessments=assessments,
        teaching_data=teaching_data,
        feedback_data=feedback_data,
        dept_act_data=dept_act_data,
        inst_act_data=inst_act_data,
        society_data=society_data,
        points_data=points_data,
        hodas_data=hodas_data,
        extra_feedback=extra_feedback,
        self_improvement_data=self_improvement_data,
        certification_data=certification_data,
        title_data=title_data,
        resource_data=resource_data,
        committee_data=committee_data,
        project_data=project_data,
        contribution_data=contribution_data,
        selected_year=selected_year,
        user_name=user_name, user_id=user_id
    )



@app.route('/principledash')
def principledash():
    user_id = session.get('user_id')
    department = request.args.get('department')
    return render_template('principaldash.html')


@app.route('/get_performers_with_hod', methods=['POST'])
def get_performers_with_hod():
    acad_years = request.json['academic_year']
    dept = request.json['department']

    print(f"Received academic year: {acad_years}, department: {dept}")  # Debug log

    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, total, hodtotal FROM total
        WHERE acad_years = %s AND dept = %s
        ORDER BY total DESC
        LIMIT 5
    """, (acad_years, dept))

    results = cursor.fetchall()
    print(f"Query Results: {results}")  # Debug log

    # Prepare the response with name, total, and hodtotal
    performers = [{'name': row[0], 'total': row[1], 'hodtotal': row[2]} for row in results]

    # If fewer than 5 results, pad with empty entries
    while len(performers) < 5:
        performers.append({'name': '', 'total': 0, 'hodtotal': 0})

    cursor.close()
    return jsonify(performers)

# Reuse the after_request handler to prevent caching
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response



@app.route('/forgotpass')
def forgotpass():
    return render_template('forgotpass.html')


def generate_reset_token(email):
    return s.dumps(email, salt='password-reset-salt')

def send_reset_email(user_email):
    print(f"Sending email to {user_email}")  # Debug line
    token = generate_reset_token(user_email)
    reset_link = url_for('reset_with_token', token=token, _external=True)

    message = f'''
    Hi,
    To reset your password, click the following link:
    {reset_link}
    
    If you did not request this, please ignore this email.
    '''

    try:
        mail.send_message(subject='Password Reset Request', recipients=[user_email], body=message)
        print("Email sent successfully!")  # Debug line
    except Exception as e:
        print(f"Failed to send email: {e}")  # Debug line




@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)  # Token expires in 1 hour
    except Exception as e:
        return render_template('error.html', message='The reset link is invalid or has expired.')

    if request.method == 'POST':
        new_password = request.form['password']

        connection = connect_to_database()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE users SET password = %s WHERE gmail = %s"
                cursor.execute(sql, (new_password, email))
                connection.commit()

            # Redirect to login with a success message
            return redirect(url_for('login', status='reset_success'))
        finally:
            connection.close()

    return render_template('reset_password.html', token=token)




@app.route('/submit-forgot-password', methods=['POST'])
def submit_forgot_password():
    email = request.form['email']

    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            # Check if the email exists in the users table
            sql = "SELECT * FROM users WHERE gmail = %s"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()

        if user:
            send_reset_email(email)  # Send reset email
            # Redirect with a success message as a query parameter
            return redirect(url_for('forgotpass', status='success'))
        else:
            # Redirect with an error message
            return redirect(url_for('forgotpass', status='error'))
    finally:
        connection.close()




app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # SMTP server for Gmail
app.config['MAIL_PORT'] = 587  # Use port 587 for TLS
app.config['MAIL_USE_TLS'] = True  # Enable TLS
app.config['MAIL_USERNAME'] = 'mayanksalvi312@gmail.com'  # Your Gmail address
app.config['MAIL_PASSWORD'] = 'lefj dkdj vkxq mhiu'  # Use an App Password if you have 2FA enabled
app.config['MAIL_DEFAULT_SENDER'] = 'mayanksalvi312@gmail.com'  # Default sender address

mail = Mail(app)


@app.route('/giveappraisal', methods=['GET'])
def give_appraisal():
    # Get the user ID from the query parameters
    user_id = request.args.get('userid')

    if not user_id:
        return jsonify({'status': 'error', 'message': 'No user ID provided.'}), 400

    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            # Fetch the user's email from the 'users' table
            sql = "SELECT gmail FROM users WHERE userid = %s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()

            if result:
                user_email = result[0]  # Access the email from the tuple
                send_appraisal_email(user_email)  # Send the email
                
                # Redirect to 'principlestaff' with success flag
                return redirect(url_for('principlestaff', success=1))  
            else:
                return jsonify({'status': 'error', 'message': 'User not found.'}), 404
    finally:
        connection.close()

def send_appraisal_email(user_email):
    """Send the appraisal approval email to the user."""
    subject = "Appraisal Approved"
    message = f'''
    Dear Employee,

    We are pleased to inform you that your appraisal form has been reviewed and approved. 
    Congratulations on your appraisal!

    Best Regards,
    HR Team
    '''
    mail.send_message(subject=subject, recipients=[user_email], body=message)



@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=False)

