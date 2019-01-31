from flask import Flask
from flask_restful import Api
from api import ProgramsResource, ParticipantsResource, CredentialsResource

app = Flask(__name__)
api = Api(app)

api.add_resource(ProgramsResource, '/programs')
api.add_resource(ParticipantsResource, '/participants')
api.add_resource(CredentialsResource, '/credentials')

if __name__ == '__main__':
    app.run(debug=True)
