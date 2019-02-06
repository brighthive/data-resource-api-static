""" validator/util.py

Utilities and methods to help with data validation.

"""


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
