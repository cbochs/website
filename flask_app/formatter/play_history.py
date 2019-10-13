from flask_app.formatter.datetime import to_datetime
from flask_app.formatter.track import format_simple_track
from flask_app.formatter.user import format_simple_user


def format_play_history(result, user):
    play_history = {
        'context': result['context'],
        'played_at': to_datetime(result['played_at'], 'ms'),
        'track': format_simple_track(result['track']),
        'user': format_simple_user(user),
        'type': 'play_history'}
    
    return play_history
