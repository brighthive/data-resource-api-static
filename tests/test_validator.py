""" Unit tests for schema validator. """

import os
import json
from pocha import describe, it, before
from expects import expect, be, equal, raise_error, be_above
from outcomes_api import Validator, ValidatorNotFoundError,\
    SchemaFormatError

TEST_SCHEMA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'fixtures')

TEST_DATA = {
    'participant_id': '123456789',
    'program_code': '124ABC',
    'program_provider': 12345,
    'entry_date': '20190101',
    'exit_date': '20190101',
    'exit_type': 'Withdrew',
    'exit_reason': 'Personal'
}

BAD_TEST_DATA = {
    'participant_id': 123456789,
    'program_code': 26.5,
    'program_provider': '12345',
    'entry_date': '2019-01-01',
    'exit_date': '2019-01-01',
    'exit_type': 1,
    'exit_reason': 105.3
}


TEST_VALID_FIELDS = [
    {'good': 'I am a good string', 'bad': 123456, 'type': 'string'},
    {'good': 34, 'bad': 2345.2, 'type': 'integer'},
    {'good': 123456, 'bad': 'i am a bad integer', 'type': 'integer'},
    {'good': 3.14159, 'bad': 123456, 'type': 'float'},
    {'good': 1.5, 'bad': 'i am a bad float', 'type': 'float'},
    {'good': 'http://www.amazon.com', 'bad': 123456, 'type': 'url'},
    {'good': 'https://localhost:5000', 'bad': 'i am not a url', 'type': 'url'},
    {'good': '50.203.100.1:8080', 'bad': 10.4, 'type': 'url'},
    {'good': '20190101', 'bad': '20190134', 'type': 'date'},
    {'good': 20190101, 'bad': 2012222.4, 'type': 'date'},
    {'good': 20200104, 'bad': 'not a good date', 'type': 'date'},
    {'good': 'me@nowhere.com', 'bad': 'user_at_nowhere.com', 'type': 'email'},
    {'good': 'me@nowhere.info', 'bad': 123.456, 'type': 'email'},
]


@describe('Test Schema Validator')
def _():
    @it('Should successfully validate individual datatypes')
    def validate_data_types():
        validator = Validator(None)
        for field in TEST_VALID_FIELDS:
            if field['type'] == 'string':
                expect(validator.is_valid_string(field['good'])).to(be(True))
                expect(validator.is_valid_string(field['bad'])).to(be(False))
            elif field['type'] == 'integer':
                expect(validator.is_valid_integer(field['good'])).to(be(True))
                expect(validator.is_valid_integer(field['bad'])).to(be(False))
            elif field['type'] == 'float':
                expect(validator.is_valid_float(field['good'])).to(be(True))
                expect(validator.is_valid_float(field['bad'])).to(be(False))
            elif field['type'] == 'date':
                expect(validator.is_valid_date(field['good'])).to(be(True))
                expect(validator.is_valid_date(field['bad'])).to(be(False))
            elif field['type'] == 'url':
                expect(validator.is_valid_url(field['good'])).to(be(True))
                expect(validator.is_valid_url(field['bad'])).to(be(False))
            elif field['type'] == 'email':
                expect(validator.is_valid_email(field['good'])).to(be(True))
                expect(validator.is_valid_email(field['bad'])).to(be(False))

    @it('Should handle user-defined regex patterns for strings')
    def test_string_pattern():
        validator = Validator(None)
        value = 'I am as happy as a Clownfish'
        pattern_1 = "I am as happy as a [A-Za-z]+"
        pattern_2 = "I enjoy music and [A-Z]+"
        expect(validator.is_valid_string(value, pattern_1)).to(be(True))
        expect(validator.is_valid_string(value, pattern_2)).to(be(False))

    @it('Should handle user-defined date formats')
    def test_date_format():
        validator = Validator(None)
        date_1 = '2019-01-01'
        date_2 = '2019-06-05 05:45'
        pattern_1 = '%Y-%m-%d'
        pattern_2 = '%Y-%m-%d %H:%M'
        expect(validator.is_valid_date(date_1, pattern_1)).to(be(True))
        expect(validator.is_valid_date(date_1, pattern_2)).to(be(False))
        expect(validator.is_valid_date(date_2, pattern_2)).to(be(True))
        expect(validator.is_valid_date(date_2, pattern_1)).to(be(False))

    @it('Should handle user-defined minimum and maximum for integers')
    def test_min_max_int():
        validator = Validator(None)
        number = 5
        min = 0
        max = 10
        expect(validator.is_valid_integer(number, min, max)).to(be(True))
        expect(validator.is_valid_integer(number, min=min)).to(be(True))
        expect(validator.is_valid_integer(number, max=max)).to(be(True))
        expect(validator.is_valid_integer(number, max, min)).to(be(False))

    @it('Should handle user-defined minimum and maximum for floats')
    def _():
        validator = Validator(None)
        number = 5.25
        min = 0.65
        max = 10.2345
        expect(validator.is_valid_float(number, min, max)).to(be(True))
        expect(validator.is_valid_float(number, min=min)).to(be(True))
        expect(validator.is_valid_float(number, max=max)).to(be(True))
        expect(validator.is_valid_float(number, max, min)).to(be(False))

    @it('Should throw a "ValidatorNotFound" error if the validator does not ' +
        'exist')
    def validator_does_not_exist():
        schema_path = '/does/not/exist/file.json'
        validator = Validator(schema_path)
        expect(lambda: validator.validate(TEST_DATA)).to(
            raise_error(ValidatorNotFoundError))

    @it('Should throw a "SchemaFormatError" error if the schema is invalid')
    def invalid_schema():
        # first schema file is an incorrectly formatted JSON document
        schema_1 = os.path.join(TEST_SCHEMA_PATH, 'bad_schema_1.json')
        schema_2 = os.path.join(TEST_SCHEMA_PATH, 'bad_schema_2.json')

        # test for a badly formatted JSON document
        validator = Validator(schema_1)
        expect(lambda: validator.validate(TEST_DATA)).to(
            raise_error(SchemaFormatError))

        # test for a schema with missing elements
        validator = Validator(schema_2)
        expect(lambda: validator.validate(TEST_DATA)).to(
            raise_error(SchemaFormatError))

    @it('Should successfully validate a properly formed document')
    def validate_document():
        schema = os.path.join(TEST_SCHEMA_PATH, 'schema.json')
        validator = Validator(schema)

        # validate a known good document
        result = validator.validate(TEST_DATA)
        expect(len(result)).to(equal(0))

        # validate a bad document
        result = validator.validate(BAD_TEST_DATA)
        expect(len(result)).to(be_above(0))

    @it('Should successfully validate optional fields')
    def validate_optiona_fields():
        schema = os.path.join(TEST_SCHEMA_PATH, 'schema_optional.json')
        validator = Validator(schema)

        # validate a known good document
        result = validator.validate(TEST_DATA)
        expect(len(result)).to(equal(0))

        # validate a bad document
        result = validator.validate(BAD_TEST_DATA)
        expect(len(result)).to(be_above(0))
