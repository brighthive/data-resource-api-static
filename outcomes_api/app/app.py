from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from outcomes_api.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

if db:
    from outcomes_api.api import ProgramsResource, ParticipantsResource,\
        CredentialsResource, ProvidersResource
    api.add_resource(ProgramsResource, '/programs')
    api.add_resource(ParticipantsResource, '/participants')
    api.add_resource(CredentialsResource, '/credentials')
    api.add_resource(ProvidersResource, '/providers')
