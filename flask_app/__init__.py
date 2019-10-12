from flask import Flask

app = Flask(__name__)
app.debug = True
app.config.from_pyfile('flaskapp.cfg')

from flask_app import routes