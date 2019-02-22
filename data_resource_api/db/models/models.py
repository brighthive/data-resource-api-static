from datetime import datetime
from sqlalchemy.dialects.postgresql.json import JSONB
from data_resource_api.app.app import db


class Token(db.Model):
    token = db.Column(db.String(100), primary_key=True)
    date_created = db.Column(
        db.DateTime, server_default=db.func.now(), nullable=False)

    def __init__(self, token=None):
        self.token = token


class EntityType(db.Model):
    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(100), nullable=False)

    providers = db.relationship(
        'Provider', backref='entity_type', lazy=True, passive_deletes=True)

    def __init__(self, name, id=None):
        self.type_id = id
        self.type_name = name


class Provider(db.Model):
    __tablename__ = 'providers'

    # required fields
    provider_id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String(100), nullable=False)
    provider_alternate_name = db.Column(db.String(100), nullable=True)
    entity_type_id = db.Column(db.Integer, db.ForeignKey(
        EntityType.type_id, ondelete='CASCADE'))
    provider_full_address = db.Column(db.String(2048), nullable=True)
    provider_description = db.Column(db.String(1024), nullable=True)
    provider_contact_email = db.Column(db.String(256), nullable=True)
    provider_url = db.Column(db.String(1024), nullable=True)
    year_incorporated = db.Column(db.Integer, nullable=True)
    programs = db.relationship(
        'Program', backref='provider', lazy=True, passive_deletes=True)
    locations = db.relationship(
        'GeographicLocation', backref='provider', lazy=True,
        passive_deletes=True)

    # extra data
    optional_fields = db.Column(JSONB)
    user_provided_fields = db.Column(JSONB)

    def __init__(self, name, entity_type_id, alternate_name=None,
                 full_address=None, description=None, contact_email=None,
                 url=None, incorporated=None, id=None):
        self.provider_name = name
        self.entity_type_id = entity_type_id
        self.provider_alternate_name = alternate_name
        self.provider_full_address = full_address
        self.provider_description = description
        self.provider_contact_email = contact_email
        self.provider_url = url
        self.year_incorporated = incorporated
        self.provider_id = id

    def to_dict(self):
        return {
            'provider_id': self.provider_id,
            'entity_type_id': self.entity_type_id,
            'provider_name': self.provider_name,
            'provider_alternate_name': self.provider_alternate_name,
            'provider_full_address': self.provider_full_address,
            'provider_description': self.provider_description,
            'provider_contact_email': self.provider_contact_email,
            'provider_url': self.provider_url,
            'year_incorporated': self.year_incorporated
        }


class ProgramPotentialOutcome(db.Model):
    potential_outcome_id = db.Column(db.Integer, primary_key=True)
    potential_outcome_name = db.Column(db.String(100), nullable=False)

    programs = db.relationship(
        'Program', backref='program_potential_outcome', lazy=True,
        passive_deletes=True)

    def __init__(self, outcome_name, outcome_id=None):
        self.potential_outcome_id = outcome_id
        self.potential_outcome_name = outcome_name


class GeographicLocation(db.Model):
    __tablename__ = 'geographic_locations'
    location_id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(100), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey(
        Provider.provider_id, ondelete='CASCADE'))
    location_description = db.Column(db.String(256), nullable=True)
    transportation = db.Column(db.String(256), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    location_full_address = db.Column(db.String(650), nullable=True)
    location_address = db.relationship(
        'PhysicalAddress', backref='geographic_location', lazy=True,
        uselist=False, passive_deletes=True)

    def __init__(self, name, provider_id, description=None,
                 transportation=None, latitude=None, longitude=None,
                 full_address=None, id=None):
        self.location_name = name
        self.provider_id = provider_id
        self.location_description = description
        self.transportation = transportation
        self.latitude = latitude
        self.longitude = longitude
        self.location_full_address = full_address,
        self.location_id = id


class PhysicalAddress(db.Model):
    __tablename__ = 'physical_addresses'

    address_id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey(
        GeographicLocation.location_id, ondelete='CASCADE'))
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(2), nullable=False)

    def __init__(self, location_id, address, city, state,
                 postal_code, country, address_id=None):
        self.location_id = location_id
        self.address = address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
        self.address_id = address_id


