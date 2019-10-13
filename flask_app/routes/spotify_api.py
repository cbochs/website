import requests
from flask import jsonify

from flask_app import app
from flask_app.formatter.play_history import format_play_history
from flask_app.formatter.playlist import format_simple_playlist
from flask_app.formatter.util import format_all
from flask_app.spotify.api import Spotify
from flask_app.spotify.credentials import SpotifyClientCredentials
from flask_app.spotify.oauth import SpotifyOAuth

SPOTIFY_API_URL = 'https://api.spotify.com/v1/'


@app.route('/spotify/me')
def me():
    credentials = SpotifyClientCredentials(app=app)
    token_info = SpotifyOAuth.load_token_info(credentials)
    spotify = Spotify(token_info, credentials)

    return jsonify(spotify.me())


@app.route('/spotify/recently_played')
def recently_played():
    credentials = SpotifyClientCredentials(app=app)
    token_info = SpotifyOAuth.load_token_info(credentials)
    spotify = Spotify(token_info, credentials)

    me = spotify.me()
    recently_played = spotify.recently_played(follow_cursor=True)
    recently_played = format_all(recently_played, format_play_history, user=me)

    return jsonify(recently_played)

@app.route('/spotify/playlists')
def playlists():
    credentials = SpotifyClientCredentials(app=app)
    token_info = SpotifyOAuth.load_token_info(credentials)
    spotify = Spotify(token_info, credentials)

    playlists = spotify.my_playlists(follow_cursor=True)
    playlists = format_all(playlists, format_simple_playlist)
    
    return jsonify(playlists)
