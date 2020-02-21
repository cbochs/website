from flask_app.spotify.api import SpotifyApi
from flask_app.spotify.oauth import SpotifyOAuth
from flask_app.spotify.credentials import SpotifyClientCredentials

# What this has to do:
# - Connect with the Spotify Web API using OAuth 2.0 flow
# - Accept config 

class Spotify(object):

    def __init__(self, app=None, credentials=None):
        self.credentials = credentials

        if app is not None:
            self.init_app(app)


    def init_app(self, app):
        self.credentials = SpotifyClientCredentials(app)


    def authorization_url(self):
        return SpotifyOAuth.authorization_url(self.credentials)


    def request_access_token(self, code):
        return SpotifyOAuth.request_access_token(self.credentials, code)


    def connect(self, token_info, scope=None):
        return SpotifyApi(self, token_info)
