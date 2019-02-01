from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

if db:
    from api import ProgramsResource, ParticipantsResource, CredentialsResource
    api.add_resource(ProgramsResource, '/programs')
    api.add_resource(ParticipantsResource, '/participants')
    api.add_resource(CredentialsResource, '/credentials')
