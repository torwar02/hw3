'''
At the command line, run 

conda activate PIC16B-24W
export FLASK_ENV=development
flask run

# Sources

This set of lecture notes is based in part on previous materials developed by [Erin George](https://www.math.ucla.edu/~egeo/) (UCLA Mathematics) and the tutorial [here](https://stackabuse.com/deploying-a-flask-application-to-heroku/). 
'''
import sqlite3
import pandas as pd

from flask import g, Flask, render_template, request #Flask class is the most important, other things just help out
from flask import redirect, url_for, abort

app = Flask(__name__) #Making a Flask object with `__name`--all HTML files go here.

# www.google.com/
@app.route("/") # decorators #Route method of the Flask instance. Decorators are functions that modify functions.
def redirect_page():
    return redirect(url_for("submit"))


@app.route("/submit/", methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        handle, message = insert_message(request)
        return render_template('submit.html', sec = True, handle = handle, message = message)

@app.route("/view/")
def view():
    postings = random_messages(5)
    length = 5
    message_tuples = []
    for i in range(length):
        message_tuples.append(tuple(postings.iloc[i,:]))
    return render_template('view.html', message_tuples = message_tuples)
    
    
def get_message_db():
    try:
        return g.message_db
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cursor = g.message_db.cursor()
        cmd = """
        CREATE TABLE IF NOT EXISTS messages(
        handle TEXT,
        message TEXT
        );
        """
        cursor.execute(cmd)
        cursor.close()
        return g.message_db
        
def insert_message(request):
    handle = request.form['handle']
    message = request.form['message']
    db = get_message_db()
    info = pd.DataFrame([{'handle': handle, 'message' : message}])
    info.to_sql("messages", db, if_exists = "append", index = False)
    db.commit()
    db.close()
    return handle, message
    
def random_messages(n):
    db = get_message_db()
    cmd = f""" SELECT * FROM messages ORDER BY RANDOM() LIMIT {n}; """
    postings = pd.read_sql_query(cmd, db)
    db.close()
    return postings
    
