from datetime import datetime, timedelta
from time import time
from urllib.parse import urlencode

import requests

from flask_app import app


def authorization_url(client_id=None, redirect_uri=None, scope=None):
    SPOTIFY_OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'

    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scope}
    
    return SPOTIFY_OAUTH_AUTHORIZE_URL + '?' + urlencode(params)


def request_access_token(code, client_id=None, client_secret=None, redirect_uri=None):
    SPOTIFY_OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri}
    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    app.logger.info('Requesting new access token')
    response = requests.post(SPOTIFY_OAUTH_TOKEN_URL, data=data)

    if response.status_code != 200:
        app.logger.error(response.reason)
        token_info = None
    else:
        token_info = response.json()
        token_info = _add_expiry_time(token_info)

    return token_info


def refresh_access_token(token_info, client_id=None, client_secret=None, redirect_uri=None):
    SPOTIFY_OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': token_info['refresh_token']}
    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    app.logger.info('Requesting refreshed access token')
    response = requests.post(SPOTIFY_OAUTH_TOKEN_URL, data=data)

    if response.status_code != 200:
        app.logger.error(response.reason)
    else:
        # keep old token in case no new token provided
        refresh_token = token_info['refresh_token']

        token_info = response.json()
        token_info = _add_expiry_time(token_info)

        if 'refresh_token' not in token_info:
            token_info['refresh_token'] = refresh_token
    
    return token_info


def _add_expiry_time(token_info):
    dt = datetime.utcnow() + timedelta(seconds=token_info['expires_in'])
    token_info['expires_dt'] = dt
    token_info['expires_at'] = int(dt.timestamp())
    return token_info


def token_expired(token_info):
    now = int((datetime.utcnow() + timedelta(minutes=5)).timestamp())
    return now > token_info['expires_at']


def _format_scope(scopes):
    if isinstance(scopes, list):
        return ','.join(scopes)
    else:
        return scopes
