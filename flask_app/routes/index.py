from flask import render_template

from flask_app import app
from flask_app.spotify.api import Spotify
from flask_app.spotify.credentials import SpotifyClientCredentials
from flask_app.spotify.oauth import SpotifyOAuth


@app.route('/')
def index():
    credentials = SpotifyClientCredentials(app=app)
    token_info = SpotifyOAuth.load_token_info(credentials)
    spotify = Spotify(token_info, credentials)

    return render_template('index.html')
