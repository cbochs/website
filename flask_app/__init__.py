from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')
db = PyMongo(app)

from flask_app import routes