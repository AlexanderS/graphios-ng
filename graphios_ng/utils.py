from functools import wraps
import logging
import re
import string
import unicodedata

try:
    from urllib import quote_plus        # pylint: disable=E0611
except ImportError:
    from urllib.parse import quote_plus  # pylint: disable=E0611,F0401


def with_log(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        logger = logging.getLogger(func.__module__)
        if 'log' not in kwds:
            kwds['log'] = logger
        return func(*args, **kwds)
    return wrapper


def get_valid_filename(s):
    s = s.strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def slugify(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = value.decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


class Formatter(string.Formatter):
    def __init__(self):
        pass

    def convert_field(self, value, conversion):
        if conversion is None:
            return value
        elif conversion == 'q':
            return quote_plus(value)
        elif conversion == 'f':
            return get_valid_filename(value)
        return string.Formatter.convert_field(self, value, conversion)
formatter = Formatter()
