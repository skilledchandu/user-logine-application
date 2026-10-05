from contextlib import closing
import re

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)

def connect_db():
    mydb = sqlite3.connect(DATABASE)
    mydb.execute(
        'CREATE TABLE IF NOT EXISTS LoginDetails2 '
        '(username TEXT, password TEXT, Email TEXT)'
    )
    mydb.commit()
    return mydb

@app.route("/logout")
def logout():
    name = ''
    id = ''
    msg = 'Logged Out Successfully'
    return render_template('login.html', msg=msg, name=name, id=id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        with closing(connect_db()) as mydb:
            mycursor = mydb.cursor()
            mycursor.execute('SELECT * FROM LoginDetails2 WHERE username = ? AND password = ?', (username, password))
            account = mycursor.fetchone()
        if account:
            print('login success')
            name = account[0]
            id = account[1]
            msg = 'Logged in Successfully'
            print('login successful')
            return render_template('welcome.html', msg=msg, name=name, id=id)
        else:
            msg = 'Incorrect Credentials. Kindly check'
            return render_template('login.html', msg=msg)
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        mydb = sqlite3.connect(DATABASE)
        mycursor = mydb.cursor()
        print(username)
        
        mycursor.execute('SELECT * FROM LoginDetails2 WHERE username = ? AND Email = ?', (username, email))
        account = mycursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Kindly fill the details !'
        else:
            mycursor.execute('INSERT INTO LoginDetails2 VALUES (%s, %s, %s)', (username, password, email))
            mydb.commit()
            msg = 'Your Registration is Successful'
            name = username
            return render_template('welcome.html', msg=msg, name=name)

    elif request.method == 'POST':
        msg = 'Kindly fill the details !'
        
    return render_template('registration.html', msg=msg)






app.run(debug=True)