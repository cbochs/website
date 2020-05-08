from datetime import datetime, timedelta

from flask_app import mysqldb as db
from flask_app.spotify.token import SpotifyToken as BaseSpotifyToken
from flask_app.spotify.token import SpotifyTokenException

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
        self._token = BaseSpotifyToken(**kwargs)
        self._update()

        spotify_user = kwargs.get('spotify_user')
        if spotify_user:
            self.spotify_id = spotify_user.id

    def refresh(self, credentials):
        try:
            refreshed = self.token.refresh(credentials)
        except SpotifyTokenException as e:
            # TODO: remove token from db and set spotify_user's api_token to none
            return

        if refreshed:
            self._update()
            db.session.commit()

    @property
    def token(self):
        if not hasattr(self, '_token'):
            self._token = BaseSpotifyToken(**self.__dict__)
        return self._token

    def _update(self):
        self.access_token  = self.token.access_token
        self.expires_at    = self.token.expires_at
        self.expires_dt    = self.token.expires_dt
        self.expires_in    = self.token.expires_in
        self.refresh_token = self.token.refresh_token
        self.scope         = self.token.scope
        self.token_type    = self.token.token_type

    def __repr__(self):
        return f'<type: spotify, access_token: {self.access_token[:16]}, refresh_token: {self.refresh_token[:16]}, expires_dt: {self.expires_dt}, #scopes: {len(self.scope)}>'
