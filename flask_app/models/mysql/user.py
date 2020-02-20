from sqlalchemy import Column, Integer, String, DateTime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_app import mysqldb as db


class User(db.Model):
    __tablename__ = 'users'

    id       = Column(Integer, primary_key=True)
    email    = Column(String(320), unique=True, nullable=False)
    username = Column(String(80),  unique=True, nullable=False)
    password = Column(String(128),              nullable=False)

    def __init__(self, email, username, password):
        self.email    = email
        self.username = username
        self.password = password

    # @classmethod
    # def authenticate(cls, **kwargs):
    #     email    = kwargs.get('email')
    #     username = kwargs.get('username')
    #     password = kwargs.get('password')

    #     if not email and not username:
    #         return None

    #     if not password:
    #         return None
        
    #     return cls.query.filter_by(email=email).first()

# https://developer.spotify.com/documentation/general/guides/authorization-guide/
# class SpotifyAccessToken(db.Model):
#     __tablename__ = 'spotify_tokens'

#     id            = Column(Integer, primary_key=True)
#     access_token  = Column(String(255), nullable=False)
#     expires_at    = Column(Integer)
#     expires_dt    = Column(DateTime)
#     expires_in    = Column(Integer)
#     refresh_token = Column(String(255))
#     scope         = Column(String(255)) # TODO: update to a better value
#     token_type    = Column(String(6))   # should always be 'Bearer'
#     user          = db.relationship('User', backref='access_token', lazy=True, uselist=False)

# {
#     "access_token": "BQBoLQCncPdSzChxqGEX8HxOwBzyjxz6wwJtcyljZRKc4Y9wIujYfr-VaO2N46dJUPukfU6ZoO0x-QOuo8qhHkGTISu8-WARqX-YuCjl-eJRHL1wsWRfWC3ucTbvdUnIzWVMzqKIYhHF-8LjZ0e8T0nv_Yn3mY-yZnFCTTq-BbJ0Ax0O17UQ5LOAVvxuvZK5odNppnynLq0i3BOso5EMNnrEYlGcklE3nRyBte21",
#     "token_type": "Bearer",
#     "expires_in": 3600,
#     "scope": "playlist-read-private playlist-read-collaborative user-library-read playlist-modify-private playlist-modify-public user-read-recently-played",
#     "expires_dt": "2020-02-20 19:44:16.012404",
#     "expires_at": 1582253056,
#     "refresh_token": "AQAZ2PefAjDVQbjmVKwl1EeGl2lCyPmBAsYkT4flzCK9zuiaD8cBFAUHmZgm38PZItQBrqPuzCKMg9Whk8zXl6pPa9bpl-khDq8O_d13lTXFnaFEY1k9E08M4hefv-Mi3B0PoA"}