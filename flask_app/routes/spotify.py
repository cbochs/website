from flask import jsonify, make_response, redirect, request, session

from flask_app import app, spotify, mysqldb
from flask_app.models.mysql.spotify_access_token import SpotifyAccessToken
from flask_app.models.mysql.spotify_user import SpotifyUser
from flask_app.models.mysql.user import User
from flask_app.spotify.oauth import SpotifyOAuth


@app.route('/api/spotify/authorize', methods=('GET',))
def spotify_authorize():
    error = request.values.get('error')
    code = request.values.get('code')

    # TODO: ensure use is authenticated in session
    user = User.find_user(email=session['email'])

    if user.spotify_user:
        if user.spotify_user.access_token.expired():
            mysqldb.session.delete(user.spotify_user.access_token)
            mysqldb.session.delete(user.spotify_user)
            mysqldb.session.commit()
        else:
            app.logger.info(f'User has already authorized for Spotify')
            return make_response('Already authorized.', 200)
    
    if error:
        app.logger.error(f'Could not authorize user {user}. Error: {error}')
        return make_response('Unauthorized.', 401)
    elif code:
        token_info = spotify.request_access_token(code)

        spotify_api = spotify.connect(token_info)
        me = spotify_api.me()

        spotify_user = SpotifyUser(me, user)
        access_token = SpotifyAccessToken(token_info, spotify_user)

        mysqldb.session.add(access_token)
        mysqldb.session.add(spotify_user)
        mysqldb.session.commit()

        app.logger.info('Obtained access code!')
        return make_response('Authorized.', 200)
    else:
        app.logger.info('Requesting Spotify access code')
        return redirect(spotify.authorization_url())


@app.route('/api/spotify/me', methods=('GET',))
def me():
    pass
