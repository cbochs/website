from flask import Flask
from flask_migrate import Migrate
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_app.utils.jsonencoder import JSONEncoder

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')
app.json_encoder = JSONEncoder

Session(app)

mongodb = PyMongo(app)
mysqldb = SQLAlchemy(app)

migrate_mongodb = Migrate(app, mongodb)
migrate_mysqldb = Migrate(app, mysqldb)

from flask_app import models
from flask_app import routes
