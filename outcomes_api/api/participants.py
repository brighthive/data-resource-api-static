""" Participants Resource


"""

from flask import request
from flask_restful import Resource
from outcomes_api.api import VersionedResource
from outcomes_api.api.v1_0 import V1_0_ParticipantsHandler
from outcomes_api.auth import login_required


class ParticipantsResource(VersionedResource):
    @login_required
    def get(self):
        headers = request.headers
        api_version = self.get_api_version(headers)
        if api_version == 'v1.0':
            request_handler = V1_0_ParticipantsHandler()

        return request_handler.get_all_participants(), 200

    @login_required
    def post(self):
        headers = request.headers
        api_version = self.get_api_version(headers)
        if api_version == 'v1.0':
            request_handler = V1_0_ParticipantsHandler()

        result, status = request_handler.add_new_participant(
            request.get_json())
        return result, status


class ParticipantResource(VersionedResource):
    @login_required
    def get(self, id):
        pass

    @login_required
    def put(self, id):
        pass

    @login_required
    def delete(self, id):
        pass
