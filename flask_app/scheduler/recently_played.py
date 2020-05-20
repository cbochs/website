from flask_app import app, mongodb, my_scheduler, spotify_credentials
from flask_app.formatter.play_history import format_play_history
from flask_app.formatter.util import format_all
from flask_app.models.mysql.spotify_user import SpotifyUser
from flask_app.spotify.client import SpotifyClient
from pymongo.errors import BulkWriteError


def watch_recently_played(spotify_id):
    job_id = f'recently_played_{spotify_id}'
    job = my_scheduler.get_job(job_id)

    if job is None:
        job = my_scheduler.add_job(
            job_id,
            update_recently_played,
            args=[spotify_id],
            trigger='cron',
            hour='*/2',
            jitter=120)
        app.logger.info(f'Job added. job_id={job_id}')

    return job


def unwatch_recently_played(spotify_id):
    job_id = f'recently_played_{spotify_id}'
    my_scheduler.remove_job(job_id)
    app.logger.info(f'Job removed. job_id={job_id}')


def update_recently_played(spotify_id):
    spotify_user = SpotifyUser.find_user(id=spotify_id)
    spotify_token = spotify_user.api_token
    spotify_client = SpotifyClient(spotify_credentials, spotify_token)

    recently_played = format_all(
        spotify_client.recently_played(follow_cursor=True),
        format_play_history, spotify_user.__dict__)

    try:
        history_collection = mongodb.db.recently_played
        history_collection.insert_many(recently_played, ordered=False)
    except BulkWriteError as e:
        pass
    app.logger.info(f'Recently played updated. spotify_id={spotify_id}')
