from datetime import datetime

# DEFINE A FEW STANDARD DATETIME STYLES
DATETIME_FORMAT_MS = '%Y-%m-%dT%H:%M:%S.%fZ'
DATETIME_FORMAT_LONG = '%Y-%m-%dT%H:%M:%SZ'
DATETIME_FORMAT_SHORT = '%Y-%m-%d'
DATETIME_FORMAT_YR_MTH = '%Y-%m'
DATETIME_FORMAT_YEAR = '%Y'

DATETIME_FORMAT_DEFAULT = '%Y-%m-%dT%H:%M:%SZ'
DATETIME_FORMAT_FILENAME = '%Y-%m-%dT%H-%M-%SZ'

DATETIME_FORMAT_ECMA = '%Y-%m-%dT%H:%M:%S.%f+0000'

lookup = {
    'ms': DATETIME_FORMAT_MS,
    'second': DATETIME_FORMAT_LONG,
    'day': DATETIME_FORMAT_SHORT,
    'month': DATETIME_FORMAT_YR_MTH,
    'year': DATETIME_FORMAT_YEAR}


def to_datetime(date_string, precision):
    if isinstance(date_string, datetime):
        return date_string

    if precision not in lookup or date_string == '0000':
        return None

    return datetime.strptime(date_string, lookup[precision])


def from_datetime(date_obj, precision):
    if isinstance(date_obj, str):
        return date_obj

    datetime_format = lookup[precision] if precision in lookup else precision
    return datetime.strftime(date_obj, datetime_format)
