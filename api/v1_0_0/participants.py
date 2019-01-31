""" Participants Resource


"""

from flask_restful import Resource


class ParticipantsResource(Resource):
    def get(self):
        return {'message': 'participants resource'}, 200
