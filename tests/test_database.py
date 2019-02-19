""" Unit tests for API Endpoints """

import json
import os
import random
from time import sleep
from pocha import describe, it, before, after
from expects import expect, be, equal, be_above

from data_resource_api import app, db, Program, Provider, Participant,\
    Credential, CredentialType, ProgramPotentialOutcome,\
    ProgramPrerequisite, EntityType, GeographicLocation,\
    PhysicalAddress

from tests.utils.utilities import DatabaseContainerFixture

database_fixture = DatabaseContainerFixture()

# Test Directory Home
TEST_DIR = os.path.dirname(os.path.abspath(__file__))

# Sample data in JSON format
JSON_FIXTURES = os.path.join(TEST_DIR, 'fixtures', 'sample')

# Sample data files
PROGRAM_PREREQUISITES = os.path.join(
    JSON_FIXTURES, 'program_prerequisites.json')
PROGRAM_POTENTIAL_OUTCOMES = os.path.join(
    JSON_FIXTURES, 'program_potential_outcomes.json')
ENTITY_TYPES = os.path.join(JSON_FIXTURES, 'entity_types.json')
CREDENTIAL_TYPES = os.path.join(JSON_FIXTURES, 'credential_types.json')
PROVIDERS = os.path.join(JSON_FIXTURES, 'providers.json')
LOCATIONS = os.path.join(JSON_FIXTURES, 'locations.json')
ADDRESSES = os.path.join(JSON_FIXTURES, 'addresses.json')
CREDENTIALS = os.path.join(JSON_FIXTURES, 'credentials.json')
PROGRAMS = os.path.join(JSON_FIXTURES, 'programs.json')
PARTICIPANTS = os.path.join(JSON_FIXTURES, 'participants.json')


@before
def setup_test_database():
    database_fixture.setup_database()
    tables_loaded = False
    retries = 0

    while not tables_loaded and retries < 10:
        try:
            database_fixture.populate_database()
            tables_loaded = True
        except Exception:
            retries += 1
            sleep(1)


@after
def teardown_test_database():
    database_fixture.teardown_database()