class CredentialType(db.Model):
    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(1024), nullable=False)
    audience_level = db.Column(db.String(256), nullable=False)

    def __init__(self, name, level, id=None):
        self.type_id = id
        self.type_name = name
        self.audience_level = level


class Credential(db.Model):
    __tablename__ = 'credentials'

    # required fields
    credential_id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey(
        Provider.provider_id, ondelete='CASCADE'), nullable=False)
    programs = db.relationship(
        'Program', backref='credential', lazy=True, passive_deletes=True)
    credential_name = db.Column(db.String(1024), nullable=False)
    credential_description = db.Column(db.String(4098), nullable=False)
    credential_type_id = db.Column(db.Integer, db.ForeignKey(
        CredentialType.type_id, ondelete='SET NULL'), nullable=False)
    credential_status_type = db.Column(db.String(256), nullable=False)
    audience = db.Column(db.String(256), nullable=False)
    language = db.Column(db.String(256), nullable=False)

    # recommended fields
    ce_ctid = db.Column(db.String(50), nullable=True)
    webpage = db.Column(db.String(1024), nullable=True)

    # extra data
    optional_fields = db.Column(JSONB)
    user_provided_fields = db.Column(JSONB)

    def __init__(self, provider_id, name, description, credential_type_id,
                 credential_status_type, audience, language, ce_ctid=None,
                 webpage=None, id=None):
        self.provider_id = provider_id
        self.credential_name = name
        self.credential_description = description
        self.credential_type_id = credential_type_id
        self.credential_status_type = credential_status_type
        self.audience = audience
        self.language = language
        self.ce_ctid = ce_ctid
        self.webpage = webpage
        self.credential_id = id

    def to_dict(self):
        return {
            'credential_id': self.credential_id,
            'provider_id': self.provider_id,
            'credential_name': self.credential_name,
            'credential_description': self.credential_description,
            'credential_type_id': self.credential_type_id,
            'credential_status_type': self.credential_status_type,
            'audience': self.audience,
            'language': self.language,
            'ctid': self.ce_ctid,
            'webpage': self.webpage
        }


class ProgramPrerequisite(db.Model):
    prerequisite_id = db.Column(db.Integer, primary_key=True)
    prerequisite_name = db.Column(db.String(100), nullable=False)

    def __init__(self, name, id=None):
        self.prerequisite_id = id
        self.prerequisite_name = name


