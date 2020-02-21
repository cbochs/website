from flask_app import mysqldb as db

class SpotifyUser(db.Model):
    __tablename__ = 'spotify_users'

    id           = db.Column(db.String(255), primary_key=True)
    display_name = db.Column(db.String(255), nullable=True)
    type         = db.Column(db.String(255), nullable=False)
    uri          = db.Column(db.String(255), nullable=False)
    user         = db.relationship('User',               back_populates='spotify_user', lazy=True, uselist=False)
    access_token = db.relationship('SpotifyAccessToken', back_populates='spotify_user', lazy=True, uselist=False)
    
    def __init__(self, me):
        self.id           = me['id']
        self.display_name = me['display_name']
        self.type         = me['type']
        self.uri          = me['uri']

    def __repr__(self):
        return f'<id: {self.id}, display_name: {self.display_name}>'
