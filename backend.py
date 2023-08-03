from flask import Flask, g, jsonify, render_template, redirect, request, url_for
import sqlite3

DATABASE = 'todolist.db'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/api/items", methods=["GET"])
def show_list():
    db = get_db()
    cur = db.execute('SELECT what_to_do, due_date, status FROM entries')
    entries = cur.fetchall()
    tdlist = [dict(what_to_do=row[0], due_date=row[1], status=row[2])
              for row in entries]
    return jsonify(tdlist)

@app.route("/api/add", methods=["POST"])
def add_entry():
    db = get_db()
    data = request.get_json()  # Assuming the frontend sends JSON data
    db.execute('INSERT INTO entries (what_to_do, due_date) VALUES (?, ?)',
               (data['what_to_do'], data['due_date']))
    db.commit()
    return jsonify({"message": "Entry added successfully"})


@app.route("/api/delete/<item>", methods=["DELETE"])
def delete_entry(item):
    db = get_db()
    db.execute("DELETE FROM entries WHERE what_to_do=?", (item,))
    db.commit()
    return jsonify({"message": "Entry deleted successfully"})


@app.route("/api/mark/<item>", methods=["PUT"])
def mark_as_done(item):
    db = get_db()
    db.execute("UPDATE entries SET status='done' WHERE what_to_do=?", (item,))
    db.commit()
    return jsonify({"message": "Entry marked as done"})


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

if __name__ == "__main__":
    #app.run("localhost", 5001)
    app.run("0.0.0.0", port=80)



