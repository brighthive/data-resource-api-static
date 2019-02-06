""" validator/validator.py

A data validation class that leverages external JSON configuration
files to validate data provided by API consumers.

"""

import json
import os
from datetime import datetime
from validator.util import ValidatorNotFoundError, SchemaFormatError


class Validator(object):
    """ Generic validator class.

    This class implements all the infrastructure necessary for validating an
    object.

    Attributes:
        schema_path (str): Full path and name of the schema file to validate
        data against.

    Args:
        schema_path (str): Full path and name of the schema to validate data
        against.

    """

    def __init__(self, schema_path):
        self.schema_path = schema_path

    def field_exists(self, field: str, dataset: dict):
        """ Determine if the field exists. """
        return field in dataset.keys()

    def is_valid_string(self, text, pattern=None):
        """ Determine if an item is a valid string. """
        is_valid = False
        if isinstance(text, str):
            is_valid = True
        return is_valid

    def is_valid_integer(self, text, min=None, max=None):
        """ Determine if an item is a valid string. """
        is_valid = False
        if isinstance(text, int):
            is_valid = True
        return is_valid

    def is_valid_float(self, text, min=None, max=None):
        """ Determine if an item is a valid string. """
        is_valid = False
        if isinstance(text, float):
            is_valid = True
        return is_valid

    def is_valid_url(self, text):
        """ Determine if an item is a valid string. """
        is_valid = False
        return is_valid

    def is_valid_email(self, text):
        """ Determine if an item is a valid string. """
        is_valid = False
        return is_valid

    def is_valid_date(self, text, format="%Y%m%d"):
        """ Determine if an item is a valid date. """
        is_valid = False
        try:
            date = datetime.strptime(str(text), format)
            is_valid = True
        except Exception:
            pass
        return is_valid

    def validate(self, dataset: dict):
        """ Validate a dataset to ensure that it conforms to a schema.

        Parameters:
            dataset (dict): Dataset (represented as a Python dictionary) to
            apply validation rules to.

        """
        errors = []
        if not os.path.exists(self.schema_path) or not os.path.isfile(
                self.schema_path):
            raise ValidatorNotFoundError(
                'The specified validator ({}) does not exist'.format(
                    self.schema_path))
        else:
            try:
                with open(self.schema_path, 'r') as f:
                    schema = json.load(f)
            except Exception:
                raise(SchemaFormatError(
                    'Failed to load schema from {}'.format(self.schema_path)))

            try:
                for field in schema['schema']:
                    if not self.field_exists(field['field'], dataset):
                        if field['required'] == 'true':
                            errors.append(
                                "Field '{0}' is required and cannot be blank."
                                .format(field['field']))
                    else:
                        field_type = field['type']
                        if field_type == 'string':
                            print('string')
                            if field['pattern']:
                                print('...... has a pattern')
                        elif field_type == 'integer':
                            print('integer')
                            if field['min']:
                                print('...... has a minimum value')
                            if field['max']:
                                print('...... has a maximum value')
                        elif field_type == 'float':
                            if field['min']:
                                print('...... has a minimum value')
                            if field['max']:
                                print('...... has a maximum value')
                        elif field_type == 'url':
                            print('url')
                        elif field_type == 'email':
                            print('email')
                        elif field_type == 'date':
                            print('date')
                            if field['format']:
                                print('...... has a date format')
                return errors
            except Exception as e:
                raise(SchemaFormatError(
                    'Schema format error detected in schema {}'.format(
                        self.schema_path)))
