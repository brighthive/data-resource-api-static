from sqlalchemy.dialects.postgresql.json import JSONB
from app.app import db


class Provider(db.Model):
    __tablename__ = 'providers'
    provider_id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String(100), nullable=False)
    provider_alternate_name = db.Column(db.String(100), nullable=False)
    # entity type id
    optional_fields = db.Column(JSONB)
    user_provided_fields = db.Column(JSONB)


class ProgramCategory(db.Model):
    __tablename__ = 'program_category'
    category_cip = db.Column(db.String(12), primary_key=True)
    category_name = db.Column(db.String(200))
    # TODO finish building out


class Program(db.Model):
    __tablename__ = 'programs'

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
    __tablename__ = 'credentials'
    credential_id = db.Column(db.Integer, primary_key=True)
    optional_fields = db.Column(JSONB)
    user_provided_fields = db.Column(JSONB)


class Participant(db.Model):
    __tablename__ = 'participants'
    participant_id = db.Column(db.Integer, primary_key=True)
    optional_fields = db.Column(JSONB)
    user_provided_fields = db.Column(JSONB)
