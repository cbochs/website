from flask import jsonify, make_response, redirect, request, session

from flask_app import app, spotify, mysqldb
from flask_app.models.mysql.spotify_access_token import SpotifyAccessToken
from flask_app.models.mysql.spotify_user import SpotifyUser
from flask_app.models.mysql.user import User
from flask_app.spotify.oauth import SpotifyOAuth


@app.route('/api/spotify/authorize', methods=('GET',))
def spotify_authorize():
    app.logger.info(f'session <user_id: {session.get("user_id")}>')
    spotify_user = SpotifyUser.find_user(id=session.get('spotify_id'))
    if spotify_user:
        # TODO: refresh token if needed
        app.logger.info(f'Spotify user already authorized in session {spotify_user}')
        return make_response('Already authorized.', 200)

    user = User.find_user(id=session.get('user_id'))
    if user and user.spotify_user:
        # TODO: refresh token if needed
        session['spotify_id'] = user.spotify_user.id
        app.logger.info(f'User is already authorized with valid spotify user {user}')
        return make_response('Already authorized.', 200)
    
    error = request.values.get('error')
    code = request.values.get('code')

    if error:
        app.logger.error(f'Could not authorize user {user}. Error: {error}')
        return make_response('Unauthorized.', 401)
    elif code:
        token_info = spotify.request_access_token(code)

        spotify_api = spotify.connect(token_info)
        me = spotify_api.me()

        spotify_user = SpotifyUser.find_user(id=me['id'])
        if spotify_user:
            # TODO: refresh token with new token
            session['spotify_id'] = spotify_user.id
            app.logger.info(f'Spotify user already authorized, but not in session {spotify_user}')
            return make_response('Already authorized.', 200)

        spotify_user = SpotifyUser(me, user=user)
        access_token = SpotifyAccessToken(token_info, spotify_user=spotify_user)

        mysqldb.session.add(access_token)
        mysqldb.session.add(spotify_user)
        mysqldb.session.commit()

        session['spotify_id'] = spotify_user.id

        app.logger.info(f'Created new user! {spotify_user}')
        return make_response('Authorized.', 200)
    else:
        app.logger.info('Requesting Spotify access code')
        # return redirect(spotify.authorization_url())
        return make_response(jsonify({'auth_url': spotify.authorization_url()}), 200)


@app.route('/api/spotify/me', methods=('GET',))
def me():
    app.logger.info(f'session {session.get("spotify_id")}')
    spotify_user = SpotifyUser.find_user(id=session.get('spotify_id'))
    
    if not spotify_user:
        return redirect('/api/spotify/authorize')

    if not spotify_user.access_token:
        return redirect('/api/spotify/authorize')

    spotify_api = spotify.connect(spotify_user.access_token)

    return make_response(jsonify(spotify_api.me()), 200)
