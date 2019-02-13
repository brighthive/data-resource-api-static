""" API Version 1.0 Programs Handler """

import os
import json
from outcomes_api.db import Program
from outcomes_api.validator import ProgramValidator


class ProgramsHandler(object):
    def get_all_programs(self):
        results = Program.query.all()
        programs = {'programs': []}
        for program in results:
            programs['programs'].append(program.to_dict())
        return programs

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
