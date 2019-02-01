""" Credentials Database Model. """

from sqlalchemy.dialects.postgresql.json import JSONB
from app.app import db


class Credentials(db.Model):
    id = db.Column(db.Integer, primary_key='true')
    optional_data = db.Column(JSONB)
