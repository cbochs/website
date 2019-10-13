import os


class SpotifyCredentialsException(BaseException):
    pass


class SpotifyClientCredentials(object):

    def __init__(self, app=None, use_env=True, client_id=None, client_secret=None, redirect_uri=None, scope=None, token_save_location=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.token_save_location = token_save_location

        if use_env:
            self.init_env()

        if app is not None:
            self.init_app(app)


    def init_env(self):
        if self.client_id is None:
            self.client_id = os.getenv('CLIENT_ID')
        
        if self.client_secret is None:
            self.client_secret = os.getenv('CLIENT_SECRET')

        if self.redirect_uri is None:
            self.redirect_uri = os.getenv('REDIRECT_URI')

        if self.scope is None:
            self.scope = os.getenv('SCOPE')

        if self.token_save_location is None:
            self.token_save_location = os.getenv('TOKEN_SAVE_LOCATION')


    def init_app(self, app):
        if self.client_id is None:
            self.client_id = app.config.get('CLIENT_ID')
        
        if self.client_secret is None:
            self.client_secret = app.config.get('CLIENT_SECRET')

        if self.redirect_uri is None:
            self.redirect_uri = app.config.get('REDIRECT_URI')

        if self.scope is None:
            self.scope = app.config.get('SCOPE')
        
        if self.token_save_location is None:
            self.token_save_location = app.config.get('TOKEN_SAVE_LOCATION')
