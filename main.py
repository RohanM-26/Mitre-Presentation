from flask import Flask, session, render_template, redirect, url_for, request, g

import sqlite3
import datetime
app = Flask('app')
FLASK_ENV = 'development'
app.secret_key = "CHANGE ME"
import random


def get_connection():
    connection = getattr(g, '_database', None)
    if connection is None:
        connection = g._database = sqlite3.connect("database.db")
        connection.row_factory = sqlite3.Row
    return connection

def get_course_catalog():
    cursor = get_connection().cursor()
    cursor.execute("SELECT * FROM course LEFT JOIN prerequisite ON course.course_num = prerequisite.course_num")
    course_catalog = cursor.fetchall()
    # Marks duplicates in query. Occurs due to table set up #
    seen_courses = set()
    for course in course_catalog:
        dept_course_key = (course['dept'], course['course_num'])
        if dept_course_key in seen_courses:
            course_with_duplicate = tuple(course) + (True,)
        else:
            seen_courses.add(dept_course_key)
            course_with_duplicate = tuple(course) + (False,) 
        yield course_with_duplicate
    #--------------------------------------------------------#
    return course_catalog

def create_account(first_name, last_name, email, username, password, address):
    cursor = get_connection().cursor()
    cursor.execute('INSERT INTO User (username, password, fname, lname) VALUES (?, ?, ?, ?)')
    cursor.commit()
    cursor.close()
    return True


