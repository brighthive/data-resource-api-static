""" Participants Resource


"""

from flask import request
from flask_restful import Resource
from data_resource_api.api import VersionedResource
from data_resource_api.api.v1_0 import V1_0_ParticipantsHandler
from data_resource_api.auth import login_required


class ParticipantsResource(VersionedResource):
    def get_request_handler(self, headers):
        api_version = self.get_api_version(headers)
        if api_version == 'v1.0':
            request_handler = V1_0_ParticipantsHandler()
        else:
            request_handler = V1_0_ParticipantsHandler()
        return request_handler

    @login_required
    def get(self):
        return self.get_request_handler(request.headers).get_all_participants()

    @login_required
    def post(self):
        return self.get_request_handler(request.header).add_new_participant(
            request.get_json())


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
