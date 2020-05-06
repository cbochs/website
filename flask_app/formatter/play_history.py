from .datetime import to_datetime
from .track import format_simple_track
from .user import format_basic_user


def format_play_history(result, user):
    play_history = {
        'context': result['context'],
        'played_at': to_datetime(result['played_at'], 'ms'),
        'track': format_simple_track(result['track']),
        'user': format_basic_user(user),
        'type': 'play_history'}

    return play_history
