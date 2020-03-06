from datetime import datetime, timedelta

from flask_app.spotify.oauth import SpotifyOAuth

class SpotifyTokenException(BaseException):
    pass

class SpotifyToken(object):
    
    def __init__(self, access_token=None, expires_at=None, expires_dt=None,
                       expires_in=None, refresh_token=None, scope=None,
                       token_type=None):
        self.access_token  = access_token
        self.expires_at    = expires_at
        self.expires_dt    = expires_dt
        self.expires_in    = expires_in
        self.refresh_token = refresh_token
        self.scope         = scope
        self.token_type    = token_type

        if not self.expires_at or not self.expires_dt:
            self._add_expiry_time()


    def refresh(self, credentials):
        if not self.expired():
            return False

        token_info = SpotifyOAuth.refresh_access_token(spotify_credentials, self)
        if token_info is None:
            raise SpotifyTokenException('Could not refresh access token')

        self._update(**token_info)

        return True


    def expired(self):
        now = int((datetime.utcnow() + timedelta(minutes=5)).timestamp())
        return now > self.expires_at


    def _update(self, **kwargs):
        self.access_token  = kwargs.get('access_token')
        self.expires_at    = kwargs.get('expires_at')
        self.expires_dt    = kwargs.get('expires_dt')
        self.expires_in    = kwargs.get('expires_in')
        self.scope         = kwargs.get('scope')
        self.token_type    = kwargs.get('token_type')

        # might not get a new refresh token. If not, keep the old one
        self.refresh_token = kwargs.get('refresh_token', self.refresh_token)

        self._add_expiry_time()


    def _add_expiry_time(self):
        dt = datetime.utcnow() + timedelta(seconds=self.expires_in)
        self.expires_dt = dt
        self.expires_at = int(dt.timestamp())
