def format_all(result, formatter, *args, **kwargs):
    flambda = lambda r: formatter(r, *args, **kwargs)
    return list(filter(None, list(map(flambda, result))))
