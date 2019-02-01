""" Participants Database Model

This class models the Participants as described in the TPOT Datasheet for
Participants.

"""

from sqlalchemy.dialects.postgresql.json import JSONB
from app.app import db


class Participant(db.Model):
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    program_provider = db.Column(db.String)
    program_name = db.Column(db.String)
    program_code = db.Column(db.String)
    program_description = db.Column(db.String)
    program_status = db.Column(db.String)
    program_fees = db.Column(db.String)
    geographic_areas = db.Column(db.String)
    program_address = db.Column(db.String)
    eligibility_criteria = db.Column(db.String)
    credential_earned = db.Column(db.String)
    program_potential_outcome = db.Column(db.String)
    program_url = db.Column(db.String)
    optional_fields = db.Column(JSONB)
