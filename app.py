from enum import nonmember

from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

app.secret_key = "secret_key"
DATABASE = 'DB_FILE'


def connect_database(db_file):
    """
    Creates a connection to the database.
    :param db_file:
    :return: conn
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
    return

@app.route('/')
def render_homepage():  # put application's code here
    username = None
    if 'user_id' in session:
        con = connect_database(DATABASE)
        cur = con.cursor()
        query = "SELECT first_name FROM user WHERE user_id = ?"
        cur.execute(query, (session['user_id'],))
        name = cur.fetchone()
        con.close()
        if name:
            username = name[0]
    return render_template('home.html', user_name=username)


@app.route('/login',methods=['POST', 'GET'])
def render_login_page():  # put application's code here\
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        password = request.form.get('user_password1')
        con = connect_database(DATABASE)
        cur = con.cursor()
        cur.execute("SELECT email, password  FROM user")
        all_emails = cur.fetchall()
        print(f"DEBUG: All emails in database: {all_emails}")
        query = "SELECT password, user_id, email, is_tutor FROM user WHERE email = ?"
        cur.execute(query,(email,))
        user_info = cur.fetchone()
        con.close()
        session["logged_in"] = True
        print(f"DEBUG: Entered email: {email}")  # Debugging email input
        print(f"DEBUG: Retrieved user_info: {user_info}")  # Debugging database result
        if user_info:
            stored_password = user_info[0]
            print(stored_password)
            print(user_info[0])
            print(password)
            if stored_password == password:
                session['user_id'] = user_info[1]
                session['email'] = user_info[2]
                session['is_tutor'] = bool(user_info[3])
                return redirect("/")
            else:
                return redirect("/login?error=Incorrect+password")
        else:
            return redirect("/login?error=Account+not+found")
    return render_template('login.html')


@app.route('/signup',methods=['POST', 'GET'])
def render_signup_page():  # put application's code here
    if request.method =='POST':
        fname = request.form.get('user_fname').title().strip()
        lname = request.form.get('user_lname').title().strip()
        email = request.form.get('user_email').lower().strip()
        password1 = request.form.get('user_password1')
        password2 = request.form.get('user_password2')
        user_role = request.form.get('user_role')
        if password1 != password2:
            return redirect("\signup?error=passwords+do+not+match")
        if len(password1) < 8:
            return redirect("\signup?error=password+must+be+over+8+characters")
        else:
            session['logged_in = True']=True
            redirect('/')
        con = connect_database(DATABASE)
        querysean = "SELECT email FROM user"
        cur = con.cursor()
        cur.execute(querysean)
        all_emails = cur.fetchall()
        if (email,) in all_emails:
            return redirect("\signup?error=email+already+in+use")
        is_tutor = 1 if user_role == "Tutor" else 0
        query_insert = "INSERT INTO user (first_name, surname, email, password, is_tutor) VALUES (?, ?, ?, ?, ?)"
        cur.execute(query_insert, (fname, lname, email, password1, is_tutor))
        con.commit()
        con.close()
        session["logged_in"] = True
        session['is_tutor'] = is_tutor
    return render_template('signup.html')

@app.route('/apply',methods=['POST', 'GET'])
def apply_session():
    if 'user_id' not in session:
        return redirect('login.html')
    session_id = request.form.get('session_id')
    tutee_id = session['user_id']
    con = connect_database(DATABASE)
    cur=con.cursor()
    query = 'INSERT INTO applications (session_id, tutee_id) VALUES (?, ?)'
    cur.execute(query, (session_id, tutee_id))
    con.commit()
    con.close()
    return redirect('/tutee')


@app.route('/logout')
def render_logout_page():
    session.clear()
    return redirect("/")

@app.route('/tutee',methods=['POST', 'GET'])
def render_tutee_page():
    con = connect_database(DATABASE)
    cur = con.cursor()
    query = "SELECT session.session_id, session.subject, session.subject_level, session.session_time, user.first_name, user.surname, user.email FROM session JOIN user ON session.fk_user_id = user.user_id"
    cur.execute(query)
    sessions = cur.fetchall()
    con.close()
    print("DEBUG: Sessions ->", sessions)
    return render_template('tutee.html', sessions=sessions)
@app.route('/tutor',methods=['POST', 'GET'])
def render_booking_page():  # put application's code here
    if request.method == 'POST':
        subject = request.form.get('subject')
        level = request.form.get('level')
        time = request.form.get('time')
        tutor_id = session.get('user_id')
        print("DEBUG: session['user_id'] =", session.get('user_id'))
        con = connect_database(DATABASE)
        cur = con.cursor()
        query_insert = "INSERT INTO session (subject, subject_level, session_time, fk_user_id) VALUES (?, ?, ?, ?)"
        cur.execute(query_insert, (subject, level, time, tutor_id))
        con.commit()
        con.close()
        return redirect("/")
    return render_template('tutor.html')


def print_all_users():
    con = connect_database(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM user;")
    rows = cur.fetchall()
    con.close()
    for row in rows:
        print(row)


if __name__ == '__main__':
    print_all_users()
    app.run()
