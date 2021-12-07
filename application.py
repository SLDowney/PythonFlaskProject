import sqlite3
from contextlib import closing
from flask import Flask, render_template, request

app = Flask(__name__)

conn = sqlite3.connect("Collection.db", check_same_thread=False)

@app.route("/")
def index():
    headline = "This is a Test!"
    return render_template("index.html", headline=headline)

@app.route("/success", methods=["POST"])
def success():
    name = request.form.get("name")
    headline = "Thanks for the submission "
    return render_template("additem.html", headline=headline, name=name)

@app.route("/display")
def display():
    headline = "This is the Display Page!"
    with closing(conn.cursor()) as c:
        query = '''Select * From Collection'''
        c.execute(query)
        results = c.fetchall()
        images = []
        for result in results:
            images.append((result[1], result[2], result[3]))
    return render_template("display.html", headline=headline, images=images)

@app.route("/additem")
def additem():
    headline = "Choose a file to upload to the collection:"
    return render_template("additem.html", headline=headline)

@app.route("/deleteitem")
def deleteitem():
    headline = "This is the Delete Item Page!"
    return render_template("deleteitem.html", headline=headline)

if __name__ == "__main__":
    app.run(debug=True)