from flask import jsonify, make_response, redirect, request, session

from flask_app import app, spotify_credentials, mysqldb
from flask_app.models.mysql.spotify_token import SpotifyToken
from flask_app.models.mysql.spotify_user import SpotifyUser
from flask_app.models.mysql.user import User
from flask_app.spotify.client import SpotifyClient
from flask_app.spotify.oauth import SpotifyOAuth
from flask_app.scheduler.playlist import _update_playlist
from flask_app.scheduler.recently_played import _update_recently_played

def requires_spotify_authorization(route):
    def wrapper(*args, **kwargs):
        spotify_user = SpotifyUser.find_user(id=session.get('spotify_id'))
        if not spotify_user:
            return redirect('/api/spotify/authorize')

        spotify_token = spotify_user.api_token
        if not spotify_token:
            return redirect('/api/spotify/authorize')

        return route(*args, **kwargs)
    return wrapper

# TODO: if the spotify user is in the db, but doesn't have a token we should
#       still re-authorize the user
@app.route('/spotify/authorize', methods=('POST',))
def spotify_authorize():
    spotify_user = SpotifyUser.find_user(id=session.get('spotify_id'))
    if spotify_user:
        app.logger.info(f'Spotify user already authorized in session {spotify_user}')
        return make_response('Authorized.', 200)

    user = User.find_user(id=session.get('user_id'))
    if user and user.spotify_user:
        session['spotify_id'] = user.spotify_user.id
        app.logger.info(f'User is already authorized with valid spotify user {user}')
        return make_response('Authorized.', 200)

    data = request.get_json()
    error = data.get('error')
    code = data.get('code')

    if error:
        app.logger.error(f'Could not authorize user {user}. Error: {error}')
        return make_response('Unauthorized.', 401)
    elif code:
        try:
            token_info = SpotifyOAuth.request_access_token(spotify_credentials, code)
        except SpotifyOAuthException as e:
            app.logger.error(e)
            return make_response('Unauthorized', 401)

        spotify_token = SpotifyToken(**token_info)
        spotify_client = SpotifyClient(spotify_credentials, spotify_token)
        me = spotify_client.me()

        spotify_user = SpotifyUser.find_user(id=me['id'])
        if spotify_user:
            session['spotify_id'] = spotify_user.id
            app.logger.info(f'Spotify user already authorized, but not in session {spotify_user}')
            return make_response('Authorized.', 200)

        spotify_user = SpotifyUser(**me, user=user)
        spotify_token.spotify_id = spotify_user.id # must add spotify id

        mysqldb.session.add(spotify_token)
        mysqldb.session.add(spotify_user)
        mysqldb.session.commit()

        session['spotify_id'] = spotify_user.id

        app.logger.info(f'Created new user! {spotify_user}')
        return make_response('Authorized.', 201)
    else:
        app.logger.info('Could not find code or error in request')
        return make_response('Unauthorized', 200)


@app.route('/spotify/authorization_url', methods=('GET',))
def spotify_authorization_url():
    authorization_url = SpotifyOAuth.authorization_url(spotify_credentials)
    app.logger.info('Requesting Spotify access code')
    return make_response(jsonify({'auth_url': authorization_url}), 200)


@requires_spotify_authorization
@app.route('/spotify/me', methods=('GET',))
def spotify_me():
    spotify_user = SpotifyUser.find_user(id=session.get('spotify_id'))
    spotify_token = spotify_user.api_token
    spotify_client = SpotifyClient(spotify_credentials, spotify_token)

    return make_response(jsonify(spotify_client.me()), 200)


@requires_spotify_authorization
@app.route('/spotify/watch/playlist', methods=('POST',))
def spotify_watch_playlist():
    data = request.get_json()
    playlist_id = data.get('playlist_id')
    spotify_id = session.get('spotify_id')
    _update_playlist(spotify_id, playlist_id)
    return make_response('Not implemented', 200)


@requires_spotify_authorization
@app.route('/spotify/watch/recently_played', methods=('POST',))
def spotify_watch_recently_played():
    spotify_id = session.get('spotify_id')
    _update_recently_played(spotify_id)
    return make_response('Not implemented', 200)
