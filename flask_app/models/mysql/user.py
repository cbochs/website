# from sqlalchemy import Column, Integer, String, DateTime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_app import mysqldb as db


class User(db.Model):
    __tablename__ = 'users'

    id       = db.Column(db.Integer, primary_key=True)
    email    = db.Column(db.String(320), unique=True, nullable=False)
    username = db.Column(db.String(80),  unique=True, nullable=False)
    password = db.Column(db.String(128),              nullable=False)
    spotify_user = db.relationship('SpotifyUser', back_populates='user', lazy=True, uselist=False)

    def __init__(self, **kwargs):
        self.email    = kwargs.get('email')
        self.username = kwargs.get('username')
        self.password = generate_password_hash(kwargs.get('password'), method='sha256')

    def to_dict(self):
        return dict(
            id=self.id,
            email=self.email,
            username=self.username)

    def __repr__(self):
        return f'<username: {self.username}, email: {self.email}, id: {self.id}>'

    @classmethod
    def find_user(cls, **kwargs):
        email    = kwargs.get('email')
        username = kwargs.get('username')

        if email:
            return cls.query.filter_by(email=email).first()

        if username:
            return cls.query.filter_by(username=username).first()

        return None

    @classmethod
    def authenticate(cls, **kwargs):
        password = kwargs.get('password')

        user = User.find_user(**kwargs)
        if user is None:
            return None
        
        if not check_password_hash(user.password, password):
            return None

        return user
