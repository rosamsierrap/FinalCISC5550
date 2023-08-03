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

if __name__ == "__main__":
    app.run("localhost", 5001)



