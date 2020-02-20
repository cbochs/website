from flask import Flask
from flask_migrate import Migrate
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

mongodb = PyMongo(app)
mysqldb = SQLAlchemy(app)

migrate_mongodb = Migrate(app, mongodb)
migrate_mysqldb = Migrate(app, mysqldb)

from flask_app import models
from flask_app import routes
