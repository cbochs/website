from .track import format_playlist_track
from .user import format_simple_user
from .util import format_all
from .datetime import to_datetime

def format_custom_playlist(result, snapshots, last_checked, last_updated):
    playlist = {
        'collaborative': result['collaborative'],
        'description': result['description'],
        'followers': result['followers']['total'],
        'name': result['name'],
        'owner': format_simple_user(result['owner']),
        'public': result['public'],
        'snapshots': snapshots,
        'snapshot_id': result['snapshot_id'],
        'last_checked': to_datetime(last_checked, 'second'),
        'last_updated': to_datetime(last_updated, 'second'),
        'tracks': format_all(result['tracks'], format_playlist_track),
        'uri': result['uri'],
        'id': result['id'],
        'type': result['type']}

    return playlist


def format_custom_snapshot(result, old_fields, new_fields):
    snapshot = {
        'changed_at': to_datetime(result['changed_at'], 'second'),
        'tracks': result['tracks'],
        'snapshot_id': result['snapshot_id'],
        'prev_snapshot': result['prev_snapshot'],
        'next_snapshot': result['next_snapshot'],
        'old_fields': old_fields,
        'new_fields': new_fields,
        'change': result['change']}

    return snapshot