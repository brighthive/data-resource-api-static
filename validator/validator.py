""" validator/validator.py

A data validation class that leverages external JSON configuration
files to validate data provided by API consumers.

"""

import json
import os
import re
from datetime import datetime
from validator.util import ValidatorNotFoundError, SchemaFormatError, \
    EMAIL_REGEX, URL_REGEX


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
        try:
            if isinstance(text, str):
                is_valid = True
                if pattern is not None:
                    matcher = re.compile(pattern)
                    if matcher.match(text):
                        is_valid = True
                    else:
                        is_valid = False
        except Exception:
            is_valid = False
        return is_valid

    def is_valid_integer(self, text, min=None, max=None):
        """ Determine if an item is a valid string. """
        is_valid = False
        try:
            if isinstance(text, int):
                is_valid = True
                if is_valid and min is not None:
                    if int(text) < int(min):
                        is_valid = False
                if is_valid and max is not None:
                    if int(text) > int(max):
                        is_valid = False
        except Exception:
            is_valid = False
        return is_valid

    def is_valid_float(self, text, min=None, max=None):
        """ Determine if an item is a valid float. """
        is_valid = False
        try:
            if isinstance(text, float):
                is_valid = True
                if is_valid and min is not None:
                    if float(text) < float(min):
                        is_valid = False
                if is_valid and max is not None:
                    if float(text) > float(max):
                        is_valid = False
        except Exception:
            is_valid = False
        return is_valid

    def is_valid_url(self, text):
        """ Determine if an item is a valid string. """
        is_valid = False
        try:
            if URL_REGEX.match(text):
                is_valid = True
        except Exception:
            pass
        return is_valid

    def is_valid_email(self, text):
        """ Determine if an item is a valid string. """
        is_valid = False
        try:
            if EMAIL_REGEX.match(text):
                is_valid = True
        except Exception:
            pass
        return is_valid

    def is_valid_date(self, text, format=None):
        """ Determine if an item is a valid date. """
        is_valid = False
        try:
            if format is None:
                format = "%Y%m%d"
            date = datetime.strptime(str(text), format)
            is_valid = True
        except Exception:
            is_valid = False
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
                    current_field = field['field']
                    if not self.field_exists(current_field, dataset):
                        if field['required'] == 'true':
                            errors.append(
                                "Field '{0}' is required and cannot be blank."
                                .format(current_field))
                    else:
                        field_type = field['type']
                        if field_type == 'string':
                            if 'pattern' in field.keys():
                                pattern = field['pattern']
                            else:
                                pattern = None

                            if not self.is_valid_string(dataset[current_field],
                                                        pattern):
                                errors.append(
                                    'Field {} is not a valid string'.format(
                                        current_field))
                        elif field_type == 'integer':
                            if 'min' in field.keys():
                                min = field['min']
                            else:
                                min = None
                            if 'max' in field.keys():
                                max = field['max']
                            else:
                                max = None
                            if not self.is_valid_integer(
                                    dataset[current_field], min, max):
                                errors.append(
                                    'Fiels {} is not a valid integer'.format(
                                        current_field))
                        elif field_type == 'float':
                            if 'min' in field.keys():
                                min = field['min']
                            else:
                                min = None
                            if 'max' in field.keys():
                                max = field['max']
                            else:
                                max = None
                            if not self.is_valid_float(
                                    dataset[current_field], min, max):
                                errors.append(
                                    'Fiels {} is not a valid integer'.format(
                                        current_field))
                        elif field_type == 'url':
                            if not self.is_valid_url(dataset[current_field]):
                                errors.append(
                                    'Field {} is not a valid URL'.format(
                                        current_field))
                        elif field_type == 'email':
                            if not self.is_valid_date(dataset[current_field]):
                                errors.append(
                                    'Field {} is not a valid email address'
                                    .format(current_field))
                        elif field_type == 'date':
                            if 'format' in field.keys():
                                format = field['format']
                            else:
                                format = None
                            if not self.is_valid_date(dataset[current_field],
                                                      format):
                                errors.append('Field {} is not a valid date.')
                return errors
            except Exception as e:
                raise(SchemaFormatError(
                    'Schema format error detected in schema {}'.format(
                        self.schema_path)))
