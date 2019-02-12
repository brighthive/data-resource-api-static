""" Unit tests for API Endpoints """

import json
import os
from time import sleep
from pocha import describe, it, before, after
from expects import expect, be, equal, be_above

from outcomes_api import app, db, Program, Provider, Participant,\
    Credential, CredentialType

from tests.utils.utilities import DatabaseContainerFixture

database_fixture = DatabaseContainerFixture()


@before
def setup_test_database():
    database_fixture.setup_database()
    tables_loaded = False
    retries = 0

    while not tables_loaded and retries < 10:
        try:
            print('Setting up database...')
            database_fixture.populate_database()
            tables_loaded = True
        except Exception:
            retries += 1
            sleep(2)


@after
def teardown_test_database():
    database_fixture.teardown_database()


@describe('Test Database Models')
def _():
    @it('Should perform CRUD operations on credential types')
    def _():
        credential_type = CredentialType()
        credential_type.type_name = 'A Credential Type'
        credential_type.audience_level = 'Advanced'
        db.session.add(credential_type)
        db.session.commit()
        results = CredentialType.query.all()
        expect(len(results)).to(be(1))
        for result in results:
            db.session.delete(result)
            db.session.commit()
        results = CredentialType.query.all()
        expect(len(results)).to(be(0))
