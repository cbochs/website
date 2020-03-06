from flask_app import mysqldb as db

class SpotifyUser(db.Model):
    __tablename__ = 'spotify_users'

    id           = db.Column(db.String(80), primary_key=True)
    display_name = db.Column(db.String(80), nullable=True)
    type         = db.Column(db.String(80), nullable=False)
    uri          = db.Column(db.String(80), nullable=False)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    api_token    = db.relationship('SpotifyToken', backref='spotify_user', lazy=True, uselist=False)
    
    def __init__(self, **kwargs):
        self.id           = kwargs.get('id')
        self.display_name = kwargs.get('display_name')
        self.type         = kwargs.get('type')
        self.uri          = kwargs.get('uri')

        user = kwargs.get('user')
        if user:
            self.user_id = user.id

    def __repr__(self):
        return f'<display_name: {self.display_name}, id: {self.id}>'

    @classmethod
    def find_user(cls, **kwargs):
        id = kwargs.get('id')
        if id:
            return cls.query.get(id)

        return None
