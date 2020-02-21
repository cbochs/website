import os


class SpotifyCredentialsException(BaseException):
    pass


class SpotifyClientCredentials(object):

    def __init__(self, app=None, use_env=False, client_id=None, client_secret=None,
                       redirect_uri=None, default_scope=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.default_scope = default_scope

        if use_env:
            self.init_env()

        if app is not None:
            self.init_app(app)

        if self.client_id is None:
            raise SpotifyCredentialsException('CLIENT_ID was not set / properly')

        if self.client_secret is None:
            raise SpotifyCredentialsException('CLIENT_SECRET was not set / properly')

        if self.redirect_uri is None:
            raise SpotifyCredentialsException('REDIRECT_URI was not set / properly')


    def init_env(self):
        if self.client_id is None:
            self.client_id = os.getenv('CLIENT_ID')
        
        if self.client_secret is None:
            self.client_secret = os.getenv('CLIENT_SECRET')

        if self.redirect_uri is None:
            self.redirect_uri = os.getenv('REDIRECT_URI')

        if self.default_scope is None:
            self.default_scope = os.getenv('DEFAULT_SCOPE')


    def init_app(self, app):
        if self.client_id is None:
            self.client_id = app.config.get('CLIENT_ID')
        
        if self.client_secret is None:
            self.client_secret = app.config.get('CLIENT_SECRET')

        if self.redirect_uri is None:
            self.redirect_uri = app.config.get('REDIRECT_URI')

        if self.default_scope is None:
            self.default_scope = app.config.get('DEFAULT_SCOPE')
