from base64 import b64decode
from datetime import datetime

import flask_app.utils.myers as myers
from flask_app import mongodb, scheduler, spotify_credentials
from flask_app.formatter.custom import format_snapshot, format_watched_playlist
from flask_app.models.mysql.spotify_user import SpotifyUser
from flask_app.spotify.client import SpotifyClient


def watch_playlist(playlist_id):
    job_id = f'playlist_{playlist_id}'
    job = scheduler.get_job(job_id)

    if job is None:
        scheduler.add_job(
            job_id,
            _update_playlist,
            args=[playlist_id],
            cron='')


def unwatch_playlist(playlist_id):
    job_id = f'playlist_{playlist_id}'
    scheduler.remove_job(job_id)


def _update_playlist(playlist_id):
    spotify_user = SpotifyClient.find_user(id=spotify_id)
    spotify_token = spotify_user.api_token
    spotify_client = SpotifyClient(spotify_credentials, spotify_token)

    new_snapshot_id = spotify_client.playlist(playlist_id, fields='snapshot_id')
    old_snapshot_id = '' # TODO

    if new_snapshot_id != old_snapshot_id:
        new_playlist = spotify_client.playlist(playlist_id, follow_cursor=True)
        old_playlist = '' # TODO
        snapshot = _create_snapshot(old_playlist, new_playlist)


def _create_snapshot(old_playlist, new_playlist):
    snapshot = {
        'changed_at': datetime.utcnow(),
        'tracks': _create_patch(old_playlist, new_playlist),
        'snapshot_id': new_playlist['snapshot_id'],
        'prev_snapshot': None, # old_playlist['last_snapshot'],
        'next_snapshot': None,
        'change': int(b64decode(new_playlist['snapshot_id'])
                     .decode('ascii')
                     .split(',')[0])}

    old_fields = {
        ef: old_playlist[ef]
        for ef in ['collaborative', 'description', 'name', 'public']
        if old_playlist[ef] != new_playlist[ef]}

    new_fields = {
        ef: new_playlist[ef]
        for ef in ['collaborative', 'description', 'name', 'public']
        if old_playlist[ef] != new_playlist[ef]}

    return format_snapshot(snapshot, old_fields, new_fields)


def _create_patch(old_playlist, new_playlist):
    steps = myers.diff(
        old_playlist['tracks'],
        new_playlist['tracks'],
        key=lambda pl: pl['track']['id'])

    patch = []

    for px, py, nx, ny in steps:
        if px == nx: # insert new track
            patch.append((px, py, nx, ny, new_playlist['tracks'][py]))
        elif py == ny: # remove old track
            patch.append((px, py, nx, ny, old_playlist['tracks'][px]))

    return patch


def _apply_snapshot(old_playlist, snapshot):
    x, i = 0, 0

    patch = snapshot.pop('tracks')
    new_tracks = []

    while x < len(old_playlist['tracks']) or i < len(patch):
        if i < len(patch):
            px, py, nx, ny, nt = patch[i]
        else:
            px, py, nx, ny, nt = -1, -1, -1, -1, None

        if x == px:
            if px == nx:
                new_tracks.append(nt)
            else:
                x = x + 1 # remove track
            i = i + 1
        else:
            new_tracks.append(old_playlist['tracks'][x])
            x = x + 1

    new_playlist = {
        **old_playlist,
        'tracks': new_tracks,
        **snapshot['new_fields']}

    return new_playlist


def _revert_snapshot(new_playlist, snapshot):
    y, i = 0, 0

    patch = snapshot.pop('tracks')
    old_tracks = []

    while y < len(new_playlist['tracks']) or i < len(patch):
        if i < len(patch):
            px, py, nx, ny, ot = patch[i]
        else:
            px, py, nx, ny, ot = -1, -1, -1, -1, None

        if y == py:
            if py == ny:
                old_tracks.append(ot)
            else:
                y = y + 1
            i = i + 1
        else:
            old_tracks.append(new_playlist['tracks'][y])
            y = y + 1

    old_playlist = {
        **new_playlist,
        'tracks': old_tracks,
        **snapshot['old_fields']}

    return old_playlist
