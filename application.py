import sqlite3
from contextlib import closing
from flask import Flask, render_template, redirect, request, abort
import imghdr
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_PATH"] = "static/images"
app.config["UPLOAD_EXTENSIONS"] = ['.jpg', '.png', '.jfif', '.jpeg']

conn = sqlite3.connect("Collection.db", check_same_thread=False)


@app.route("/")
def index():
    headline = "This is a Test!"
    return render_template("index.html", headline=headline)


@app.route("/display")
def display():
    headline = "This is the Display Page!"
    with closing(conn.cursor()) as c:
        query = '''Select * From Collection'''
        c.execute(query)
        results = c.fetchall()
        images = []
        for result in results:
            images.append((result[0], result[1], result[2], result[3]))
    return render_template("display.html", headline=headline, images=images)


@app.route("/additem", methods=["GET", "POST"])
def additem():
    headline = "Choose a file to upload to the collection:"
    if request.method == 'POST':
        form = request.form.get("form")
        uploaded_file = request.files["item_picture"]
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        try:
            picture = request.form['item_picture']
            title = request.form['title']
            author = request.form['author']
            series = request.form['series']

            with closing(conn.cursor()) as c:
                query = '''INSERT INTO Collection (item_picture,item_title,item_author,item_series)
                            VALUES(?, ?, ?, ?)'''
                c.execute(query, (picture, title, author, series))

                c.commit()
                headline = "success!!"
        except sqlite3.OperationalError as e:
            print(e)
            headline = "error in insert operation"
        return render_template("additem.html", headline=headline)
    elif request.method == 'GET':
        return render_template("additem.html", headline=headline)

@app.route("/deleteitem")
def deleteitem():
    headline = "This is the Delete Item Page!"
    return render_template("deleteitem.html", headline=headline)


if __name__ == "__main__":
    app.run(debug=True)