from flask import Flask, render_template, request, redirect, url_for, session, flash


app = Flask(__name__)

@app.route("/logout")
def logout():
    name = ''
    id = ''
    msg = 'Logged Out Successfully'
    return render_template('login.html', msg=msg, name=name, id=id)


app.run(debug=True)