""" API Version 1.0 Programs Handler """

import os
import json
from db import Program
from validator import ProgramValidator


class ProgramsHandler(object):
    def get_all_programs(self):
        return {'message': 'programs api version 1.0'}

    def add_new_program(self, program):
        validator = ProgramValidator()
        if program is not None:
            result = validator.validate(program)
            if len(result) > 0:
                return {'error': json.dumps(result)}, 400
            else:
                return {'message': 'Successfuly sent valid data!'}, 200
        else:
            return {'message': 'request body cannot be empty'}, 400
