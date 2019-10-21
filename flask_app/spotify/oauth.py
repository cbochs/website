import json
from datetime import datetime, timedelta
from time import time
from urllib.parse import urlencode

import requests

from flask_app.spotify.credentials import SpotifyClientCredentials


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
            'scope': scope or credentials.scope}
        
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

        # app.logger.info('Requesting new access token')
        response = requests.post(SPOTIFY_OAUTH_TOKEN_URL, data=data)

        if response.status_code != 200:
            app.logger.error(response.reason)
            token_info = None
        else:
            token_info = response.json()
            token_info = _add_expiry_time(token_info)
            _save_token_info(credentials, token_info)

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

        # app.logger.info('Requesting refreshed access token')
        response = requests.post(SPOTIFY_OAUTH_TOKEN_URL, data=data)

        if response.status_code != 200:
            # app.logger.error(response.reason)
            token_info = None
        else:
            # Keep old token in case no new token provided
            refresh_token = token_info['refresh_token']

            token_info = response.json()
            token_info = _add_expiry_time(token_info)

            if 'refresh_token' not in token_info:
                token_info['refresh_token'] = refresh_token
            
            _save_token_info(credentials, token_info)
        
        return token_info

    
    @staticmethod
    def update_access_token(credentials, token_info):
        if token_expired(token_info):
            return SpotifyOAuth.refresh_access_token(credentials, token_info)
        else:
            return token_info


    @staticmethod
    def load_token_info(credentials):
        token_save_location = credentials.token_save_location

        # app.logger.info(f'Retrieved token info from {token_save_location}')
        with open(token_save_location, 'r') as ifile:
            token_info = json.load(ifile)

        if token_expired(token_info):
            token_info = SpotifyOAuth.refresh_access_token(credentials, token_info)

        return token_info


def _save_token_info(credentials, token_info):
    token_save_location = credentials.token_save_location

    # app.logger.info(f'Saved token info to {token_save_location}')
    with open(token_save_location, 'w') as ofile:
        json.dump(token_info, ofile)
        

def _add_expiry_time(token_info):
    dt = datetime.utcnow() + timedelta(seconds=token_info['expires_in'])
    token_info['expires_dt'] = dt
    token_info['expires_at'] = int(dt.timestamp())
    return token_info


def token_expired(token_info):
    now = int((datetime.utcnow() + timedelta(minutes=5)).timestamp())
    return now > token_info['expires_at']
