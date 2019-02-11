""" API Version 1.0 Credentials Handler """

from outcomes_api.db import Credential


class CredentialsHandler(object):
    def get_all_credentials(self):
        return {'message': 'credentials api version 1.0'}

    def add_new_credential(self, credential):
        if credential is not None:
            return {'message': 'added a new credential'}, 201
        else:
            return {'message': 'request body cannot be empty'}, 400
