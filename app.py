from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to connect to the SQLite database
def connect_db():
    conn = sqlite3.connect('users.db') #Create Database
    return conn

# Function to create the users table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''') #Create User Table
    conn.commit()
    conn.close()

# Function to register a new user
def register_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, password) VALUES (?, ?)
    ''', (username, password))
    conn.commit()
    conn.close()

# Function to verify user credentials
def verify_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE username = ? AND password = ?
    ''', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = verify_user(username, password)
        if user:
            session['username'] = username
            return redirect(url_for('Dashboard'))
        else:
            return 'Invalid username or password'
    return render_template('login.html',pageTitle="Login")

@app.route('/Dashboard')
def Dashboard():
   return render_template('Dashboard.html',t1=session['username'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register_user(username, password)
        session['successreg']="Your Account Created Successfully"
        return redirect(url_for('login'))
    
    return render_template('register.html',pageTitle="Register")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    create_table()  # Create the users table if it doesn't exist
    app.run(debug=True)
