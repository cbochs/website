from .track import format_playlist_track
from .user import format_simple_user
from .util import format_all


def format_simple_playlist(result):
    playlist = {
        'name': result['name'],
        'id': result['id'],
        'type': result['type']}

    return playlist


def format_playlist(result):
    playlist = {
        'collaborative': result['collaborative'],
        'description': result['description'],
        'followers': result['followers']['total'],
        'name': result['name'],
        'owner': format_simple_user(result['owner']),
        'public': result['public'],
        'snapshot_id': result['snapshot_id'],
        'tracks': format_all(result['tracks'], format_playlist_track),
        'uri': result['uri'],
        'id': result['id'],
        'type': result['type']}

    return playlist
