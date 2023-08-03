from flask import Flask, render_template, redirect, request, url_for
import requests

app = Flask(__name__)

@app.route("/")
def show_list():
      resp = requests.get("http://localhost:5001/api/items")
      resp = resp.json()
      return render_template('index.html', todolist=resp)


if __name__ == "__main__":
    app.run("0.0.0.0")
