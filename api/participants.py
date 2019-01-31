""" Participants Resource


"""

from flask_restful import Resource
from api.v1_0 import V1_0_ParticipantsHandler


class ParticipantsResource(Resource):
    def get(self):
        request_handler = V1_0_ParticipantsHandler()
        return request_handler.get_all_participants(), 200
