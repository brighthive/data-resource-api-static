""" API Version 1.0 Providers Handler """

from data_resource_api.db import Provider


class ProvidersHandler(object):
    def get_all_providers(self):
        results = Provider.query.all()
        providers = {'providers': []}
        for provider in results:
            providers['providers'].append(provider.to_dict())
        return providers

    def add_new_provider(self, provider):
        if provider is not None:
            return {'message': 'added a new provider'}, 201
        else:
            return {'message': 'request body cannot be empty'}, 400
