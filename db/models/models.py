from sqlalchemy.dialects.postgresql.json import JSONB
from app.app import db


class Program(db.Model):
    __tablename__ = 'programs'

    # required fields
    program_id = db.Column(db.Integer, primary_key=True)
    program_name = db.Column(db.String(140), nullable=False)
    program_code = None
    program_description = db.Column(db.String(4096), nullable=False)
    program_status = db.Column(db.String(256), nullable=False)
    program_fees = db.Column(db.Float, nullable=False)
    # geographic_areas
    # program_address
    eligibility_criteria = db.Column(db.String(256), nullable=False)
    # credential_earned
    # program_potential_outcome
    program_url = db.Column(db.String(256), nullable=False)

    # recommended fields
    program_contact_phone = db.Column(db.String(64), nullable=True)
    program_contact_email = db.Column(db.String(256), nullable=True)
    languages = db.Column(db.String(256), nullable=True)
    current_intake_capacity = db.Column(db.Integer, nullable=True)
    # program_offering_model = None
    program_length_hours = db.Column(db.Float, nullable=True)
    program_length_weeks = db.Column(db.Float, nullable=True)
    # prerequisites = None
    # program_soc = None
    funding_sources = db.Column(db.String(2048), nullable=True)
    on_etpl = db.Column(db.Integer, nullable=True)
    # cost_of_books_and_supplies = None

    # extra data
    optional_fields = db.Column(JSONB)
    user_provided_fields = db.Column(JSONB)

    def __repr__(self):
        return '<Program: {}, {}, {}>'.format(self.program_id,
                                              self.program_code,
                                              self.program_name)


class Provider(db.Model):
    __tablename__ = 'providers'

    # required fields
    provider_id = db.Column(db.Integer, primary_key=True)

    # recommended fields

    # extra data
    optional_fields = db.Column(JSONB)
    user_provided_fields = db.Column(JSONB)


class Credential(db.Model):
    __tablename__ = 'credentials'

    # required fields
    credential_id = db.Column(db.Integer, primary_key=True)
    # program_provider = None
    # program_code = None
    credential_name = db.Column(db.String(1024), nullable=False)
    credential_description = db.Column(db.String(4098), nullable=False)
    # credential_type = None
    credential_status_type = db.Column(db.String(256), nullable=False)
    audience = db.Column(db.String(256), nullable=False)
    # audience_level = None
    language = db.Column(db.String(256), nullable=False)

    # recommended fields
    ctid = db.Column(db.String(50), nullable=True)
    webpage = db.Column(db.String(1024), nullable=True)

    # extra data
    optional_fields = db.Column(JSONB)
    user_provided_fields = db.Column(JSONB)


class Participant(db.Model):
    __tablename__ = 'participants'

    # required fields
    participant_id = db.Column(db.Integer, primary_key=True)
    # program_code = db.Column()
    # program_provider = db.Column()
    # entry_date = db.Column()
    # exit_date = db.Column()
    # exit_type = db.Column()
    # exit_reason = db.Column()

    # recommended fields
    # program_name = db.Column()
    # service_location = db.Column()
    # funding_sources = db.Column()
    # wioa_participant = db.Column()

    # extra data
    optional_fields = db.Column(JSONB)
    user_provided_fields = db.Column(JSONB)
