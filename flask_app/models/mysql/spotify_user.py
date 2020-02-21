from flask_app import mysqldb as db

class SpotifyUser(db.Model):
    __tablename__ = 'spotify_users'

    id           = db.Column(db.String(80), primary_key=True)
    display_name = db.Column(db.String(80), nullable=True)
    type         = db.Column(db.String(80), nullable=False)
    uri          = db.Column(db.String(80), nullable=False)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    access_token = db.relationship('SpotifyAccessToken', backref='spotify_user', lazy=True, uselist=False)
    
    def __init__(self, me, user):
        self.id           = me['id']
        self.display_name = me['display_name']
        self.type         = me['type']
        self.uri          = me['uri']
        self.user_id      = user.id


    def __repr__(self):
        return f'<id: {self.id}, display_name: {self.display_name}>'
