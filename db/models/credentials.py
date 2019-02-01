""" Credentials Database Model.

This class models the Credentials as described in the TPOT Datasheet for
Credentials.

"""

from sqlalchemy.dialects.postgresql.json import JSONB
from app.app import db


class Credential(db.Model):
    __tablename__ = 'credentials'
    id = db.Column(db.Integer, primary_key='true')
    optional_data = db.Column(JSONB)
