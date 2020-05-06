from .album import format_simple_album
from .artist import format_simple_artist
from .datetime import to_datetime
from .user import format_basic_user
from .util import format_all


def format_simple_track(result):
    if result['is_local']:
        return None

    track = {
        'album': format_simple_album(result['album']),
        'artists': format_all(result['artists'], format_simple_artist),
        'name': result['name'],
        'id': result['id'],
        'type': result['type']}

    return track


def format_track(result):
    if result['is_local']:
        return None

    track = {
        'album': format_simple_album(result['album']),
        'artists': format_all(result['artists'], format_simple_artist),
        'disc_number': result['disc_number'],
        'duration_ms': result['duration_ms'],
        'explicit': result['explicit'],
        'name': result['name'],
        'popularity': result['popularity'],
        'track_number': result['track_number'],
        'uri': result['uri'],
        'id': result['id'],
        'type': result['type']}

    return track


def format_saved_track(result, user):
    saved_track = {
        'added_at': to_datetime(result['added_at'], 'second'),
        'added_by': format_basic_user(user),
        'track': format_simple_track(result['track']),
        'type': 'saved_track'}

    return saved_track


def format_playlist_track(result):
    playlist_track = {
        'added_at': to_datetime(result['added_at'], 'second'),
        'added_by': format_basic_user(result['added_by']),
        'track': format_simple_track(result['track']),
        'type': 'playlist_track'}

    return playlist_track
