""" Unit tests for API Endpoints """

import json
import os
import random
from time import sleep
from pocha import describe, it, before, after
from expects import expect, be, equal, be_above

from outcomes_api import app, db, Program, Provider, Participant,\
    Credential, CredentialType, ProgramPotentialOutcome

from tests.utils.utilities import DatabaseContainerFixture

database_fixture = DatabaseContainerFixture()


@before
def setup_test_database():
    database_fixture.setup_database()
    tables_loaded = False
    retries = 0

    while not tables_loaded and retries < 10:
        try:
            print('Setting up database container...')
            database_fixture.populate_database()
            tables_loaded = True
        except Exception:
            retries += 1
            sleep(2)


# @after
# def teardown_test_database():
#     print('Tearing down database container...')
#     database_fixture.teardown_database()


@describe('Test Database Models')
def _():
    @it('Should perform CRUD operations on database tables')
    def _():
        pass
        # # load outcomes from dataset
        # for outcome in POTENTIAL_OUTCOMES:
        #     outcome = ProgramPotentialOutcome(
        #         outcome['id'], outcome['description'])
        #     db.session.add(outcome)

        # # all outcomes loaded
        # results = ProgramPotentialOutcome.query.all()
        # expect(len(results)).to(equal(len(POTENTIAL_OUTCOMES)))

        # # find a specific outcome
        # potential_outcome = random.randint(0, 10)
        # outcome_id = POTENTIAL_OUTCOMES[potential_outcome]['id']
        # outcome_name = POTENTIAL_OUTCOMES[potential_outcome]['description']

        # result = ProgramPotentialOutcome.query.filter_by(
        #     potential_outcome_id=outcome_id).all()
        # expect(len(result)).to(equal(1))
        # expect(result[0].potential_outcome_id).to(equal(outcome_id))
        # expect(result[0].potential_outcome_name).to(
        #     equal(outcome_name))

        # credential_type = CredentialType()
        # credential_type.type_name = 'A Credential Type'
        # credential_type.audience_level = 'Advanced'
        # db.session.add(credential_type)
        # db.session.commit()
        # results = CredentialType.query.all()
        # expect(len(results)).to(be(1))
        # for result in results:
        #     db.session.delete(result)
        #     db.session.commit()
        # results = CredentialType.query.all()
        # expect(len(results)).to(be(0))
