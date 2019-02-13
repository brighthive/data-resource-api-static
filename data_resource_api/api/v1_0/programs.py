""" API Version 1.0 Programs Handler """

import os
import json
from data_resource_api.db import Program
from data_resource_api.validator import ProgramValidator


class ProgramsHandler(object):
    def get_all_programs(self):
        results = Program.query.all()
        programs = {'programs': []}
        for program in results:
            programs['programs'].append(program.to_dict())
        return programs, 200

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

    def get_program_by_id(self, id):
        try:
            program = Program.query.filter_by(program_id=id).first()
            if program is not None:
                return {'program': program.to_dict()}, 200
            else:
                return {'message': 'Program with id {} does not exist'.format(
                    id)}, 404
        except Exception:
            return {'error': 'Invalid request'}, 400
