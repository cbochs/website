import json
from urllib.parse import urlencode

import requests


class GoogleOAuthException(BaseException):
    pass


class GoogleOAuth(object):

    # https://developers.google.com/identity/protocols/oauth2
    GOOGLE_OAUTH_AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    GOOGLE_OAUTH_TOKEN_URI = 'https://oauth2.googleapis.com/token'

    @staticmethod
    def authorization_url(credentials, scope=None, access_type='offline'):
        params = {
            'client_id': credentials.client_id,
            'response_type': 'code',
            'redirect_uri': credentials.redirect_uri,
            'scope': scope or credentials.default_scope,
            'access_type': access_type}

        return GOOGLE_OAUTH_AUTH_URI + '?' + urlencode(params)


    @staticmethod
    def request_access_token(credentials, code):
        data = {
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': credentials.redirect_uri}
        # headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(GOOGLE_OAUTH_TOKEN_URI, data=data)

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

        response = requests.post(GOOGLE_OAUTH_TOKEN_URI, data=data)

        if response.status_code == 200:
            token_info = response.json()
        else:
            token_info = None

        return token_info
