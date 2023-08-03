from flask import Flask, render_template, redirect, request, url_for
import requests

app = Flask(__name__)

@app.route("/")
def show_list():
      resp = requests.get("http://localhost:5001/api/items")
      resp = resp.json()
      return render_template('index.html', todolist=resp)

@app.route("/add", methods=['POST'])
def add_entry(): # this is the counterpart of add_entry() from homework 3
    requests.post("http://localhost:5001/api/items", json={
                  "what_to_do": request.form['what_to_do'], "due_date": request.form['due_date']})
    return redirect(url_for('show_list'))

@app.route("/delete/<item>")
def delete_entry(item):
    response = requests.delete(f"http://localhost:5001/api/delete/{item}")
    return redirect("/")

@app.route("/mark/<item>")
def mark_as_done(item):
    response = requests.put(f"http://localhost:5001/api/mark/{item}")
    return redirect("/")

@app.teardown_appcontext
def close_request(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
          
if __name__ == "__main__":
    app.run("0.0.0.0", port=80)
