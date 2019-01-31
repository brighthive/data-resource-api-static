""" Programs Resource


"""

import os
from flask_restful import Resource
from api.v1_0 import V1_0_ProgramsHandler


class ProgramsResource(Resource):
    def get(self):
        request_handler = V1_0_ProgramsHandler()
        return request_handler.get_all_programs(), 200
