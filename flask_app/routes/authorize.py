from flask import redirect, request

from flask_app import app
from flask_app.spotify import oauth


CLIENT_ID = '9954e08018e242b6b5be2a19191808d9'
CLIENT_SECRET = '5216305cc4064deaac1c6ee299972691'
REDIRECT_URI = 'http://127.0.0.1:5000/authorize'
SCOPE = ','.join(['playlist-read-private',
                  'playlist-read-collaborative',
                  'playlist-modify-public',
                  'playlist-modify-private',
                  'user-library-read',
                  'user-read-recently-played'])


@app.route('/authorize')
def authorize():
    error = request.values.get('error')
    code = request.values.get('code')
    
    if error:
        app.logger.error(error)
        return redirect('/')
    elif code:
        app.logger.info('Obtained access code')
        return oauth.request_access_token(code, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
    else:
        app.logger.info('Requesting Spotify access code')
        return redirect(oauth.authorization_url(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE))
