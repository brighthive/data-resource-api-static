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
        CredentialsResource, ProvidersResource, ProgramResource,\
        ParticipantResource, CredentialResource, ProviderResource,\
        ProviderProgramResource, ProgramCredentialResource

    # programs
    api.add_resource(ProgramsResource, '/programs', endpoint='programs')
    api.add_resource(ProgramResource, '/programs/<int:id>',
                     endpoint='program')

    # participants
    api.add_resource(ParticipantsResource, '/participants',
                     endpoint='participants')
    api.add_resource(ParticipantResource, '/participants/<int:id>',
                     endpoint='participant')

    # credentials
    api.add_resource(CredentialsResource, '/credentials',
                     endpoint='credentials')
    api.add_resource(CredentialResource, '/credentials/<int:id>',
                     endpoint='credential')

    # providers
    api.add_resource(ProvidersResource, '/providers', endpoint='providers')
    api.add_resource(ProviderResource, '/providers/<int:id>',
                     endpoint='provider')

    # provider programs
    api.add_resource(ProviderProgramResource, '/providers/<int:id>/programs',
                     endpoint='provider_programs')

    # program credentials
    api.add_resource(ProgramCredentialResource,
                     '/programs/<int:id>/credentials',
                     endpoint='program_credentials')

    # locations
    # /locations
    # /locations/{id}
    # /locations/{id}/address
