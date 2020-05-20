from flask import Flask
from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_migrate import Migrate
from flask_pymongo import PyMongo
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from .google.credentials import GoogleClientCredentials
from .spotify.credentials import SpotifyClientCredentials
from .utils.json import JSONEncoder

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')
app.json_encoder = JSONEncoder

CORS(app, supports_credentials=True)

my_scheduler = APScheduler(app=app)
my_scheduler.start()

mongodb = PyMongo(app)
mysqldb = SQLAlchemy(app)
session = Session(app)

mysqldb.create_all()
session.app.session_interface.db.create_all()

migrate_mongodb = Migrate(app, mongodb)
migrate_mysqldb = Migrate(app, mysqldb)

google_credentials = GoogleClientCredentials(app)
spotify_credentials = SpotifyClientCredentials(app)

from flask_app import models
from flask_app import routes
