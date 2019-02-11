""" Providers Resource


"""

import os
from flask import request
from flask_restful import Resource
from outcomes_api.api import VersionedResource
from outcomes_api.api.v1_0 import V1_0_ProvidersHandler
from outcomes_api.auth import login_required


class ProvidersResource(VersionedResource):
    @login_required
    def get(self):
        headers = request.headers
        api_version = self.get_api_version(headers)
        if api_version == 'v1.0':
            request_handler = V1_0_ProvidersHandler()

        return request_handler.get_all_providers(), 200

    @login_required
    def post(self):
        headers = request.headers
        api_version = self.get_api_version(headers)
        if api_version == 'v1.0':
            request_handler = V1_0_ProvidersHandler()

        result, status = request_handler.add_new_provider(request.get_json())
        return result, status
