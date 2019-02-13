""" Versioned Resource

This class extends the Flask-Restful Resource class with the ability to look
up the API version number in a request header.

"""

from flask_restful import Resource
from outcomes_api.config import Config


class VersionedResource(Resource):
    def __init__(self):
        Resource.__init__(self)

    def get_api_version(self, headers):
        try:
            api_version = headers['X-Api-Version']
        except Exception:
            api_version = Config.get_api_version()
        return api_version

    def get_request_handler(self, headers):
        """ Override this method to provide the request handler. """
        pass
