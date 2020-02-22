from datetime import datetime, timedelta

from flask_app import mysqldb as db
from flask_app import spotify_credentials
from flask_app.spotify.oauth import SpotifyOAuth

# https://developer.spotify.com/documentation/general/guides/authorization-guide/
class SpotifyToken(db.Model):
    __tablename__ = 'spotify_tokens'

    id            = db.Column(db.Integer,     primary_key=True)
    access_token  = db.Column(db.String(255), nullable=False)
    expires_at    = db.Column(db.Integer,     nullable=False)
    expires_dt    = db.Column(db.DateTime,    nullable=False)
    expires_in    = db.Column(db.Integer,     nullable=False)
    refresh_token = db.Column(db.String(255), nullable=False)
    scope         = db.Column(db.String(255), nullable=False) # TODO: handle scope storing better (array?)
    token_type    = db.Column(db.String(6),   nullable=False) # should always be 'Bearer'
    spotify_id    = db.Column(db.String(80), db.ForeignKey('spotify_users.id'), nullable=True)

    def __init__(self, **kwargs):
        self._update(**kwargs)

    def expired(self):
        now = int((datetime.utcnow() + timedelta(minutes=5)).timestamp())
        return now > self.expires_at

    def refresh(self):
        if not self.expired():
            return

        token_info = SpotifyOAuth.refresh_access_token(spotify_credentials, self)
        self._update(**token_info, commit=True)

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

        spotify_user = kwargs.get('spotify_user')
        if spotify_user:
            self.spotify_id = spotify_user.id

        commit = kwargs.get('commit', False)
        if commit:
            db.session.commit()

    def _add_expiry_time(self):
        dt = datetime.utcnow() + timedelta(seconds=self.expires_in)
        self.expires_dt = dt
        self.expires_at = int(dt.timestamp())
        
    def __repr__(self):
        return f'<token: {self.access_token[:16]}, refresh_token: {self.refresh_token[:16]}, token_type: {self.token_type}, expires_dt: {self.expires_dt}, scopes: {len(self.scope)}>'
