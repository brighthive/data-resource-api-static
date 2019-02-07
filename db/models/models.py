from sqlalchemy.dialects.postgresql.json import JSONB
from app.app import db


class EntityType(db.Model):
    __tablename__ = 'entity_type'
    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(100), nullable=False)


class Provider(db.Model):
    __tablename__ = 'provider'
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


class GeographicLocation(db.Model):
    __tablename__ = 'geographic_location'

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
        'PhysicalAddress', backref='geographic_location',
        lazy=True, uselist=False, passive_deletes=True)


class PhysicalAddress(db.Model):
    __tablename__ = 'physical_address'

    address_id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey(
        GeographicLocation.location_id, ondelete='CASCADE'))
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(2), nullable=False)


class ProgramCategory(db.Model):
    __tablename__ = 'program_category'
    category_cip = db.Column(db.String(12), primary_key=True)
    category_name = db.Column(db.String(200))
    # TODO finish building out


class Program(db.Model):
    __tablename__ = 'program'

    # required fields
    program_id = db.Column(db.Integer, primary_key=True)
    program_provider_id = db.Column(db.Integer, db.ForeignKey(
        Provider.provider_id, ondelete='CASCADE'))
    program_name = db.Column(db.String(140), nullable=False)
    program_code = db.Column(
        db.String(12), db.ForeignKey(ProgramCategory.category_cip))
    program_description = db.Column(db.String(4096), nullable=False)
    program_status = db.Column(db.String(256), nullable=False)
    program_fees = db.Column(db.Float, nullable=False)

    # geographic_areas
    # program_address
    # eligibility_criteria
    # credential_earned
    # program_potential_outcome
    # program_url

    # fields that can be validated
    optional_fields = db.Column(JSONB)

    # fields provided by the user that have no validation criteria
    user_provided_fields = db.Column(JSONB)


class Credential(db.Model):
    __tablename__ = 'credential'
    credential_id = db.Column(db.Integer, primary_key=True)
    optional_fields = db.Column(JSONB)
    user_provided_fields = db.Column(JSONB)


class Participant(db.Model):
    __tablename__ = 'participant'
    participant_id = db.Column(db.Integer, primary_key=True)
    optional_fields = db.Column(JSONB)
    user_provided_fields = db.Column(JSONB)
