from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from data_resource_api.config import ConfigurationFactory
import os

app = Flask(__name__)
app.config.from_object(ConfigurationFactory.from_env())
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

if db:
    from data_resource_api.api import ProgramsResource, ParticipantsResource,\
        CredentialsResource, ProvidersResource, ProgramResource,\
        ParticipantResource, CredentialResource, ProviderResource,\
        ProviderProgramResource, ProgramCredentialResource,\
        HealthCheckResource, CredentialProgramResource, PathwaysProgramsResource,\
        PathwaysProgramResource

    # health check
    api.add_resource(HealthCheckResource, '/health', endpoint='healthcheck')

    # programs
    api.add_resource(ProgramsResource, '/programs', endpoint='programs')
    api.add_resource(ProgramResource, '/programs/<int:id>',
                     endpoint='program')

    # pathways programs
    api.add_resource(PathwaysProgramsResource, '/pathways_programs', endpoint='pathways_programs')
    api.add_resource(PathwaysProgramResource, '/pathways_programs/<int:id>',
                     endpoint='pathways_program')

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

    # credential programs
    api.add_resource(CredentialProgramResource,
                     '/credentials/<int:id>/programs',
                     endpoint='credential_programs')

    # locations
    # /locations
    # /locations/{id}
    # /locations/{id}/address
