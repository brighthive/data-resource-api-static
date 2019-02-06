""" Unit tests for schema validator. """

import os
import json
from pocha import describe, it, before
from expects import expect, be, equal, raise_error
from validator import Validator, ValidatorNotFoundError, SchemaFormatError

TEST_SCHEMA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'fixtures')

TEST_DATA = {
    'participant_id': '123456789',
    'program_code': '124ABC',
    'program_provider': 12345,
    'entry_date': '01/01/2019',
    'exit_date': '01/01/2019',
    'exit_type': 'Withdrew',
    'exit_reason': 'Personal'
}

TEST_VALID_FIELDS = [
    {'good': 'I am a good string', 'bad': 123456, 'type': 'string'},
    {'good': 34, 'bad': 2345.2, 'type': 'integer'},
    {'good': 123456, 'bad': 'i am a bad integer', 'type': 'integer'},
    {'good': 3.14159, 'bad': 123456, 'type': 'float'},
    {'good': 1.5, 'bad': 'i am a bad float', 'type': 'float'},
    {'good': 'http://www.amazon.com', 'bad': 123456, 'type': 'url'},
    {'good': 'https://localhost:5000', 'bad': 'i am not a url', 'type': 'url'},
    {'good': '50.203.100.1', 'bad': 10.4, 'type': 'url'},
    {'good': '20190101', 'bad': '20190134', 'type': 'date'},
    {'good': 20190101, 'bad': 2012222.4, 'type': 'date'},
    {'good': 20200104, 'bad': 'not a good date', 'type': 'date'}
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

    # @it('Should successfully validate a properly formed document')
    # def validate_document():
    #     schema = os.path.join(TEST_SCHEMA_PATH, 'schema.json')
    #     validator = Validator(schema)
    #     result = validator.validate(TEST_DATA)
    #     expect(len(result)).to(equal(0))
        # print(result)
