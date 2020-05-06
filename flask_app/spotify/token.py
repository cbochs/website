import json
import os
from datetime import datetime, timedelta

from .oauth import SpotifyOAuth


class SpotifyTokenException(BaseException):
    pass


class SpotifyToken(object):

    def __init__(self, **kwargs):
        self.access_token  = None
        self.expires_at    = None
        self.expires_dt    = None
        self.expires_in    = None
        self.refresh_token = None
        self.scope         = None
        self.token_type    = None

        self._update(**kwargs)


    def refresh(self, credentials):
        if not self.expired():
            return False

        token_info = SpotifyOAuth.refresh_access_token(credentials, self)
        if token_info is None:
            raise SpotifyTokenException('Could not refresh access token')

        self._update(**token_info)

        return True


    def expired(self):
        now = int((datetime.utcnow() + timedelta(minutes=5)).timestamp())
        return now > self.expires_at


    def save(self, file_path):
        with open(file_path, 'w') as token_file:
            token_info = self.__dict__.copy()
            token_info.pop('expires_dt')
            json.dump(token_info, token_file)


    @staticmethod
    def load(file_path):
        try:
            with open(file_path, 'r') as token_file:
                token_info = json.load(token_file)
                return SpotifyToken(**token_info)
        except:
            return None


    def _update(self, **kwargs):
        self.access_token  = kwargs.get('access_token')
        self.expires_at    = kwargs.get('expires_at')
        self.expires_dt    = kwargs.get('expires_dt')
        self.expires_in    = kwargs.get('expires_in')
        self.scope         = kwargs.get('scope')
        self.token_type    = kwargs.get('token_type')

        # might not get a new refresh token. If not, keep the old one
        self.refresh_token = kwargs.get('refresh_token', self.refresh_token)

        if not self.expires_at or not self.expires_dt:
            self._add_expiry_time()


    def _add_expiry_time(self):
        if not self.expires_at:
            dt = datetime.utcnow() + timedelta(seconds=self.expires_in)
            self.expires_dt = dt
            self.expires_at = int(dt.timestamp())
        else:
            self.expires_dt = datetime.fromtimestamp(self.expires_at)
