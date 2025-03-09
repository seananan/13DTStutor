from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

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


@app.route('/signup')
def render_signup_page():  # put application's code here
    return render_template('signup.html')


if __name__ == '__main__':
    app.run()
