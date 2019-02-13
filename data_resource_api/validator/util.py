""" validator/util.py

Utilities and methods to help with data validation.

"""

import re

# See: https://emailregex.com/
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

# See: https://codereview.stackexchange.com/questions/19663/http-url-validating
URL_REGEX = re.compile(
    r'(^(?:http|ftp)s?://)?'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


class ValidatorNotFoundError(Exception):
    """ Validator not found exception.

    A custom exception that should be raised whenever the specified data
    validator schema is not found.

    """

    def __init__(self, message):
        super(ValidatorNotFoundError, self).__init__(message)
        self.message = message


class SchemaFormatError(Exception):
    """ Schema validation failed exception.

    A custom exception that should be raised whenever a schema file cannot be
    validated.

    """

    def __init__(self, message):
        super(SchemaFormatError, self).__init__(message)
        self.message = message
