from flask import render_template, jsonify

from flask_app import app
from flask_app.spotify.api import Spotify
from flask_app.spotify.credentials import SpotifyClientCredentials
from flask_app.spotify.oauth import SpotifyOAuth
from flask_app.formatter.play_history import format_play_history
from flask_app.formatter.util import format_all


@app.route('/')
def index():
    credentials = SpotifyClientCredentials(app=app)
    token_info = SpotifyOAuth.load_token_info(credentials)
    spotify = Spotify(token_info, credentials)

    me = spotify.me()
    recently_played = spotify.recently_played(follow_cursor=True)
    recently_played = format_all(recently_played, format_play_history, user=me)
    recently_played = format_all(recently_played, stringify_artists)

    return render_template('index.html', recently_played=recently_played)
    # return jsonify(recently_played)


def stringify_artists(result):
    result['track']['artists'] = ', '.join([a['name'] for a in result['track']['artists']])
    return result