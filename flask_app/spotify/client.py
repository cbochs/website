import os

import requests

from .helper import handle_bulk, handle_cursor
from .oauth import SpotifyOAuth


class SpotifyClientException(BaseException):
    pass


class SpotifyClient(object):

    # https://developer.spotify.com/documentation/web-api/reference-beta/
    SPOTIFY_API_URI = 'https://api.spotify.com/v1/'

    def __init__(self, credentials, token):
        self.credentials = credentials
        self.token = token


    def me(self, **kwargs):
        """
        Get detailed profile information about the current user (including the current user's username).
        Reference: https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-current-users-profile

        :return: the current users' user object
        :rtype: [type]
        """
        return self._get('me', **kwargs)


    @handle_cursor(limit=50)
    def recently_played(self, **kwargs):
        """
        Get tracks from the current user's recently played tracks. Note: Currently doesn't support podcast episodes.
        Reference: https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-recently-played

        :param int limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.
        :param int after: A Unix timestamp in milliseconds. Returns all items after (but not including) this cursor position. If after is specified, before must not be specified.
        :param int before: A Unix timestamp in milliseconds. Returns all items before (but not including) this cursor position. If before is specified, after must not be specified.
        :param bool follow_cursor: follow the cursor object embedded in the returned history object. Default: False

        :return: the current users' history object
        :rtype: [type]
        """
        return self._get('me/player/recently-played', **kwargs)


    @handle_cursor(limit=50)
    def my_playlists(self, **kwargs):
        """
        Get a list of the playlists owned or followed by the current Spotify user.
        Reference: https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-a-list-of-current-users-playlists

        :param int limit: The maximum number of playlists to return. Default: 20. Minimum: 1. Maximum: 50.
        :param int offset: The index of the first playlist to return. Default: 0 (the first object). Maximum offset: 100.000. Use with limit to get the next set of playlists.
        :param bool follow_cursor: follow the cursor object embedded in the returned paging object. Default: False

        :return: the current users' playlists
        :rtype: [type]
        """
        return self._get('me/playlists', **kwargs)


    @handle_cursor(limit=50)
    def my_tracks(self, **kwargs):
        """
        Get a list of the songs saved in the current Spotify user's 'Your Music' library.
        Reference: https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-users-saved-tracks

        :param int limit: The maximum number of objects to return. Default: 20. Minimum: 1. Maximum: 50.
        :param int offset: The index of the first object to return. Default: 0 (i.e., the first object). Use with limit to get the next set of objects.
        :param str market: An ISO 3166-1 alpha-2 country code or the string from_token. Provide this parameter if you want to apply Track Relinking.
        :param bool follow_cursor: follow the cursor object embedded in the returned paging object. Default: False

        :return: the current users' 'Liked Songs'
        :rtype: [type]
        """
        return self._get('me/tracks', **kwargs)


    @handle_cursor('tracks')
    @handle_bulk(limit=20)
    def albums(self, **kwargs):
        """
        [summary]

        :return: [description]
        :rtype: [type]
        """
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
        if self.SPOTIFY_API_URI in endpoint:
            url = endpoint
        else:
            url = os.path.join(self.SPOTIFY_API_URI, endpoint)

        headers = self._headers()

        response = requests.get(url, headers=headers, params=kwargs)

        if response.status_code != 200:
            raise SpotifyClientException(response.reason)

        return response.json()


    def _post(self, endpoint, **kwargs):
        if self.SPOTIFY_API_URI in endpoint:
            url = endpoint
        else:
            url = os.path.join(self.SPOTIFY_API_URI, endpoint)

        headers = self._headers()

        response = requests.post(url, headers=headers, data=kwargs)

        if response.status_code != 201:
            raise SpotifyClientException(response.reason)


    def _headers(self):
        self.token.refresh(self.credentials)
        token_type = self.token.token_type
        access_token = self.token.access_token
        headers = {
            'Authorization': f'{token_type} {access_token}',
            'Content-Type': 'application/json'}

        return headers
