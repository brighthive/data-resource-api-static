""" Simple API Application Healthcheck Resource. """

from flask import request
from data_resource_api.api import VersionedResource
from data_resource_api.api.v1_0_0 import V1_0_0_HealthCheckHandler


class HealthCheckResource(VersionedResource):
    def get_request_handler(self, headers):
        api_version = self.get_api_version(headers)
        if api_version == '1.0.0':
            request_handler = V1_0_0_HealthCheckHandler()
        else:
            request_handler = V1_0_0_HealthCheckHandler()
        return request_handler

    def get(self):
        return self.get_request_handler(request.headers).get_health()
