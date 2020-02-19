from flask import jsonify, redirect, request, url_for

from flask_app import app
from flask_app.spotify.credentials import SpotifyClientCredentials
from flask_app.spotify.oauth import SpotifyOAuth


@app.route('/authorize')
def authorize():
    error = request.values.get('error')
    code = request.values.get('code')

    credentials = SpotifyClientCredentials(app=app)
    
    if error:
        app.logger.error(error)
        return redirect(url_for('home'))
    elif code:
        app.logger.info('Obtained access code')
        token_info = SpotifyOAuth.request_access_token(credentials, code)
        return redirect(url_for('home'))
    else:
        app.logger.info('Requesting Spotify access code')
        return redirect(SpotifyOAuth.authorization_url(credentials))
