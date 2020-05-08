from base64 import b64decode
from datetime import datetime

import flask_app.utils.myers as myers
from flask_app import app, mongodb, scheduler, spotify_credentials
from flask_app.formatter.custom import (format_patch_step, format_snapshot,
                                        format_watched_playlist)
from flask_app.formatter.playlist import format_playlist
from flask_app.models.mysql.spotify_user import SpotifyUser
from flask_app.spotify.client import SpotifyClient


def watch_playlist(spotify_id, playlist_id):
    job_id = f'playlist_{playlist_id}'
    job = scheduler.get_job(job_id)

    if job is None:
        scheduler.add_job(
            job_id,
            _update_playlist,
            args=[spotify_id, playlist_id],
            cron='')


def unwatch_playlist(playlist_id):
    job_id = f'playlist_{playlist_id}'
    scheduler.remove_job(job_id)


def _update_playlist(spotify_id, playlist_id):
    spotify_user = SpotifyUser.find_user(id=spotify_id)
    spotify_token = spotify_user.api_token
    spotify_client = SpotifyClient(spotify_credentials, spotify_token)

    playlist_collection = mongodb.db.playlists
    snapshot_collection = mongodb.db.snapshots

    playlist = playlist_collection.find_one({'playlist.id': playlist_id})

    if playlist is None:
        timestamp = datetime.utcnow()
        new_playlist = format_watched_playlist(
            spotify_client.playlist(playlist_id, follow_cursor=True),
            [], timestamp, timestamp)

        playlist_collection.insert_one(new_playlist)
        app.logger.info(f'Playlist added. playlist_id={playlist_id}')
        return

    old_snapshot_id = playlist['playlist']['snapshot_id']
    new_snapshot_id = spotify_client.playlist(playlist_id, fields='snapshot_id')['snapshot_id']

    timestamp = datetime.utcnow()

    if new_snapshot_id == old_snapshot_id:
        playlist_collection.update_one(
            {'playlist.id': playlist_id},
            {'$set': {'last_checked': timestamp}})
        app.logger.info(f'Playlist unchanged. playlist_id={playlist_id}')
        return

    new_playlist = format_playlist(spotify_client.playlist(playlist_id, follow_cursor=True))
    new_snapshot = _create_snapshot(playlist['playlist'], new_playlist, timestamp)

    # Apparently Discover Weekly updates A LOT, even without changes. Throw away
    # snapshots when they don't contain any deltas
    if len(new_snapshot['tracks']) == 0 and len(new_snapshot['new_fields']) == 0:
        playlist_collection.update_one(
            {'playlist.id': playlist_id},
            {'$set': {'last_checked': timestamp}})
        app.logger.info(f'Playlist updated without changes. playlist_id={playlist_id}')
        return

    old_snapshot = snapshot_collection.find_one({'snapshot_id': old_snapshot_id})
    if old_snapshot is not None:
        new_snapshot['prev_snapshot'] = old_snapshot['snapshot_id']

        snapshot_collection.update_one(
            {'snapshot_id': old_snapshot['snapshot_id']},
            {'$set': {'next_snapshot': new_snapshot['snapshot_id']}})
        app.logger.info(f"Snapshot updated. snapshot_id={old_snapshot['snapshot_id']}")

    snapshot_collection.insert_one(new_snapshot)
    app.logger.info(f"Snapshot added. snapshot_id={new_snapshot['snapshot_id']}")

    playlist_collection.update_one(
        {'playlist.id': playlist_id},
        {'$set': {
            'playlist': new_playlist,
            'snapshots': playlist['snapshots'] + [new_snapshot['snapshot_id']],
            'last_checked': timestamp,
            'last_updated': timestamp}})
    app.logger.info(f"Playlist updated. playlist_id={playlist_id}, snapshot_id={new_snapshot['snapshot_id']}")


def _create_snapshot(old_playlist, new_playlist, timestamp=None):
    snapshot = {
        'changed_at': timestamp or datetime.utcnow(),
        'tracks': _create_patch(old_playlist, new_playlist),
        'snapshot_id': new_playlist['snapshot_id'],
        'prev_snapshot': None,
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
            patch.append(format_patch_step(px, py, nx, ny, new_playlist['tracks'][py]))
        elif py == ny: # remove old track
            patch.append(format_patch_step(px, py, nx, ny, old_playlist['tracks'][px]))

    return patch


def _apply_snapshot(old_playlist, snapshot):
    x, i = 0, 0

    patch = snapshot.pop('tracks')
    new_tracks = []

    while x < len(old_playlist['tracks']) or i < len(patch):
        if i < len(patch):
            step = patch[i]
            px, py = step['px'], step['py']
            nx, ny = step['nx'], step['ny']
            nt = step['tr']
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
