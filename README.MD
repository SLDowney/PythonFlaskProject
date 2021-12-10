
Python Flask App
================

A Python Flask virtual collection.

Installation
------------

1. Click and download the file [ProjectDownloadFolder.zip](https://github.com/SLDowney/PythonFlaskProject/blob/master/ProjectDownloadFolder.zip). Place into the 
desired directory, and extract all items.

2. Open application.py. In the IDE terminal and make sure you are in your project directory, then run the commands below to install and run flask. 
  ```python
  py -m venv env
  env\Scripts\activate
  pip3 install flask
  $env:FLASK_APP="application"
  $env:FLASK_ENV="development"
  flask run
  ```
The last command (`flask run`) starts the virtual interface. Now you can go to `http://127.0.0.1:5000/` to interact with the flask app.

Use
---

The *Home* page will show a brief overview of what the app does, and a button to show you a random item from the collection. 

The *Display* page shows every item in the collection, listed with the book cover to the left, and the details to the right listed as Title, Author, and Series. 

The *Add Item* page allows you to add an item into the database. You can choose an image for the book cover - keep in mind, images must be less than 
1MB and have the extension .png, .jfif, .jpg, or .jpeg. Any other files will not be added. You can also enter a Title, Author and Series for your item When you 
click "Submit" you item will be added to the database.

The *Delete Item* page shows you a list of items in your collection by Title, and allows you to delete whichever item you want. Clicking "Submit" removes the item 
from the databse permanently, so be careful you do not accidentally delete the wrong item, or you will have to add it again.
