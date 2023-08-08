# RESTful API
from flask import Flask, render_template, redirect, g, request, url_for, jsonify, Response
from flask import session, flash ####
import sqlite3
import urllib
import json

DATABASE = 'todolist.db'


app = Flask(__name__)
app.config.from_object(__name__)

#############################################
app.secret_key = 'your_secret_key'
users = {
    'user1':'password1',
    'user2':'password2'
}

@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Perform authentication logic here (compare hashed passwords, etc.)
    # If authenticated, set user info in session
    if username in users and users[username]==password:
        session['username'] = username
        flash('Logged in successfully', 'success')
        return redirect(url_for('show_list'))
    else:
        flash('Invalid credentials', 'error')
        return redirect(url_for('login_page'))

@app.route("/logout")
def logout():
    session.pop('username', None)
    flash('Logged out successfully', 'info')
    return redirect(url_for('login_page'))
#####################################################

@app.route("/api/items")  # default method is GET
def get_items():
    db = get_db()
    cur = db.execute('SELECT what_to_do, due_date, status FROM entries')
    entries = cur.fetchall()
    tdlist = [dict(what_to_do=row[0], due_date=row[1], status=row[2])
              for row in entries]
    response = Response(json.dumps(tdlist),  mimetype='application/json')
    return response


@app.route("/api/items", methods=['POST'])
def add_item():
    db = get_db()
    db.execute('insert into entries (what_to_do, due_date) values (?, ?)',
               [request.json['what_to_do'], request.json['due_date']])
    db.commit()
    return jsonify({"result": True})


@app.route("/api/items/<item>", methods=['DELETE'])
def delete_item(item):
    item = urllib.parse.unquote(item)
    db = get_db()
    db.execute("DELETE FROM entries WHERE what_to_do='"+item+"'")
    db.commit()
    return jsonify({"result": True})


@app.route("/api/items/<item>", methods=['PUT'])
def update_item(item):
    # we do not need the body so just ignore it
    item = urllib.parse.unquote(item)
    db = get_db()
    db.execute("UPDATE entries SET status='done' WHERE what_to_do='"+item+"'")
    db.commit()
    return jsonify({"result": True})


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


if __name__ == "__main__":
    app.run("0.0.0.0", port=5001)
