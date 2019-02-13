""" Providers Resource


"""

import os
from flask import request
from flask_restful import Resource
from outcomes_api.api import VersionedResource
from outcomes_api.api.v1_0 import V1_0_ProvidersHandler
from outcomes_api.auth import login_required


class ProvidersResource(VersionedResource):
    def get_request_handler(self, headers):
        api_version = self.get_api_version(headers)
        if api_version == 'v1.0':
            request_handler = V1_0_ProvidersHandler()
        else:
            request_handler = V1_0_ProvidersHandler()
        return request_handler

    @login_required
    def get(self):
        return self.get_request_handler(request.headers).get_all_providers()

    @login_required
    def post(self):
        return self.get_request_handler(request.headers).add_new_provider(
            request.get_json())


class ProviderResource(VersionedResource):
    @login_required
    def get(self, id):
        pass

    @login_required
    def put(self, id):
        pass

    @login_required
    def delete(self, id):
        pass
