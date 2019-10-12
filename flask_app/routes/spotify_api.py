import requests
from flask import jsonify

from flask_app import app
from flask_app.spotify.api import Spotify


SPOTIFY_API_URL = 'https://api.spotify.com/v1/'

@app.route('/spotify/me')
def me():
    return jsonify(Spotify)
