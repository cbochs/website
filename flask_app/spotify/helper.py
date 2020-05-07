import functools
from time import sleep

def retry(max_attempts=10, attempt_delay=1):
    def decorator(req):
        @functools.wraps(req)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts:
                try:
                    attempt = attempt + 1
                    result = req(*args, **kwargs)
                except:
                    sleep(attempt_delay)
                    continue
                return result
        return wrapper
    return decorator


def handle_cursor(cursor_loc=None, limit=0):
    """
    A decorator method to follow cursor-wrapped objects from Spotify's API.

    :param str cursor_loc:
    :param int limit:
    :rtype func
    """
    def decorator(api_call):
        @functools.wraps(api_call)
        def wrapper(self, *args, **kwargs):
            follow_cursor = kwargs.pop('follow_cursor', False)
            if follow_cursor:
                if limit > 0:
                    kwargs.update(limit=limit)

                results = api_call(self, *args, **kwargs)
                is_list = isinstance(results, list)
                results = results if is_list else [results]

                final_result = []
                for result in results:
                    if cursor_loc is not None:
                        cursor = result[cursor_loc]
                    else:
                        cursor = result

                    items = cursor['items']
                    while cursor['next']:
                        cursor = self._next(cursor)
                        items.extend(cursor['items'])

                    if cursor_loc is not None:
                        result[cursor_loc] = items
                    else:
                        result = items

                    final_result.append(result)

                # Convert back to hash if need be
                return final_result if is_list else final_result[0]
            else:
                return api_call(self, *args, **kwargs)
        return wrapper
    return decorator


def handle_bulk(limit):
    """
    A decorator method to handle bulk requests to Spotify's API.

    :param int limit
    :rtype func
    """
    def decorator(api_call):
        @functools.wraps(api_call)
        def wrapper(self, *args, **kwargs):
            call_name = api_call.__name__

            if isinstance(kwargs.get('ids'), list):
                item_ids = kwargs.pop('ids')
                items = []
                for ids in chunks(item_ids, limit):
                    kwargs.update(ids=','.join(ids))
                    items.extend(api_call(self, *args, **kwargs)[call_name])
                return items
            elif isinstance(kwargs.get('uris'), list):
                item_uris = kwargs.pop('uris')
                for uris in chunks(item_uris, limit):
                    api_call(self, *args, uris=uris, **kwargs)
            else:
                return api_call(self, *args, **kwargs)[call_name]
        return wrapper
    return decorator


def chunks(list_, n):
    for i in range(0, len(list_), n):
        yield list_[i:i+n]
