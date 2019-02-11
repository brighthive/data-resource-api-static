""" API Version 1.0 Providers Handler """

from outcomes_api.db import Program


class ProvidersHandler(object):
    def get_all_providers(self):
        return {'message': 'providers api version 1.0'}

    def add_new_provider(self, provider):
        if provider is not None:
            return {'message': 'added a new provider'}, 201
        else:
            return {'message': 'request body cannot be empty'}, 400
