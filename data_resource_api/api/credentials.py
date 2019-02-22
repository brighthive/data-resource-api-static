""" Credentials Resource


"""

from flask import request
from flask_restful import Resource
from data_resource_api.api import VersionedResource
from data_resource_api.api.v1_0_0 import V1_0_0_CredentialsHandler
from data_resource_api.auth import login_required


class CredentialsResource(VersionedResource):
    def get_request_handler(self, headers):
        api_version = self.get_api_version(headers)
        if api_version == '1.0.0':
            request_handler = V1_0_0_CredentialsHandler()
        else:
            request_handler = V1_0_0_CredentialsHandler()
        return request_handler

    @login_required
    def get(self):
        return self.get_request_handler(request.headers).get_all_credentials()

    @login_required
    def post(self):
        return self.get_request_handler(request.headers).add_new_credential(
            request.get_json())


class CredentialResource(CredentialsResource):
    @login_required
    def get(self, id):
        return self.get_request_handler(request.headers).get_credential_by_id(
            id)

    @login_required
    def put(self, id):
        return self.get_request_handler(request.headers).update_credential(
            request.get_json(), id)

    @login_required
    def delete(self, id):
        return self.get_request_handler(
            request.headers).delete_credential_by_id(id)
