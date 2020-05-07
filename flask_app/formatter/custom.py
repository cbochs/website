from .datetime import to_datetime
from .playlist import format_playlist


def format_watched_playlist(result, snapshots, last_checked, last_updated):
    playlist = {
        'playlist': format_playlist(result),
        'snapshots': snapshots,
        'last_checked': to_datetime(last_checked, 'second'),
        'last_updated': to_datetime(last_updated, 'second'),
        'type': 'watched_playlist'}

    return playlist


def format_snapshot(result, old_fields, new_fields):
    snapshot = {
        'changed_at': to_datetime(result['changed_at'], 'second'),
        'tracks': result['tracks'],
        'snapshot_id': result['snapshot_id'],
        'prev_snapshot': result['prev_snapshot'],
        'next_snapshot': result['next_snapshot'],
        'old_fields': old_fields,
        'new_fields': new_fields,
        'change': result['change'],
        'type': 'snapshot'}

    return snapshot
