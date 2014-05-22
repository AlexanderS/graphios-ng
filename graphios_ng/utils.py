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


class Template(string.Template):
    """
    This is a subclass of the default string.Template with the addition
    to allow braced expressions to have a modifier seperated with a pipe:

    Example:

        ${var|urlencode}

    Currently urlencode and filename are the only supported modifiers.
    Additional modifiers could be implemented by subclassing this class
    and adding modifier_<name> methods.
    """

    # This is manly copied from string.Template. The only addition
    # is the whole thing around the madifier group.
    pattern = r"""
    %(delim)s(?:
      (?P<escaped>%(delim)s)                            |
      (?P<named>%(id)s)                                 |
      {(?P<braced>%(id)s)(?:\|(?P<modifier>%(id)s))?}   |
      (?P<invalid>)
    )
    """ % {
        'delim': re.escape(string.Template.delimiter),
        'id': string.Template.idpattern,
    }

    def __init__(self, template):
        string.Template.__init__(self, template)
        self.pattern = self.RegexWrapper(self)

    def modifier_urlencode(self, result):
        return quote_plus(result)

    def modifier_filename(self, result):
        return get_valid_filename(result)

    class RegexWrapper(object):
        """
        This class wraps a compiled regular expression instance. This is
        nessesary because regular expressions are implemented as native c
        extension and it is not possible to monkey patch the sub function.

        The function to replace the matching groups in the Template class
        is implemented as inner function of the substitute and
        safe_substritute method and accessing the replacement mapping
        directly from the scope of the outer function.
        """
        def __init__(self, template):
            self.template = template
            self.pattern = template.pattern

        def sub(self, convert, pattern, count=0):
            def new_convert(mo):
                result = convert(mo)
                if mo.group('modifier') is not None:
                    modifier_name = "modifier_%s" % mo.group('modifier')
                    modifier = getattr(self.template, modifier_name)
                    return modifier(result)
                return result
            return self.pattern.sub(new_convert, pattern, count)
