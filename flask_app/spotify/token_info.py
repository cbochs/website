from datetime import datetime, timedelta

class SpotifyTokenInfoException(BaseException):
    pass

class SpotifyTokenInfo(object):
    
    def __init__(self, access_token=None, expires_in=None, refresh_token=None, 
                       scope=None, token_type=None, expires_at=None, expires_dt=None):
        self.access_token  = access_token
        self.expires_in    = expires_in
        self.refresh_token = refresh_token
        self.scope         = scope
        self.token_type    = token_type
        self.expires_at    = expires_at
        self.expires_dt    = expires_dt
        
        if not expires_at or not expires_dt:
            self._add_expiry_time()


    def expired(self):
        now = int((datetime.utcnow() + timedelta(minutes=5)).timestamp())
        return now > self.expires_at


    def _add_expiry_time(self):
        dt = datetime.utcnow() + timedelta(seconds=self.expires_in)
        self.expires_dt = dt
        self.expires_at = int(dt.timestamp())

    @staticmethod
    def refresh_token(token_info, **kwargs):
        new_token_info = SpotifyTokenInfo(**kwargs)

        # Keep old token in case no new token provided
        if new_token_info.refresh_token is None:
            new_token_info.refresh_token = token_info.refresh_token

        return new_token_info
