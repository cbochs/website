from flask import Flask
from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_migrate import Migrate
from flask_pymongo import PyMongo
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from flask_app.utils.jsonencoder import JSONEncoder

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')
app.json_encoder = JSONEncoder

CORS(app, supports_credentials=True)
Session(app)

scheduler = APScheduler(app=app)

mongodb = PyMongo(app)
mysqldb = SQLAlchemy(app)

migrate_mongodb = Migrate(app, mongodb)
migrate_mysqldb = Migrate(app, mysqldb)

from flask_app.spotify.credentials import SpotifyClientCredentials

spotify_credentials = SpotifyClientCredentials(app)

from flask_app import models
from flask_app import routes