@describe('Test Database Models')
def _():
    @it('Should perform CRUD operations on database tables')
    def _():
        # load program prerequisites:
        with open(PROGRAM_PREREQUISITES, 'r') as f:
            data = json.load(f)

        for item in data['program_prerequisites']:
            prereq = ProgramPrerequisite(item['name'], item['id'])
            db.session.add(prereq)
        db.session.commit()
        result = ProgramPrerequisite.query.all()
        expect(len(result)).to(equal(len(data['program_prerequisites'])))

        # load program potential outcomes
        with open(PROGRAM_POTENTIAL_OUTCOMES, 'r') as f:
            data = json.load(f)

        for item in data['program_potential_outcomes']:
            outcome = ProgramPotentialOutcome(item['name'], item['id'])
            db.session.add(outcome)
        db.session.commit()
        result = ProgramPotentialOutcome.query.all()
        expect(len(result)).to(equal(len(data['program_potential_outcomes'])))

        # load entity types
        with open(ENTITY_TYPES, 'r') as f:
            data = json.load(f)

        for item in data['entity_types']:
            entity = EntityType(item['name'], item['id'])
            db.session.add(entity)
        db.session.commit()
        result = EntityType.query.all()
        expect(len(result)).to(equal(len(data['entity_types'])))

        # load credential types
        with open(CREDENTIAL_TYPES, 'r') as f:
            data = json.load(f)

        for item in data['credential_types']:
            credential_type = CredentialType(
                item['credential_type'], item['audience_level'],
                item['credential_type_id'])
            db.session.add(credential_type)
        db.session.commit()
        result = CredentialType.query.all()
        expect(len(result)).to(equal(len(data['credential_types'])))

        # load providers
        with open(PROVIDERS, 'r') as f:
            data = json.load(f)

        for item in data['providers']:
            provider = Provider(
                item['provider_name'],
                item['entity_type_id'],
                item['provider_alternate_name'],
                item['provider_full_address'],
                item['provider_description'],
                item['provider_contact_email'],
                item['provider_url'],
                item['year_incorporated'],
                item['provider_id']
            )
            db.session.add(provider)
        db.session.commit()
        result = Provider.query.all()
        expect(len(result)).to(equal(len(data['providers'])))

        # load locations
        with open(LOCATIONS, 'r') as f:
            data = json.load(f)

        for item in data['locations']:
            location = GeographicLocation(
                item['location_name'],
                item['provider_id'],
                item['location_description'],
                item['transportation'],
                item['latitude'],
                item['longitude'],
                item['location_full_address'],
                item['location_id']
            )
            db.session.add(location)
        db.session.commit()
        result = GeographicLocation.query.all()
        expect(len(result)).to(equal(len(data['locations'])))

        # load addresses
        with open(ADDRESSES, 'r') as f:
            data = json.load(f)

        for item in data['addresses']:
            address = PhysicalAddress(
                item['location_id'],
                item['address'],
                item['city'],
                item['state'],
                item['postal_code'],
                item['country'],
                item['address_id']
            )
            db.session.add(address)
        db.session.commit()
        result = PhysicalAddress.query.all()
        expect(len(result)).to(equal(len(data['addresses'])))

        # load credentials
        with open(CREDENTIALS, 'r') as f:
            data = json.load(f)

        for item in data['credentials']:
            credential = Credential(
                provider_id=item['provider_id'],
                name=item['credential_name'],
                description=item['credential_description'],
                credential_type_id=item['credential_type_id'],
                credential_status_type=item['credential_status_type'],
                audience=item['audience'],
                language=item['language'],
                ce_ctid=item['ce_ctid'],
                webpage=item['webpage'],
                id=item['credential_id']
            )
            db.session.add(credential)
        db.session.commit()
        result = Credential.query.all()
        expect(len(result)).to(equal(len(data['credentials'])))

        # load programs
        with open(PROGRAMS, 'r') as f:
            data = json.load(f)
            for item in data['programs']:
                program = Program(
                    name=item['program_name'],
                    code=item['program_code'],
                    description=item['program_description'],
                    status=item['program_status'],
                    fees=item['program_fees'],
                    provider_id=item['provider_id'],
                    location_id=item['location_id'],
                    eligibility_criteria=item['eligibility_criteria'],
                    potential_outcome_id=item['potential_outcome_id'],
                    program_url=item['program_url'],
                    credential_earned=item['credential_earned'],
                    contact_phone=item['program_contact_phone'],
                    contact_email=item['program_contact_email'],
                    languages=item['languages'],
                    intake=item['current_intake_capacity'],
                    offering_model=item['program_offering_model'],
                    length_hours=item['program_length_hours'],
                    length_weeks=item['program_length_weeks'],
                    prereq_id=item['prerequisite_id'],
                    program_soc=item['program_soc'],
                    funding=item['funding_sources'],
                    on_etpl=item['on_etpl'],
                    cost_of_books=item['cost_of_books_and_supplies'],
                    id=item['program_id']
                )
                db.session.add(program)
            db.session.commit()
            result = Program.query.all()
            expect(len(result)).to(equal(len(data['programs'])))

        # load participants
        with open(PARTICIPANTS, 'r') as f:
            data = json.load(f)
            for item in data['participants']:
                participant = Participant(
                    program_id=item['program_id'],
                    entry_date=item['entry_date'],
                    exit_date=item['exit_date'],
                    exit_type=item['exit_type'],
                    exit_reason=item['exit_reason'],
                    id=item['participant_id']
                )
                db.session.add(participant)
            db.session.commit()
            result = Participant.query.all()
            expect(len(result)).to(equal(len(data['participants'])))

        # find programs provided by a provider
        provider = Provider.query.first()
        program = Program.query.first()
        credential = Credential.query.first()
