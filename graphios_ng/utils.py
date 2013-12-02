from functools import wraps
import logging


def with_log(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        logger = logging.getLogger(func.__module__)
        if 'log' not in kwds:
            kwds['log'] = logger
        return func(*args, **kwds)
    return wrapper
