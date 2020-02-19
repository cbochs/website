
import os

import requests

from flask_app.spotify.helper import handle_bulk, handle_cursor
from flask_app.spotify.oauth import SpotifyOAuth


class SpotifyAPIException(BaseException):
    pass


class Spotify(object):

    API_URL = 'https://api.spotify.com/v1/'

    def __init__(self, token_info, credentials):
        self.token_info = token_info
        self.credentials = credentials

    
    def me(self, **kwargs):
        return self._get('me', **kwargs)


    @handle_cursor(limit=50)
    def recently_played(self, **kwargs):
        return self._get('me/player/recently-played', **kwargs)

    
    @handle_cursor(limit=50)
    def my_playlists(self, **kwargs):
        return self._get('me/playlists', **kwargs)

    
    @handle_cursor(limit=50)
    def my_tracks(self, **kwargs):
        return self._get('me/tracks', **kwargs)

    @handle_cursor('tracks')
    @handle_bulk(limit=20)
    def albums(self, **kwargs):
        return self._get('albums', **kwargs)


    @handle_bulk(limit=50)
    def artists(self, **kwargs):
        return self._get(f'artists/{id}', **kwargs)


    @handle_bulk(limit=100)
    def tracks(self, **kwargs):
        return self._get(f'tracks/{id}', **kwargs)

    
    @handle_cursor(limit=50)
    def album_tracks(self, id, **kwargs):
        return self._get(f'albums/{id}/tracks', **kwargs)


    @handle_cursor(limit=50)
    def artist_albums(self, id, **kwargs):
        return self._get(f'artists/{id}/albums', **kwargs)


    @handle_cursor('tracks')
    def playlist(self, id, **kwargs):
        return self._get(f'playlists/{id}', **kwargs)


    @handle_cursor(limit=100)
    def playlist_tracks(self, id, **kwargs):
        return self._get(f'playlists/{id}/tracks', **kwargs)

    
    @handle_bulk(limit=100)
    def add_tracks(self, id, uris, **kwargs):
        return self._post(f'playlists/{id}/tracks', uris=uris)


    def _next(self, result):
        return self._get(result['next']) if result['next'] else None


    def _get(self, endpoint, **kwargs):
        url = endpoint if self.API_URL in endpoint else os.path.join(self.API_URL, endpoint)
        headers = self._headers()
        
        response = requests.get(url, headers=headers, params=kwargs)

        if response.status_code != 200:
            raise SpotifyAPIException(response.reason)

        return response.json()

    def _post(self, endpoint, **kwargs):
        url = endpoint if self.API_URL in endpoint else os.path.join(self.API_URL, endpoint)
        headers = self._headers()

        response = requests.post(url, headers=headers, json=kwargs)

        if response.status_code != 201:
            raise SpotifyAPIException(response.reason)

    
    def _headers(self):
        self.token_info = SpotifyOAuth.update_access_token(self.credentials, self.token_info)

        token_type = self.token_info['token_type']
        access_token = self.token_info['access_token']
        headers = {
            'Authorization': f'{token_type} {access_token}',
            'Content-Type': 'application/json'}
        
        return headers