class Program(db.Model):
    __tablename__ = 'programs'

    # required fields
    program_id = db.Column(db.Integer, primary_key=True)
    program_name = db.Column(db.String(140), nullable=False)
    program_code = db.Column(db.String(32), nullable=False)
    program_description = db.Column(db.String(4096), nullable=False)
    program_status = db.Column(db.String(256), nullable=False)
    program_fees = db.Column(db.Float, nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey(
        Provider.provider_id, ondelete='CASCADE'))
    location_id = db.Column(db.Integer, db.ForeignKey(
        GeographicLocation.location_id, ondelete='CASCADE'), nullable=True)
    eligibility_criteria = db.Column(db.String(256), nullable=False)
    credential_earned = db.Column(db.Integer, db.ForeignKey(
        Credential.credential_id, ondelete='CASCADE'), nullable=True)
    potential_outcome_id = db.Column(db.Integer, db.ForeignKey(
        ProgramPotentialOutcome.potential_outcome_id, ondelete='CASCADE'))
    program_url = db.Column(db.String(256), nullable=False)

    # recommended fields
    program_contact_phone = db.Column(db.String(64), nullable=True)
    program_contact_email = db.Column(db.String(256), nullable=True)
    languages = db.Column(db.String(256), nullable=True)
    current_intake_capacity = db.Column(db.Integer, nullable=True)
    program_offering_model = db.Column(db.Integer, nullable=True)
    program_length_hours = db.Column(db.Float, nullable=True)
    program_length_weeks = db.Column(db.Float, nullable=True)
    prerequisite_id = db.Column(db.Integer, db.ForeignKey(
        ProgramPrerequisite.prerequisite_id, ondelete='CASCADE'),
        nullable=True)
    program_soc = db.Column(db.Integer, nullable=True)
    funding_sources = db.Column(db.String(2048), nullable=True)
    on_etpl = db.Column(db.Integer, nullable=True)
    cost_of_books_and_supplies = db.Column(db.Float, nullable=True)

    # extra data
    optional_fields = db.Column(JSONB)
    user_provided_fields = db.Column(JSONB)

    def __init__(self, name, code, description, status, fees, provider_id,
                 location_id, eligibility_criteria, potential_outcome_id,
                 program_url,  credential_earned, contact_phone=None,
                 contact_email=None, languages=None, intake=None,
                 offering_model=None, length_hours=None, length_weeks=None,
                 prereq_id=None, program_soc=None, funding=None, on_etpl=None,
                 cost_of_books=None, id=None):
        self.program_name = name
        self.program_code = code
        self.program_description = description
        self.program_status = status
        self.program_fees = fees
        self.provider_id = provider_id
        self.location_id = location_id
        self.eligibility_criteria = eligibility_criteria
        self.potential_outcome_id = potential_outcome_id
        self.program_url = program_url
        self.credential_earned = credential_earned
        self.program_contact_phone = contact_phone
        self.program_contact_email = contact_email
        self.languages = languages
        self.current_intake_capacity = intake
        self.program_offering_model = offering_model
        self.program_length_hours = length_hours
        self.program_length_weeks = length_weeks
        self.prerequisite_id = prereq_id
        self.program_soc = program_soc
        self.funding_sources = funding
        self.on_etpl = on_etpl
        self.cost_of_books_and_supplies = cost_of_books
        self.program_id = id

    def __repr__(self):
        return '<Program: {}, {}, {}>'.format(self.program_id,
                                              self.program_code,
                                              self.program_name)

    def to_dict(self):
        return {
            'program_id': self.program_id,
            'program_name': self.program_name,
            'program_code': self.program_code,
            'program_description': self.program_description,
            'program_status': self.program_status,
            'program_fees': self.program_fees,
            'provider_id': self.provider_id,
            'location_id': self.location_id,
            'eligibility_criteria': self.eligibility_criteria,
            'credential_earned_id': self.credential_earned,
            'potential_outcome_id': self.potential_outcome_id,
            'program_url': self.program_url,
            'program_contact_phone': self.program_contact_phone,
            'program_contact_email': self.program_contact_email,
            'languages': self.languages,
            'current_intake_capacity': self.current_intake_capacity,
            'program_length_hours': self.program_length_hours,
            'program_length_weeks': self.program_length_weeks,
            'prerequisite_id': self.prerequisite_id,
            'program_soc': self.program_soc,
            'funding_sources': self.funding_sources,
            'on_etpl': self.on_etpl,
            'cost_of_books_and_supplies': self.cost_of_books_and_supplies
        }


class Participant(db.Model):
    __tablename__ = 'participants'

    # required fields
    participant_id = db.Column(db.Integer, nullable=False, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey(
        Program.program_id, ondelete='CASCADE'), nullable=False,
        primary_key=True)
    entry_date = db.Column(db.Date, nullable=False)
    exit_date = db.Column(db.Date, nullable=False)
    exit_type = db.Column(db.String(32), nullable=False)
    exit_reason = db.Column(db.String(256), nullable=False)

    # extra data
    optional_fields = db.Column(JSONB)
    user_provided_fields = db.Column(JSONB)

    def __init__(self, program_id, entry_date, exit_date, exit_type,
                 exit_reason, id=None):
        self.program_id = program_id
        self.entry_date = entry_date
        self.exit_date = exit_date
        self.exit_type = exit_type
        self.exit_reason = exit_reason
        self.participant_id = id

    def to_dict(self):
        return {
            'participant_id': self.participant_id,
            'program_id': self.program_id,
            'entry_date': self.entry_date.strftime('%Y/%m/%d'),
            'exit_date': self.exit_date.strftime('%Y/%m/%d'),
            'exit_type': self.exit_type
        }
