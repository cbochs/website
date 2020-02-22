from flask_app.spotify.api import SpotifyApi
from flask_app.spotify.oauth import SpotifyOAuth
from flask_app.spotify.credentials import SpotifyClientCredentials
from flask_app.spotify.token_info import SpotifyTokenInfo
from flask_app import app

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

    
    def token_info(self, access_token):
        return SpotifyTokenInfo(**access_token.to_dict())


    def connect(self, token_info, scope=None):
        if not isinstance(token_info, SpotifyTokenInfo):
            token_info = self.token_info(token_info)
        return SpotifyApi(self.credentials, token_info)
