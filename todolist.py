# This is a simple example web app that is meant to illustrate the basics.
from flask import Flask, render_template, redirect, g, request, url_for, jsonify, json, session, flash
import urllib
import requests  # similar purpose to urllib.request, just more convenience
import os

app = Flask(__name__)
TODO_API_URL = "http://"+os.environ['TODO_API_IP']+":5001"
app.secret_key = 'your_secret_key'

@app.route("/login", methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route("/")
def show_list():
    resp = requests.get(TODO_API_URL+"/api/items")
    resp = resp.json()
    return render_template('index.html', todolist=resp)

        
# Add authentication checks for protected routes
@app.route("/add", methods=['POST'])
def add_entry():
    if 'username' in session:
        requests.post(TODO_API_URL+"/api/items", json={
                  "what_to_do": request.form['what_to_do'], "due_date": request.form['due_date']})
        return redirect(url_for('show_list'))
    else:
        flash('Please log in to add tasks', 'error')
        return redirect(url_for('login_page'))


@app.route("/delete/<item>", methods=['POST'])
def delete_entry(item):
    if 'username' in session:
        item = urllib.parse.quote(item)
        requests.delete(TODO_API_URL+"/api/items/"+item)
        return redirect(url_for('show_list'))
    else:
        flash('Please log in to delete tasks', 'error')
        return redirect(url_for('login_page'))


@app.route("/mark/<item>", methods=['POST'])
def mark_as_done(item):
    if 'username' in session:
        item = urllib.parse.quote(item)
        requests.put(TODO_API_URL+"/api/items/"+item)
        return redirect(url_for('show_list'))
    else:
        flash('Please log in to mark tasks', 'error')
        return redirect(url_for('login_page'))


if __name__ == "__main__":
    #app.run("0.0.0.0", port=80)
    app.run("0.0.0.0")
