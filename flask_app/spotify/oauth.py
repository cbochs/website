import json
from urllib.parse import urlencode

import requests

from flask_app.spotify.token_info import SpotifyTokenInfo


class SpotifyOAuthException(BaseException):
    pass


class SpotifyOAuth(object):

    @staticmethod
    def authorization_url(credentials, scope=None):
        SPOTIFY_OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'

        params = {
            'client_id': credentials.client_id,
            'response_type': 'code',
            'redirect_uri': credentials.redirect_uri,
            'scope': scope or credentials.default_scope}
        
        return SPOTIFY_OAUTH_AUTHORIZE_URL + '?' + urlencode(params)


    @staticmethod
    def request_access_token(credentials, code):
        SPOTIFY_OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

        data = {
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': credentials.redirect_uri}
        # headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(SPOTIFY_OAUTH_TOKEN_URL, data=data)

        if response.status_code == 200:
            token_info = SpotifyTokenInfo(**response.json())
        else:
            token_info = None

        return token_info


    @staticmethod
    def refresh_access_token(credentials, token_info):
        SPOTIFY_OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

        data = {
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': token_info['refresh_token']}
        # headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(SPOTIFY_OAUTH_TOKEN_URL, data=data)

        if response.status_code == 200:
            token_info = SpotifyTokenInfo.refresh_token(token_info, **response.json())
        else:
            token_info = None
        
        return token_info

    
    @staticmethod
    def update_access_token(credentials, token_info):
        if token_info.expired():
            return SpotifyOAuth.refresh_access_token(credentials, token_info)
        else:
            return token_info
