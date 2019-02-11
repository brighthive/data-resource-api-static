""" Unit tests for API Endpoints """

import json
from pocha import describe, it, before
from expects import expect, be, equal, be_above

from outcomes_api import app, db, Program, Provider, Participant,\
    Credential, CredentialType


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
