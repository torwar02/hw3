import sqlite3
import pandas as pd

from flask import Flask, g, render_template, request #Flask is most important, others are for functions
from flask import redirect, url_for

app = Flask(__name__) #Making a Flask object with `__name`--all HTML files go here.

@app.route("/") # This is a decorator
def redirect_page():
    return redirect(url_for("submit")) #Immediately take people to `submit`


@app.route("/submit/", methods=['POST', 'GET']) #Two methods (before/after post)
def submit():
    if request.method == 'GET':
        return render_template('submit.html') #Render `submit.html` as-is at first
    else:
        handle, message = insert_message(request) #When submitted, get back message info
        return render_template('submit.html', sec = True, handle = handle, message = message)
        #Return template again but with "message sent" displayed.
        
@app.route("/view/")
def view(): #For viewing messages
    postings = random_messages(5) #Get 5 random messages from database
    length = 5
    message_tuples = []
    for i in range(length):
        message_tuples.append(tuple(postings.iloc[i,:])) #Convert df rows into tuples
    return render_template('view.html', message_tuples = message_tuples) #display `view`
    
    
def get_message_db(): #create/access database
    try:
        return g.message_db #gets datbase from `g` object
    except: #should only go through here once
        g.message_db = sqlite3.connect("messages_db.sqlite") #makes database
        cursor = g.message_db.cursor()
        cmd = """
        CREATE TABLE IF NOT EXISTS messages(
        handle TEXT,
        message TEXT
        );
        """ #creates table
        cursor.execute(cmd)
        cursor.close()
        return g.message_db #then returns datbaase
        
def insert_message(request): #places messages into database
    handle = request.form['handle'] #extracts `handle`/`message` from form
    message = request.form['message']
    db = get_message_db()
    info = pd.DataFrame([{'handle': handle, 'message' : message}]) #places handle/message into df
    info.to_sql("messages", db, if_exists = "append", index = False) #places into db
    db.commit()
    db.close()
    return handle, message #sends back `handle` and `message` to `submit()`
    
def random_messages(n): #set to 5 in `view()`
    db = get_message_db()
    cmd = f""" SELECT * FROM messages ORDER BY RANDOM() LIMIT {n}; """ #grabs `n` random messages
    postings = pd.read_sql_query(cmd, db) #sent to df
    db.close()
    return postings #returned to `view()`
    
