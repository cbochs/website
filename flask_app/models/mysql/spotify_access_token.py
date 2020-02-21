from flask_app import mysqldb as db

# https://developer.spotify.com/documentation/general/guides/authorization-guide/
class SpotifyAccessToken(db.Model):
    __tablename__ = 'spotify_tokens'

    id            = db.Column(db.Integer,     primary_key=True)
    access_token  = db.Column(db.String(255), nullable=False)
    expires_at    = db.Column(db.Integer,     nullable=False)
    expires_dt    = db.Column(db.DateTime,    nullable=False)
    expires_in    = db.Column(db.Integer,     nullable=False)
    refresh_token = db.Column(db.String(255), nullable=False)
    scope         = db.Column(db.String(255), nullable=False) # TODO: handle scope storing better (array?)
    token_type    = db.Column(db.String(6),   nullable=False) # should always be 'Bearer'
    spotify_user  = db.relationship('SpotifyUser', back_populates='access_token', lazy=True, uselist=False)

    def __init__(self, token_info):
        self.access_token  = token_info.access_token
        self.expires_at    = token_info.expires_at
        self.expires_dt    = token_info.expires_dt
        self.expires_in    = token_info.expires_in
        self.refresh_token = token_info.refresh_token
        self.scope         - token_info.scope
        self.token_type    = token_info.token_type

    def __repr__(self):
        return f'<token: {self.access_token[:16]}, refresh_token: {self.refresh_token[:16]}, expires_at: {self.expires_at}, scopes: {len(self.scope)}'
