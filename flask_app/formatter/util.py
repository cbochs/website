

def format_custom(formatter, result, *args, **kwargs):
    return formatter(result, *args, **kwargs)


def format_all(result, formatter, *args, **kwargs):
    flambda = lambda r: formatter(r, *args, **kwargs)
    return list(filter(None, list(map(flambda, result))))


def my_map(func, iterable, *args, **kwargs):
    flambda = lambda i: func(i, *args, **kwargs)
    return list(map(flambda, iterable))


def my_filter(func, iterable, *args, **kwargs):
    if func is None:
        flambda = None
    else:
        flambda = lambda i: func(i, *args, **kwargs)
    return list(filter(flambda, iterable))


def map_then_filter(func_map, func_filter, iterable, *args, **kwargs):
    iterm = my_map(func_map, iterable, *args, **kwargs)
    return my_filter(func_filter, iterm, *args, **kwargs)


def filter_then_map(func_filter, func_map, iterable, *args, **kwargs):
    iterm = my_filter(func_filter, iterable, *args, **kwargs)
    return my_map(func_map, iterm, *args, **kwargs)


def flatten(lst):
    return [l for ls in lst for l in ls]