@app.route('/', methods = ['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']

        cursor = get_connection().cursor()

        cursor.execute("SELECT * FROM user_credentials WHERE user = ? AND pass = ?", (username, password,))
        user_credentials = cursor.fetchone()
        if (user_credentials):
            # creating session variables for user_credentials table values #
            session['username'] = user_credentials['user']
            session['user_id']  = user_credentials['user_id']
            
            # join tables to match user_credentials to user_information #
            cursor.execute("SELECT user_information.* FROM user_credentials JOIN user_information ON user_credentials.user_id = user_information.user_id WHERE user_credentials.user = ?", (session['username'],))
            user_information = cursor.fetchone()
            # creating session variables for user_information table values # 
            session['first_name'] = user_information['first_name']
            session['last_name'] = user_information['last_name']
            session['access'] = user_information['type']
            session['email'] = user_information['email']
            session['address'] = user_information['address']
            # creating session variables based on access level of user
            if(session['access'] == 3):
                cursor.execute("SELECT * FROM graduate_student WHERE graduate_student.user_id = ?", (session['user_id'],))
                user_role = cursor.fetchone()
                session['university_id'] = user_role['university_id']
                session['advisor_id'] = user_role['advisor_id']
                session['type_of_program'] = user_role['type_of_program']
                session['area_of_study'] = user_role['area_of_study']
                session['cleared'] = user_role['cleared']
                session['gpa'] = user_role['gpa']
            if(session['access'] == 4):
                cursor.execute("SELECT * FROM alumni WHERE alumni.user_id = ?", (session['user_id'],))
                user_role = cursor.fetchone()
                session['university_id'] = user_role['university_id']
                session['type_of_program'] = user_role['type_of_program']
                session['area_of_study'] = user_role['area_of_study']
                session['gpa'] = user_role['gpa']
                session['year_of_graduation'] = user_role['year_of_graduation']
            return redirect(url_for('home'))
        else:
            message = "Invalid login credentials. Please try again"
            return render_template('login.html', message = message)
    return render_template('login.html', message = 0)

@app.route('/create', methods = ['GET','POST'])
def create():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']

        create_account(first_name, last_name, email, username, password, address)
    return render_template('create.html', user_id = session['user_id'], username = session['username'], first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session ['address'])


@app.route('/signup', methods = ['GET','POST'])
def signup():
    if(request.method == 'POST'):
        username = request.form['username']

        cursor = get_connection().cursor()
        cursor.execute("SELECT user FROM user_credentials WHERE user = ?", (username,))

        user_credentials = cursor.fetchone()

        if(user_credentials):
            message = f"User with username {username} already exists. Please login or try a new username."
            return render_template('signup.html', message = message, status = False)
        else:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = request.form['password']
            address = request.form['address']
            if(not first_name.strip() or not last_name.strip() or not email.strip() or not username.strip() or not password.strip() or not address.strip()):
                message = "Please fill in all fields."
                return render_template("signup.html", message = message, status = False)
            else:
                cursor = get_connection().cursor()
                cursor.execute("SELECT count(first_name) FROM user_information")
                user_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO user_credentials VALUES (?, ?, ?)", (username, password, user_id,))
                cursor.execute("INSERT INTO user_information VALUES (?, ?, ?, ?, ?, ?)", (first_name, last_name, 3, email, address, user_id))   
                new = True
                while new:
                    random_number = random.randint(0, 99999999)
                    string_random_number = str(random_number)
                    cursor.execute("SELECT * FROM graduate_student WHERE university_id = ?", (string_random_number,))
                    gs = cursor.fetchone()
                    if(not gs):
                        cursor.execute("SELECT * FROM alumni WHERE university_id = ?", (string_random_number,))
                        a = cursor.fetchone()
                        if(not a):
                            new = False
                cursor.execute("INSERT INTO graduate_student VALUES (?, ?, ?, ?, ?, ?, ?)", (string_random_number, user_id, 2, 'MS', 'Computer Science', 0, '0.0'))
                get_connection().commit()
                message = "Account has been created successfully"
                return render_template("login.html", message = message, status = True)
    return render_template('signup.html')


@app.route('/home', methods = ['GET', 'POST'])
def home():
    if 'username' in session:
        return render_template('home.html', user_id = session['user_id'], username = session['username'], first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session ['address'])
    else:
        return render_template('signup.html')

@app.route('/course_catalog', methods = ['GET', 'POST'])
def course_catalog():
    course_catalog = list(get_course_catalog())
    return render_template('course_catalog.html', course_catalog = course_catalog, first_name = session['first_name'], last_name = session['last_name'], access = session['access'], len = len(course_catalog))

@app.route('/taken_course_and_requirements', methods = ['GET', 'POST'])
def taken_course_and_requirements():
    cursor = get_connection().cursor()
    cursor.execute("SELECT * FROM course_taken WHERE course_taken.university_id = ?", (session['university_id'],))
    taken_courses = cursor.fetchall()
    return render_template('taken_course_and_requirements.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], type_of_program = session['type_of_program'], taken_courses = taken_courses)

@app.route('/forms', methods = ['GET', 'POST'])
def forms():
    course_catalog = list(get_course_catalog())
    if(request.method == 'POST'):
        form_one = []
        for course in course_catalog:
            course_name = "select/" + str(course[0]) + "/" + str(course[1])
            course_form_name = request.form.get(course_name)
            if(course_form_name):
                form_one.append(course)
        if(not form_one):
            message = f"Please do not submit an empty form!"
            return render_template('forms.html', course_catalog = course_catalog, first_name = session['first_name'], last_name = session['last_name'], access = session['access'], len = len(course_catalog), message = message, type_of_program = session['type_of_program'])
        cursor = get_connection().cursor()
        cursor.execute("INSERT INTO forms (submitted_university_id) VALUES (?)", (session['university_id'],))
        get_connection().commit()
        cursor.execute("SELECT form_id FROM forms WHERE forms.submitted_university_id = ? ORDER BY form_id DESC LIMIT 1", (session['university_id'],))
        form_id = cursor.fetchone()[0]
        for course in form_one:
            cursor.execute("INSERT INTO forms_classes (form_id, university_id, dept, course_num) VALUES (?, ?, ?, ?)", (form_id, session['university_id'], course[0], course[1]))
            get_connection().commit()
        if(session['type_of_program'] == 'PhD'):
            if(request.form['large-text']):
                thesis = request.form['large-text']
                cursor.execute("INSERT INTO thesis (form_id, thesis, submitted_university_id) VALUES (?, ?, ?)", (form_id, thesis, session['university_id']))
                get_connection().commit()
        message = f"You have successfully submitted your form 1!"
        return render_template('forms.html', course_catalog = course_catalog, first_name = session['first_name'], last_name = session['last_name'], access = session['access'], len = len(course_catalog), message = message,  type_of_program = session['type_of_program'])


    return render_template('forms.html', course_catalog = course_catalog, first_name = session['first_name'], last_name = session['last_name'], access = session['access'], len = len(course_catalog), type_of_program = session['type_of_program'])

@app.route('/students', methods = ['GET', 'POST'])
def students():
    if request.method == 'POST':
        if request.args.get('approved') == 'True':
            student_id = request.form['student_id']
            cursor = get_connection().cursor()
            cursor.execute("SELECT * FROM graduate_student WHERE user_id = ?", (student_id,)) 
            student = cursor.fetchone()
            yog = datetime.datetime.now().year
            university_id = student['university_id']
            gpa = student['gpa']
            type_of_program = student['type_of_program']
            area_of_study = student['area_of_study']
            cursor.execute("UPDATE graduation_application SET approved = ? WHERE submitted_university_id = ?", (1, university_id))
            cursor.execute("UPDATE user_information SET type = ? WHERE user_id = ?", (4, student_id))
            cursor.execute("DELETE FROM graduate_student WHERE user_id = ?", (student_id,))
            cursor.execute("INSERT INTO alumni VALUES (?, ?, ?, ?, ?, ?)", (university_id, student_id, yog, type_of_program, area_of_study, gpa))
            get_connection().commit()
        else: 
            advisor_id = int(request.form['advisor'])
            student_id = request.form['student_id']
            cursor = get_connection().cursor() 
            cursor.execute("UPDATE graduate_student SET advisor_id = ? WHERE university_id = ?", (advisor_id, student_id))
            get_connection().commit()
    cursor = get_connection().cursor()
    cursor.execute("SELECT * FROM user_information u JOIN graduate_student gs ON u.user_id = gs.user_id LEFT JOIN forms f ON gs.university_id = f.submitted_university_id WHERE u.type = 3")
    students = cursor.fetchall()
    cursor.execute("SELECT * FROM user_information WHERE type = 2")
    advisors = cursor.fetchall()
    return render_template('users.html', type = "student", users = students, first_name = session['first_name'], last_name = session['last_name'], access = session['access'], advisors = advisors)

@app.route('/advisors')
def advisors():
    cursor = get_connection().cursor()
    cursor.execute("SELECT * FROM user_information WHERE type = 2")
    information = cursor.fetchall()
    return render_template('users.html', type = "advisors", users = information, first_name = session['first_name'], last_name = session['last_name'], access = session['access'])

@app.route('/assign', methods = ['GET', 'POST'])
def assign():
    user_id = -1
    error = ""
    if request.method == 'POST':
        role = int(request.form['role'])
        prev_role = int(request.form['prev_role'])
        user_id = request.form['user_id']
        program = request.form['program']
        major = request.form['major']
        cursor = get_connection().cursor() 
        if (role == 0 and prev_role != 0 and prev_role != 3):
            cursor.execute("INSERT INTO systems_administrator VALUES (?)", (user_id))
        elif (role == 1 and prev_role != 1 and prev_role != 3):
            cursor.execute("INSERT INTO grad_secretary VALUES (?)", (user_id))
        elif (role == 2 and prev_role != 2 and prev_role != 3):
            cursor.execute("INSERT INTO faculty_advisor VALUES (?)", (user_id))
        elif (role == 3 and prev_role == 5 and prev_role != 3):
            cursor.execute("SELECT count(user_id) FROM graduate_student")
            count = cursor.fetchone()[0]
            id = str(100000000 + int(count))
            id_cut = id[1:]
            cursor.execute("INSERT INTO graduate_student VALUES (?, ?, ?, ?, ?, ?, ?)", (id_cut, user_id, None, program, major, 0, 4.0))
        elif (role == 3):
            error = "students must apply through the home page (user must be type: \"No Role\")"
        elif (prev_role == 3):
            error = "students must graduate to change roles"
        elif (prev_role == role):
            error = "do not try to change user to the same role"
        if prev_role == 0 and len(error) < 1:
            cursor.execute("DELETE FROM systems_administrator WHERE sys_admin_id = ?", (user_id,))
        elif prev_role == 1 and len(error) < 1:
            cursor.execute("DELETE FROM grad_secretary WHERE secretary_id = ?", (user_id,))
        elif prev_role == 2 and len(error) < 1:
            cursor.execute("DELETE FROM faculty_advisor WHERE faculty_advisor_id = ?", (user_id,))
        if len(error) < 1:
            cursor.execute("UPDATE user_information SET type = ? WHERE user_id = ?", (role, user_id,))
            error = "success!"
        get_connection().commit()
    cursor = get_connection().cursor()
    cursor.execute("SELECT * FROM user_information ORDER BY type DESC")
    information = cursor.fetchall()
    return render_template('assign.html', information = information, first_name = session['first_name'], last_name = session['last_name'], access = session['access'], error = error, person = user_id)

@app.route('/studentprofile/<id>', methods = ['GET', 'POST'])
def preview(id):
    cursor = get_connection().cursor()
    cursor.execute("SELECT * FROM course_taken WHERE course_taken.university_id = (SELECT university_id FROM graduate_student WHERE user_id = ? )", (id,))
    taken_courses = cursor.fetchall()
    cursor.execute("SELECT * FROM user_information LEFT JOIN graduate_student ON user_information.user_id = graduate_student.user_id WHERE user_information.user_id = ?", (id,))
    student = cursor.fetchone()
    first_name = student['first_name']
    last_name = student['last_name'] 
    user_id = student['user_id'] 
    access = session['access']
    stud_access = student['type']
    email = student['email']
    address = student['address']
    university_id = student['university_id']
    gpa = student['gpa']
    type_of_program = student['type_of_program']
    area_of_study = student['area_of_study']
    return render_template('profile.html', first_name = first_name, last_name = last_name, access = access, email = email, address = address, university_id = university_id, gpa = gpa, type_of_program = type_of_program, area_of_study = area_of_study, taken_courses = taken_courses, preview = 1, stud_access = stud_access, user_id = user_id)

@app.route('/list_of_advisees', methods=['GET', 'POST'])
def list_of_advisees():
    cursor = get_connection().cursor()
    cursor.execute("SELECT * FROM graduate_student LEFT JOIN user_information ON graduate_student.user_id = user_information.user_id WHERE graduate_student.advisor_id = ?", (session['user_id'],))
    list_of_advisees = cursor.fetchall()
    if(request.method == 'POST'):
        selected_advisee_id = request.form.get('selected_advisee_id')
        if(selected_advisee_id):
            cursor = get_connection().cursor()
            cursor.execute("SELECT * FROM graduate_student JOIN user_information ON user_information.user_id = graduate_student.user_id WHERE graduate_student.university_id = ?", (selected_advisee_id,))
            selected_student = cursor.fetchone()
            cursor = get_connection().cursor()
            cursor.execute("SELECT * FROM course_taken WHERE course_taken.university_id = ?", (selected_advisee_id,))
            taken_courses = cursor.fetchall()
            cursor = get_connection().cursor()
            cursor.execute("SELECT * FROM forms WHERE forms.submitted_university_id = ? ORDER BY form_id DESC LIMIT 1", (selected_advisee_id,))
            latest_form = cursor.fetchone()
            cursor = get_connection().cursor()
            cursor.execute("SELECT * FROM graduation_application WHERE graduation_application.submitted_university_id = ? ORDER BY form_id DESC LIMIT 1", (selected_advisee_id,))
            graduation_application = cursor.fetchone()
            return render_template('list_of_advisees.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], list_of_advisees = list_of_advisees, selected_student = selected_student, taken_courses = taken_courses, latest_form = latest_form, graduation_application = graduation_application)
    return render_template('list_of_advisees.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], list_of_advisees = list_of_advisees)

@app.route('/review_forms',methods=['GET', 'POST'])
def review_forms():
    thesis = None
    cursor = get_connection().cursor()
    cursor.execute("SELECT * FROM forms LEFT JOIN graduate_student ON graduate_student.university_id = forms.submitted_university_id JOIN user_information ON user_information.user_id = graduate_student.user_id WHERE (submitted_university_id, form_id) IN (SELECT submitted_university_id, MAX(form_id) FROM forms GROUP BY submitted_university_id)")
    list_of_latest_forms = cursor.fetchall()
    if(request.args.get('selected_student_id')):
        selected_student_id = request.args.get('selected_student_id')
        cursor = get_connection().cursor()
        cursor.execute("SELECT * FROM forms WHERE forms.submitted_university_id = ? ORDER BY form_id DESC LIMIT 1", (selected_student_id,))
        form = cursor.fetchone()
        cursor.execute("SELECT * FROM forms_classes WHERE form_id = ?", (form[0],))
        forms_classes = cursor.fetchall()
        cursor.execute("SELECT * FROM graduate_student JOIN user_information ON graduate_student.user_id = user_information.user_id WHERE graduate_student.university_id = ?", (selected_student_id,))
        advisee_information = cursor.fetchone()
        if(advisee_information[3] == 'PhD'):
            cursor.execute("SELECT * FROM thesis WHERE thesis.submitted_university_id = ? ORDER BY form_id DESC LIMIT 1", (selected_student_id,))
            thesis = cursor.fetchone()
        return render_template('review_forms.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], list_of_forms = list_of_latest_forms, selected_student = selected_student_id, advisee_information = advisee_information, forms_classes = forms_classes, form = form, thesis = thesis)
    if(request.method == 'POST'):
        selected_advisee_id = request.form.get('selected_advisee_id')
        approve = request.form.get('approve')
        if(selected_advisee_id):
            cursor = get_connection().cursor()
            cursor = get_connection().cursor()
            cursor.execute("SELECT * FROM forms WHERE forms.submitted_university_id = ? ORDER BY form_id DESC LIMIT 1", (selected_advisee_id,))
            form = cursor.fetchone()
            cursor.execute("SELECT * FROM forms_classes WHERE form_id = ?", (form[0],))
            forms_classes = cursor.fetchall()
            cursor.execute("SELECT * FROM graduate_student JOIN user_information ON graduate_student.user_id = user_information.user_id WHERE graduate_student.university_id = ?", (selected_advisee_id,))
            advisee_information = cursor.fetchone()
            if(advisee_information[3] == 'PhD'):
                cursor.execute("SELECT * FROM thesis WHERE thesis.submitted_university_id = ? ORDER BY form_id DESC LIMIT 1", (selected_advisee_id,))
                thesis = cursor.fetchone()
            return render_template('review_forms.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], list_of_forms = list_of_latest_forms, selected_student = selected_advisee_id, advisee_information = advisee_information, forms_classes = forms_classes, form = form, thesis = thesis)
        elif(approve):
            form_id = request.args.get('form_id')
            cursor = get_connection().cursor()
            cursor.execute('UPDATE forms SET approved = ? WHERE form_id = ?', (1, form_id))
            get_connection().commit()
    return render_template('review_forms.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], list_of_forms = list_of_latest_forms)


@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    thesis = None
    form_id = None
    forms_classes = None
    logout = request.args.get('logout')
    apply_to_graduate = request.args.get('apply_to_graduate')
    if(session['access'] == 3 or session['access'] == 4):
        if(session['type_of_program'] == 'PhD'):
            cursor = get_connection().cursor()
            cursor.execute("SELECT * FROM thesis WHERE thesis.submitted_university_id = ? ORDER BY form_id DESC LIMIT 1", (session['university_id'],))
            thesis = cursor.fetchone()
        if(session['access'] == 3):
            cursor = get_connection().cursor()
            cursor.execute("SELECT * FROM forms WHERE forms.submitted_university_id = ? ORDER BY form_id DESC LIMIT 1", (session['university_id'],))
            latest_form = cursor.fetchone()
            if(not latest_form):
                form = 'none'
            else:
                approved = latest_form['approved']
                cursor.execute("SELECT * FROM forms WHERE submitted_university_id = ? ORDER BY form_id DESC LIMIT 1", (session['university_id'],))
                form_id = cursor.fetchone()[0]
                cursor.execute("SELECT * FROM forms_classes WHERE form_id = ?", (form_id,))
                forms_classes = cursor.fetchall()
                if(approved == 0):
                    form = 'pending'
                else:
                    form = 'approved'
            cursor.execute("SELECT * FROM graduation_application WHERE graduation_application.submitted_university_id = ? ORDER BY form_id DESC LIMIT 1", (session['university_id'],))
            latest_application = cursor.fetchone()
            if(not latest_application):
                cleared = 'none'
            else:
                approved = latest_application['approved']
                if(approved == 0):
                    cleared = 'pending'
                else:
                    cleared = 'approved'
        cursor = get_connection().cursor()
        cursor.execute("SELECT * FROM course_taken WHERE course_taken.university_id = ?", (session['university_id'],))
        taken_courses = cursor.fetchall()
    if(request.method == 'POST'):
        if(logout):
            [session.pop(key) for key in list(session.keys())]
            session.clear()
            message = f"You have logged out successfully."
            return render_template('login.html', message = message, status =  True)
        elif(apply_to_graduate):
            cursor = get_connection().cursor()
            cursor.execute("SELECT * FROM forms WHERE forms.submitted_university_id = ? ORDER BY form_id DESC LIMIT 1", (session['university_id'],))
            latest_form = cursor.fetchone()
            if(not latest_form):
                message = f"You have not submitted a form 1!"
                return render_template('profile.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session['address'], university_id = session['university_id'], gpa = session['gpa'], type_of_program = session['type_of_program'], area_of_study = session['area_of_study'], taken_courses = taken_courses, message = message, status = False, form = form, cleared = cleared, form_id = form_id, forms_classes = forms_classes)
            elif(latest_form['approved'] == 0):
                message = f"Your form 1 has not been approved!"
                return render_template('profile.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session['address'], university_id = session['university_id'], gpa = session['gpa'], type_of_program = session['type_of_program'], area_of_study = session['area_of_study'], taken_courses = taken_courses, message = message, status = False, form = form, cleared = cleared, form_id = form_id, forms_classes = forms_classes)
            cursor.execute("SELECT course_taken.dept, course_taken.course_num FROM course_taken WHERE course_taken.university_id = ? AND course_taken.grade != 'IP'", (session['university_id'],))
            courses_taken = cursor.fetchall()
            cursor.execute("SELECT forms_classes.dept, forms_classes.course_num FROM forms_classes WHERE forms_classes.university_id = ?", (session['university_id'],))
            courses_on_form = cursor.fetchall()
            courses_on_form_set = set(courses_on_form)
            courses_taken_set = set(courses_taken)
            if(not courses_on_form_set.issubset(courses_taken_set)):
                message = f"You have not taken all the courses listed on your form 1!"
                return render_template('profile.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session['address'], university_id = session['university_id'], gpa = session['gpa'], type_of_program = session['type_of_program'], area_of_study = session['area_of_study'], taken_courses = taken_courses, message = message, status = False, form = form, cleared = cleared, form_id = form_id, forms_classes = forms_classes, thesis = thesis)
            if(session['type_of_program'] == 'MS'):
                cursor.execute("SELECT MS_required_courses.dept, MS_required_courses.course_num FROM MS_required_courses")
                required_courses = cursor.fetchall()
                required_courses_set = set(required_courses)
                if(not required_courses_set.issubset(courses_taken)):
                    message = f"You have not taken all the required courses!"
                    return render_template('profile.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session['address'], university_id = session['university_id'], gpa = session['gpa'], type_of_program = session['type_of_program'], area_of_study = session['area_of_study'], taken_courses = taken_courses, message = message, status = False, form = form, cleared = cleared, form_id = form_id, forms_classes = forms_classes, thesis = thesis)
                cursor.execute("SELECT * FROM MS_requirements")
                MS_requirements = cursor.fetchone()
                if(float(session['gpa']) < float(MS_requirements['min_gpa'])):
                    message = f"You do not meet the GPA requirement!"
                    return render_template('profile.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session['address'], university_id = session['university_id'], gpa = session['gpa'], type_of_program = session['type_of_program'], area_of_study = session['area_of_study'], taken_courses = taken_courses, message = message, status = False, form = form, cleared = cleared, form_id = form_id, forms_classes = forms_classes, thesis = thesis)
                total_credits = 0
                courses_outside_of_CS = 0
                grades_below_B = 0
                cursor.execute("SELECT * FROM course_taken WHERE course_taken.university_id = ? AND course_taken.grade != 'IP'", (session['university_id'],))
                courses_taken = cursor.fetchall()
                for course in courses_taken:
                    total_credits += course[4]
                    if(course[1] != 'CSCI'):
                        courses_outside_of_CS += 1
                    if(course[6] != 'A' and course[6] != 'A-' and course[6] != 'B+' and course[6] != 'B'):
                        grades_below_B += 1
                if(total_credits < MS_requirements['min_credit_hours']):
                    message = f"You do not meet the minimum credit hours requirement!"
                    return render_template('profile.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session['address'], university_id = session['university_id'], gpa = session['gpa'], type_of_program = session['type_of_program'], area_of_study = session['area_of_study'], taken_courses = taken_courses, message = message, status = False, form = form, cleared = cleared, form_id = form_id, forms_classes = forms_classes, thesis = thesis)
                elif(courses_outside_of_CS > MS_requirements['most_courses_outside_CS']):
                    message = f"You have taken too many courses outside of CS!"
                    return render_template('profile.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session['address'], university_id = session['university_id'], gpa = session['gpa'], type_of_program = session['type_of_program'], area_of_study = session['area_of_study'], taken_courses = taken_courses, message = message, status = False, form = form, cleared = cleared, form_id = form_id, forms_classes = forms_classes, thesis = thesis)
                elif(grades_below_B > MS_requirements['most_grades_below_B']):
                    message = f"You have too many grades below a B!"
                    return render_template('profile.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session['address'], university_id = session['university_id'], gpa = session['gpa'], type_of_program = session['type_of_program'], area_of_study = session['area_of_study'], taken_courses = taken_courses, message = message, status = False, form = form, cleared = cleared, form_id = form_id, forms_classes = forms_classes,thesis = thesis)
                message = f"Your application to graduate has been successfully submitted! A graduate secretary will formally process your application."
                cursor.execute("INSERT INTO graduation_application (submitted_university_id, approved) VALUES (?, ?)", (session['university_id'], 0))
                cursor.execute("UPDATE graduate_student SET cleared = ? WHERE university_id = ?", (1, session['university_id']))    
                get_connection().commit()
                return render_template('profile.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session['address'], university_id = session['university_id'], gpa = session['gpa'], type_of_program = session['type_of_program'], area_of_study = session['area_of_study'], taken_courses = taken_courses, message = message, status = False, form = form, cleared = cleared, form_id = form_id, forms_classes = forms_classes, thesis = thesis)
            elif(session['type_of_program'] == 'PhD'):
                cursor.execute("SELECT * FROM PhD_requirements")
                PhD_requirements = cursor.fetchone()
                if (float(session['gpa']) < float(PhD_requirements['min_gpa'])):
                    message = f"You do not meet the GPA requirement!"
                    return render_template('profile.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session['address'], university_id = session['university_id'], gpa = session['gpa'], type_of_program = session['type_of_program'], area_of_study = session['area_of_study'], taken_courses = taken_courses, message = message, status = False, form = form, cleared = cleared, form_id = form_id, forms_classes = forms_classes, thesis = thesis)
                total_credits = 0
                credit_in_cs = 0
                grades_below_B = 0
                cursor.execute("SELECT * FROM course_taken WHERE course_taken.university_id = ? AND course_taken.grade != 'IP'", (session['university_id'],))
                courses_taken = cursor.fetchall()
                for course in courses_taken:
                    total_credits += course[4]
                    if(course[1] == 'CSCI'):
                        credit_in_cs += course[4]
                    if(course[6] != 'A' and course['grade'] != 'A-' and course['grade'] != 'B+' and course['grade'] != 'B'):
                        grades_below_B += 1
                if(total_credits < PhD_requirements['min_credit_hours']):
                    message = f"You do not meet the minimum courses outside of CS!"
                    return render_template('profile.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session['address'], university_id = session['university_id'], gpa = session['gpa'], type_of_program = session['type_of_program'], area_of_study = session['area_of_study'], taken_courses = taken_courses, message = message, status = False, form = form, cleared = cleared, form_id = form_id, forms_classes = forms_classes, thesis = thesis)
                elif(credit_in_cs < PhD_requirements['min_credits_in_cs']):
                    message = f"You do not meet the minimum credits in cs!"
                    return render_template('profile.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session['address'], university_id = session['university_id'], gpa = session['gpa'], type_of_program = session['type_of_program'], area_of_study = session['area_of_study'], taken_courses = taken_courses, message = message, status = False, form = form, cleared = cleared, form_id = form_id, forms_classes = forms_classes, thesis = thesis)
                elif(grades_below_B > PhD_requirements['most_grades_below_B']):
                    message = f"You have too many grades below a B!"
                    return render_template('profile.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session['address'], university_id = session['university_id'], gpa = session['gpa'], type_of_program = session['type_of_program'], area_of_study = session['area_of_study'], taken_courses = taken_courses, message = message, status = False, form = form, cleared = cleared, form_id = form_id, forms_classes = forms_classes, thesis = thesis)
                message = f"Your application to graduate has been successfully submitted! A graduate secretary will formally process your application."
                cursor.execute("INSERT INTO graduation_application (submitted_university_id, approved) VALUES (?, ?)", (session['university_id'], 0))
                cursor.execute("UPDATE graduate_student SET cleared = ? WHERE university_id = ?", (1, session['university_id']))
                get_connection().commit()
                return render_template('profile.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session['address'], university_id = session['university_id'], gpa = session['gpa'], type_of_program = session['type_of_program'], area_of_study = session['area_of_study'], taken_courses = taken_courses, message = message, status = False, form = form, cleared = cleared, form_id = form_id, forms_classes = forms_classes, thesis = thesis)
        else:
            if(request.form['email'] and request.form['email'].strip()):
                updated_email = request.form['email']
                session['email'] = updated_email
                cursor = get_connection().cursor()
                cursor.execute("UPDATE user_information SET email = ? WHERE user_id = ?", (session['email'], session['user_id']))
            if(request.form['address'] and request.form['address'].strip()):
                updated_address = request.form['address']
                session['address'] = updated_address
                cursor = get_connection().cursor()
                cursor.execute("UPDATE user_information SET address = ? WHERE user_id = ? ", (session['address'], session['user_id']))
            get_connection().commit()
    if(session['access'] == 3):
        return render_template('profile.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session['address'], university_id = session['university_id'], gpa = session['gpa'], type_of_program = session['type_of_program'], area_of_study = session['area_of_study'], taken_courses = taken_courses, form = form, cleared = cleared, form_id = form_id, forms_classes = forms_classes, thesis = thesis)
    if(session['access'] == 4):
        return render_template('profile.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session['address'], university_id = session['university_id'], gpa = session['gpa'], type_of_program = session['type_of_program'], area_of_study = session['area_of_study'], year_of_graduation = session['year_of_graduation'], taken_courses = taken_courses, thesis = thesis)
    return render_template('profile.html', first_name = session['first_name'], last_name = session['last_name'], access = session['access'], email = session['email'], address = session['address'])

app.run(host='0.0.0.0', port=8080, debug = True) 