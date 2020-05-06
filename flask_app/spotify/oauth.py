import json
from urllib.parse import urlencode

import requests


# https://developer.spotify.com/documentation/general/guides/authorization-guide/
SPOTIFY_OAUTH_AUTH_URI = 'https://accounts.spotify.com/authorize'
SPOTIFY_OAUTH_TOKEN_URI = 'https://accounts.spotify.com/api/token'


class SpotifyOAuthException(BaseException):
    pass


class SpotifyOAuth(object):

    @staticmethod
    def authorization_url(credentials, scope=None):
        params = {
            'client_id': credentials.client_id,
            'response_type': 'code',
            'redirect_uri': credentials.redirect_uri,
            'scope': scope or credentials.default_scope}

        return SPOTIFY_OAUTH_AUTH_URI + '?' + urlencode(params)


    @staticmethod
    def request_access_token(credentials, code):
        data = {
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': credentials.redirect_uri}
        # headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(SPOTIFY_OAUTH_TOKEN_URI, data=data)

        if response.status_code == 200:
            token_info = response.json()
        else:
            token_info = None

        return token_info


    @staticmethod
    def refresh_access_token(credentials, token_info):
        data = {
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': token_info.refresh_token}
        # headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(SPOTIFY_OAUTH_TOKEN_URI, data=data)

        if response.status_code == 200:
            token_info = response.json()
        else:
            token_info = None

        return token_info
