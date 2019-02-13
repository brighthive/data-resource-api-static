""" API Version 1.0 Credentials Handler """

import json
from data_resource_api.db import Credential


class CredentialsHandler(object):
    def get_all_credentials(self):
        all_results = Credential.query.all()
        credentials = {'credentials': []}
        for result in all_results:
            credentials['credentials'].append(result.to_dict())
        return credentials

    def add_new_credential(self, credential):
        if credential is not None:
            return {'message': 'added a new credential'}, 201
        else:
            return {'message': 'request body cannot be empty'}, 400
