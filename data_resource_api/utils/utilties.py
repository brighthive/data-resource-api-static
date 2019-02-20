import os
import sys
import docker
import json
from time import sleep
from flask_migrate import upgrade
from data_resource_api import app, db, ConfigurationFactory,\
    ProgramPrerequisite, ProgramPotentialOutcome, EntityType,\
    CredentialType, Provider, GeographicLocation, PhysicalAddress,\
    Credential, Program, Participant


class DatabaseConfigurationUtility(object):
    def __init__(self, configuration='DEVELOPMENT', verbose=False):
        relative_path = os.path.dirname(os.path.relpath(__file__))
        absolute_path = os.path.dirname(os.path.abspath(__file__))
        self.root_path = absolute_path.split(relative_path)[0]
        self.docker_client = docker.from_env()
        self.config = ConfigurationFactory.get_config(
            str(configuration).upper())
        self.container = None
        self.db_environment = [
            'POSTGRES_USER={}'.format(self.config.POSTGRES_USER),
            'POSTGRES_PASSWORD={}'.format(self.config.POSTGRES_PASSWORD),
            'POSTGRES_DB={}'.format(self.config.POSTGRES_DATABASE)
        ]
        self.db_ports = {'5432/tcp': self.config.POSTGRES_PORT}
        self.sample_data_root = os.path.join(
            self.root_path, 'tests', 'fixtures', 'sample')
        self.verbose = verbose

    def setup_database(self):
        # pull the postgresql image from repo if it doesn't exist
        try:
            self.docker_client.images.pull(self.config.get_postgresql_image())
        except Exception:
            if self.verbose:
                print('Failed to pull image {} from repository.'.format(
                    self.config.get_postgresql_image()))
            else:
                pass

        # launch the container
        self.container = self.docker_client.containers.run(
            self.config.get_postgresql_image(),
            detach=True,
            auto_remove=True,
            name=self.config.CONTAINER_NAME,
            environment=self.db_environment,
            ports=self.db_ports)

    def add_datasets(self):
        # location of sample datasets
        PROGRAM_PREREQUISITES = os.path.join(
            self.sample_data_root, 'program_prerequisites.json')
        PROGRAM_POTENTIAL_OUTCOMES = os.path.join(
            self.sample_data_root, 'program_potential_outcomes.json')
        ENTITY_TYPES = os.path.join(self.sample_data_root, 'entity_types.json')
        CREDENTIAL_TYPES = os.path.join(
            self.sample_data_root, 'credential_types.json')
        PROVIDERS = os.path.join(self.sample_data_root, 'providers.json')
        LOCATIONS = os.path.join(self.sample_data_root, 'locations.json')
        ADDRESSES = os.path.join(self.sample_data_root, 'addresses.json')
        CREDENTIALS = os.path.join(self.sample_data_root, 'credentials.json')
        PROGRAMS = os.path.join(self.sample_data_root, 'programs.json')
        PARTICIPANTS = os.path.join(self.sample_data_root, 'participants.json')

        # manually load datasets
        if self.verbose:
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
                    id=item['program_id']
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

    def apply_migrations(self):
        app.config.from_object(self.config)
        with app.app_context():
            relative_path = os.path.dirname(os.path.relpath(__file__))
            absolute_path = os.path.dirname(os.path.abspath(__file__))
            self.root_path = absolute_path.split(relative_path)[0]
            migrations_dir = os.path.join(
                self.root_path, 'data_resource_api', 'db', 'migrations')
            upgrade(directory=migrations_dir)

    def start_database(self, populate_sample_data=False):
        tables_loaded = False
        retries = 0
        max_retries = 10
        try:
            if self.verbose:
                print('Launching Database Container {}...'.format(
                    self.config.CONTAINER_NAME))
            self.setup_database()
        except Exception:
            if self.verbose:
                print('Database Container {} is already running.'.format(
                    self.config.CONTAINER_NAME))
                sys.exit(1)
            else:
                pass
        while not tables_loaded and retries < max_retries:
            try:
                if self.verbose:
                    print('Applying Migrations, Attempt {} of {}...'.format(
                        retries + 1, max_retries))
                self.apply_migrations()
                tables_loaded = True
            except Exception:
                tables_loaded = False
                retries += 1
                sleep(1)

        if tables_loaded and populate_sample_data:
            try:
                if self.verbose:
                    print('Populating Database With Sample Datasets...')
                self.add_datasets()
            except Exception:
                if self.verbose:
                    print('Failed to add sample datasets.')
                else:
                    pass

    def stop_database(self):
        if self.verbose:
            print('Stopping Database Container {}...'.format(
                self.config.CONTAINER_NAME))

        try:
            if self.container is None:
                self.container = self.docker_client.containers.get(
                    self.config.CONTAINER_NAME)
            self.container.stop()
        except Exception:
            if self.verbose:
                print('Database Container {} is not running.'.format(
                    self.config.CONTAINER_NAME))
            else:
                pass
