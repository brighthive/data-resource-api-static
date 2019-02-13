""" Programs Resource


"""

import os
from flask import request
from flask_restful import Resource
from outcomes_api.api import VersionedResource
from outcomes_api.api.v1_0 import V1_0_ProgramsHandler
from outcomes_api.auth import login_required


class ProgramsResource(VersionedResource):
    @login_required
    def get(self):
        headers = request.headers
        api_version = self.get_api_version(headers)
        if api_version == 'v1.0':
            request_handler = V1_0_ProgramsHandler()

        return request_handler.get_all_programs(), 200

    @login_required
    def post(self):
        headers = request.headers
        api_version = self.get_api_version(headers)
        if api_version == 'v1.0':
            request_handler = V1_0_ProgramsHandler()

        result, status = request_handler.add_new_program(request.get_json())
        return result, status


class ProgramResource(VersionedResource):
    @login_required
    def get(self, id):
        pass

    @login_required
    def put(self, id):
        pass

    @login_required
    def delete(self, id):
        pass


class ProviderProgramResource(VersionedResource):
    @login_required
    def get(self, id):
        pass


class ProgramCredentialResource(VersionedResource):
    @login_required
    def get(self, id):
        pass
