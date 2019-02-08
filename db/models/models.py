from sqlalchemy.dialects.postgresql.json import JSONB
from app.app import db


class EntityType(db.Model):
    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(100), nullable=False)

    providers = db.relationship(
        'Provider', backref='entity_type', lazy=True, passive_deletes=True)


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


class ProgramPotentialOutcome(db.Model):
    potential_outcome_id = db.Column(db.Integer, primary_key=True)
    potential_outcome_name = db.Column(db.String(100), nullable=False)

    programs = db.relationship(
        'Program', backref='program_potential_outcome', lazy=True,
        passive_deletes=True)


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


class CredentialType(db.Model):
    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(1024), nullable=False)
    audience_level = db.Column(db.String(256), nullable=False)


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


class ProgramPrerequisite(db.Model):
    prerequisite_id = db.Column(db.Integer, primary_key=True)
    prerequisite_name = db.Column(db.String(100), nullable=False)


class Program(db.Model):
    __tablename__ = 'programs'

    # required fields
    program_id = db.Column(db.Integer, primary_key=True)
    program_name = db.Column(db.String(140), nullable=False)
    program_code = None
    program_description = db.Column(db.String(4096), nullable=False)
    program_status = db.Column(db.String(256), nullable=False)
    program_fees = db.Column(db.Float, nullable=False)
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

    def __repr__(self):
        return '<Program: {}, {}, {}>'.format(self.program_id,
                                              self.program_code,
                                              self.program_name)


class Participant(db.Model):
    __tablename__ = 'participants'

    # required fields
    participant_id = db.Column(db.Integer, nullable=False, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey(
        Program.program_id, ondelete='CASCADE'), nullable=False,
        primary_key=True)
    entry_date = db.Column(db.Date, nullable=False)
    exit_date = db.Column(db.Date, nullable=False)
    exit_type = db.Column(db.Date, nullable=False)
    exit_reason = db.Column(db.String(256), nullable=False)

    # extra data
    optional_fields = db.Column(JSONB)
    user_provided_fields = db.Column(JSONB)
