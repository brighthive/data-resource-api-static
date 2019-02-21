""" Provision A Database with Test Data """

import os
import sys
import json
from flask_migrate import upgrade

relative_path = os.path.dirname(os.path.relpath(__file__))
absolute_path = os.path.dirname(os.path.abspath(__file__))
root_path = absolute_path.split(relative_path)[0]
sample_data_root = os.path.join(root_path, 'tests', 'fixtures', 'sample')
verbose = True

# add the path of the application to the system path
if root_path:
    sys.path.append(root_path)
    from data_resource_api import *


def usage():
    print('You are doing it incorrectly')


def insert_sample_data():
    # location of sample datasets
    PROGRAM_PREREQUISITES = os.path.join(
        sample_data_root, 'program_prerequisites.json')
    PROGRAM_POTENTIAL_OUTCOMES = os.path.join(
        sample_data_root, 'program_potential_outcomes.json')
    ENTITY_TYPES = os.path.join(sample_data_root, 'entity_types.json')
    CREDENTIAL_TYPES = os.path.join(
        sample_data_root, 'credential_types.json')
    PROVIDERS = os.path.join(sample_data_root, 'providers.json')
    LOCATIONS = os.path.join(sample_data_root, 'locations.json')
    ADDRESSES = os.path.join(sample_data_root, 'addresses.json')
    CREDENTIALS = os.path.join(sample_data_root, 'credentials.json')
    PROGRAMS = os.path.join(sample_data_root, 'programs.json')
    PARTICIPANTS = os.path.join(sample_data_root, 'participants.json')

    # manually load datasets
    if verbose:
        print('Creating Sample Datasets...')
    # load program prerequisites:
    with open(PROGRAM_PREREQUISITES, 'r') as f:
        data = json.load(f)

    for item in data['program_prerequisites']:
        prereq = ProgramPrerequisite(item['name'], item['id'])
        db.session.add(prereq)
    db.session.commit()

    # load program potential outcomes
    with open(PROGRAM_POTENTIAL_OUTCOMES, 'r') as f:
        data = json.load(f)

    for item in data['program_potential_outcomes']:
        outcome = ProgramPotentialOutcome(item['name'], item['id'])
        db.session.add(outcome)
    db.session.commit()

    # load entity types
    with open(ENTITY_TYPES, 'r') as f:
        data = json.load(f)

    for item in data['entity_types']:
        entity = EntityType(item['name'], item['id'])
        db.session.add(entity)
    db.session.commit()

    # load credential types
    with open(CREDENTIAL_TYPES, 'r') as f:
        data = json.load(f)

    for item in data['credential_types']:
        credential_type = CredentialType(
            item['credential_type'], item['audience_level'],
            item['credential_type_id'])
        db.session.add(credential_type)
    db.session.commit()

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
                # id=item['program_id']
                id=None
            )
            db.session.add(program)
        db.session.commit()

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


def provision_database(load_sample_data=False):
    app.config.from_object(ConfigurationFactory.from_env())
    with app.app_context():
        migrations_dir = os.path.join(
            root_path, 'data_resource_api', 'db', 'migrations')
        upgrade(directory=migrations_dir)
        if load_sample_data:
            insert_sample_data()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        provision_database()
    elif len(sys.argv) == 2:
        if str(sys.argv[1]).lower() == '--load-sample-data':
            provision_database(True)
        else:
            print('Unrecognized flag: {}'.format(sys.argv[1]))
            usage()
            sys.exit(1)
    else:
        usage()
        sys.exit(1)
