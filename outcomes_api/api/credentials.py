""" Credentials Resource


"""

from flask import request
from flask_restful import Resource
from outcomes_api.api import VersionedResource
from outcomes_api.api.v1_0 import V1_0_CredentialsHandler


class CredentialsResource(VersionedResource):
    def get(self):
        headers = request.headers
        api_version = self.get_api_version(headers)
        if api_version == 'v1.0':
            request_handler = V1_0_CredentialsHandler()

        return request_handler.get_all_credentials(), 200

    def post(self):
        headers = request.headers
        api_version = self.get_api_version(headers)
        if api_version == 'v1.0':
            request_handler = V1_0_CredentialsHandler()

        result, status = request_handler.add_new_credential(request.get_json())
        return result, status
