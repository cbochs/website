from flask import jsonify, request, redirect, make_response

from flask_app import app, spotify
from flask_app.models.mysql.spotify_access_token import SpotifyAccessToken
from flask_app.models.mysql.spotify_user import SpotifyUser
from flask_app.spotify.oauth import SpotifyOAuth

@app.route('/api/spotify/authorize', methods=('GET',))
def spotify_authorize():
    error = request.values.get('error')
    code = request.values.get('code')

    # TODO: check the session that the user isn't already authenticated
    
    if error:
        app.logger.error(f'Could not authorize user {user}. Error: {error}')
        return make_response('Unauthorized.', 401)
    elif code:
        token_info = spotify.request_access_token(code)

        spotify_api = spotify.connect(token_info)
        me = spotify_api.me()

        access_token = SpotifyAccessToken(token_info)
        spotify_user = SpotifyUser(me)

        app.logger.info(f'token info: {token_info}')
        app.logger.info(f'me: {me}')

        app.logger.info('Obtained access code!')
        return make_response('Authorized user.', 200)
    else:
        app.logger.info('Requesting Spotify access code')
        return redirect(spotify.authorization_url())


@app.route('/api/spotify/me', methods=('GET',))
def me():
    pass
    # TODO: check the session that the user isn't already authenticated





# @app.route('/spotify/recently_played')
# def recently_played():
#     credentials = SpotifyClientCredentials(app=app)
#     token_info = SpotifyOAuth.load_token_info(credentials)
#     spotify = Spotify(token_info, credentials)

#     me = spotify.me()
#     recently_played = spotify.recently_played(follow_cursor=True)
#     recently_played = format_all(recently_played, format_play_history, user=me)

#     return jsonify(recently_played)

# @app.route('/spotify/playlists')
# def playlists():
#     credentials = SpotifyClientCredentials(app=app)
#     token_info = SpotifyOAuth.load_token_info(credentials)
#     spotify = Spotify(token_info, credentials)

#     playlists = spotify.my_playlists(follow_cursor=True)
#     playlists = format_all(playlists, format_simple_playlist)
    
#     return jsonify(playlists)
