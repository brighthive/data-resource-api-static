""" Credentials Resource


"""

from flask_restful import Resource
from api.v1_0 import V1_0_CredentialsHandler


class CredentialsResource(Resource):
    def get(self):
        request_handler = V1_0_CredentialsHandler()
        return request_handler.get_all_credentials(), 200
