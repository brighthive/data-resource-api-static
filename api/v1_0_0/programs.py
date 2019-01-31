""" Programs Resource


"""

from flask_restful import Resource


class ProgramsResource(Resource):
    def get(self):
        return {'message': 'programs resource'}, 200
