""" API Version 1.0 Programs Handler """

from db import Program


class ProgramsHandler(object):
    def get_all_programs(self):
        return {'message': 'programs api version 1.0'}

    def add_new_program(self, program):
        if program is not None:
            return {'message': 'added a new program'}, 201
        else:
            return {'message': 'request body cannot be empty'}, 400
