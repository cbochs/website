from flask_app import mongodb, scheduler, spotify_credentials
from flask_app.formatter.play_history import format_play_history
from flask_app.formatter.util import format_all
from flask_app.models.mysql.spotify_user import SpotifyUser
from flask_app.spotify.client import SpotifyClient


def watch_recently_played(spotify_id):
    job_id = f'recently_played_{spotify_id}'
    job = scheduler.get_job(job_id)

    if job is None:
        scheduler.add_job(
            job_id,
            _update_recently_played,
            args=[spotify_id],
            cron='')

    return job


def unwatch_recently_played(spotify_id):
    job_id = f'recently_played_{spotify_id}'
    scheduler.remove_job(job_id)


def _update_recently_played(spotify_id):
    spotify_user = SpotifyClient.find_user(id=spotify_id)
    spotify_token = spotify_user.api_token
    spotify_client = SpotifyClient(spotify_credentials, spotify_token)

    recently_played = format_all(
        spotify_client.recently_played(follow_cursor=True),
        format_play_history, spotify_user)

    history_collection = mongodb.db.listening_history
    history_collection.update_many({}, recently_played, upsert=True)
