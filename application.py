import random
import sqlite3
from contextlib import closing
from flask import Flask, render_template, request, abort, redirect
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_PATH"] = "static/images"
app.config["UPLOAD_EXTENSIONS"] = ['.jpg', '.png', '.jfif', '.jpeg']
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024

conn = sqlite3.connect("Collection.db", check_same_thread=False)


@app.route("/")
def index():
    headline = "This is a Test!"
    with closing(conn.cursor()) as c:
        query = '''Select * From Collection'''
        c.execute(query)
        items = c.fetchall()
        itemList = []
        for item in items:
            itemList.append(item)
    itemToShow = random.choice(itemList)
    return render_template("index.html", headline=headline, itemToShow=itemToShow)


@app.route("/display")
def display():
    headline = "View your Collection in all it's glory!!"
    with closing(conn.cursor()) as c:
        query = '''Select * From Collection'''
        c.execute(query)
        results = c.fetchall()
        images = []
        for result in results:
            images.append((result[0], result[1], result[2], result[3]))
    return render_template("display.html", headline=headline, images=images)


@app.route("/success")
def success():
    headline = "Choose a file to upload to the collection:"
    return render_template("success.html", headline=headline)


@app.route("/additem", methods=["GET", "POST"])
def additem():
    headline = "Choose a file to upload to the collection:"
    if request.method == 'POST':
        uploaded_file = request.files["item_picture"]
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        try:
            title = request.form['title']
            author = request.form['author']
            series = request.form['series']

            with closing(conn.cursor()) as c:
                query = '''INSERT INTO Collection (item_picture,item_title,item_author,item_series)
                            VALUES(?, ?, ?, ?)'''
                c.execute(query, (filename, title, author, series))
                conn.commit()
                tagline = "Successfully added Item to Collection!!"
                return render_template("success.html", tagline=tagline)
        except sqlite3.OperationalError as e:
            print(e)
            headline = "Error in insert operation. Please try again."
    else:
        return render_template("additem.html", headline=headline)


@app.route("/deleteitem", methods=["GET", "POST"])
def deleteitem():
    counter = 0
    headline = "Choose a file to delete from the collection:"
    with closing(conn.cursor()) as c:
        query = '''SELECT * FROM Collection'''
        c.execute(query)
        items = c.fetchall()
        item_titles = []
        for item in items:
            item_titles.append(item)
    if request.method == 'POST':
        itemToDelete = int(request.form['item'])
        for item in item_titles:
            if itemToDelete == item[4]:
                try:
                    with closing(conn.cursor()) as c:
                        query = '''DELETE FROM Collection
                                    WHERE item_index = ?'''
                        c.execute(query, (itemToDelete,))
                        conn.commit()
                        item_titles.pop(counter)
                        if os.path.exists("static\images\\" + item[0]):
                            os.remove("static\images\\" + item[0])
                            tagline = "Successfully Deleted Item from Collection!!"
                        else:
                            tagline = "Failed to delete image file"
                        return render_template("success.html", tagline=tagline)
                except sqlite3.OperationalError as e:
                    print(e)
                    headline = "Error in delete operation. Please try again.", e
            counter = counter + 1
    return render_template("deleteitem.html", headline=headline, item_titles=item_titles, counter=counter)


if __name__ == "__main__":
    app.run(debug=True)
