from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error

DATABASE = 'DB_FILE'

app = Flask(__name__)

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
    return render_template('home.html')


@app.route('/login',methods=['POST', 'GET'])
def render_login_page():  # put application's code here
    return render_template('login.html')


@app.route('/signup',methods=['POST', 'GET'])
def render_signup_page():  # put application's code here
    if request.method =='POST':
        fname = request.form.get('user_fname').title().strip()
        lname = request.form.get('user_lname').title().strip()
        email = request.form.get('user_email').lower().strip()
        password1 = request.form.get('user_password1')
        password2 = request.form.get('user_password2')
        if password1 != password2:
            return redirect("\signup?error=passwords+do+not+match")
        if len(password1) < 8:
            return redirect("\signup?error=password+must+be+over+8+characters")

        con = connect_database(DATABASE)
        query_insert = "INSERT INTO user (fname, lname, email, password1) VALUES (?. ?, ?, ?)"
        cur = con.cursor()
        cur.execute(query_insert, (fname, lname, email, password1))
        con.commit()
        con.close()
    return render_template('signup.html')

@app.route('/booking',methods=['POST', 'GET'])
def render_booking_page():  # put application's code here
    return render_template('booking.html')

if __name__ == '__main__':
    app.run()
