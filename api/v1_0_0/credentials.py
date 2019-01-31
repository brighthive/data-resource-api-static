""" Credentials Resource


"""

from flask_restful import Resource


class CredentialsResource(Resource):
    def get(self):
        return {'message': 'credentials resource'}, 200
