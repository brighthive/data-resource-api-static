""" API Version 1.0 Programs Handler """

import os
import json
from data_resource_api.db import Program
from data_resource_api.validator import ProgramValidator
from data_resource_api.app.app import db


class ProgramsHandler(object):
    def get_all_programs(self):
        results = Program.query.all()
        programs = {'programs': []}
        for program in results:
            programs['programs'].append(program.to_dict())
        return programs, 200

    def update_program(self, program, id):
        existing_program = Program.query.filter_by(program_id=id).first()
        if existing_program is None:
            return {'message': 'Program with id {} does not exist'.format(
                id)}, 404

        validator = ProgramValidator()
        if program is not None:
            result = validator.validate(program)
            if len(result) > 0:
                return {'error': result}, 400
            else:
                try:
                    existing_program.program_name = program['program_name']
                except Exception:
                    pass

                try:
                    existing_program.program_code = program['program_code']
                except Exception:
                    pass

                try:
                    existing_program.program_description = program[
                        'program_description']
                except Exception:
                    pass

                try:
                    existing_program.program_status = program['program_status']
                except Exception:
                    pass

                try:
                    existing_program.program_fees = program['program_fees']
                except Exception:
                    pass

                try:
                    existing_program.provider_id = program['provider_id']
                except Exception:
                    pass

                try:
                    existing_program.location_id = program['location_id']
                except Exception:
                    pass

                try:
                    existing_program.eligibility_criteria = program[
                        'eligibility_criteria']
                except Exception:
                    pass

                try:
                    existing_program.potential_outcome_id = program[
                        'potential_outcome_id']
                except Exception:
                    pass
                try:
                    existing_program.program_url = program['program_url']
                except Exception:
                    pass

                try:
                    existing_program.credential_earned = program[
                        'credential_earned_id']
                except Exception:
                    pass

                # optional fields
                try:
                    existing_program.program_contact_phone = program[
                        'program_contact_phone']
                except Exception:
                    pass

                try:
                    existing_program.program_contact_email = program[
                        'program_contact_email']
                except Exception:
                    pass

                try:
                    existing_program.languages = program['languages']
                except Exception:
                    pass

                try:
                    existing_program.current_intake_capacity = program[
                        'current_intake_capacity']
                except Exception:
                    pass

                try:
                    existing_program.program_offering_model = program[
                        'program_offering_model']
                except Exception:
                    pass

                try:
                    existing_program.program_length_hours = program[
                        'program_length_hours']
                except Exception:
                    pass

                try:
                    existing_program.program_length_weeks = program[
                        'program_length_weeks']
                except Exception:
                    pass

                try:
                    existing_program.prerequisite_id = program[
                        'prerequisite_id']
                except Exception:
                    pass

                try:
                    existing_program.program_soc = program[
                        'program_soc']
                except Exception:
                    pass

                try:
                    existing_program.funding_sources = program[
                        'funding_sources']
                except Exception:
                    pass

                try:
                    existing_program.on_etpl = program[
                        'on_etpl']
                except Exception:
                    pass

                try:
                    existing_program.cost_of_books_and_supplies = program[
                        'cost_of_books_and_supplies']
                except Exception:
                    pass

                try:
                    db.session.commit()
                    return existing_program.to_dict(), 201
                except Exception:
                    return {'message': 'Failed to update program'}, 400
        else:
            return {'message': 'request body cannot be empty'}, 400

    def add_new_program(self, program):
        validator = ProgramValidator()
        if program is not None:
            result = validator.validate(program)
            if len(result) > 0:
                return {'error': result}, 400
            else:
                new_program = Program(
                    name=program['program_name'],
                    code=program['program_code'],
                    description=program['program_description'],
                    status=program['program_status'],
                    fees=program['program_fees'],
                    provider_id=program['provider_id'],
                    location_id=program['location_id'],
                    eligibility_criteria=program['eligibility_criteria'],
                    potential_outcome_id=program['potential_outcome_id'],
                    program_url=program['program_url'],
                    credential_earned=program['credential_earned_id'])

                # optional fields
                try:
                    new_program.program_contact_phone = program[
                        'program_contact_phone']
                except Exception:
                    pass

                try:
                    new_program.program_contact_email = program[
                        'program_contact_email']
                except Exception:
                    pass

                try:
                    new_program.languages = program['languages']
                except Exception:
                    pass

                try:
                    new_program.current_intake_capacity = program[
                        'current_intake_capacity']
                except Exception:
                    pass

                try:
                    new_program.program_offering_model = program[
                        'program_offering_model']
                except Exception:
                    pass

                try:
                    new_program.program_length_hours = program[
                        'program_length_hours']
                except Exception:
                    pass

                try:
                    new_program.program_length_weeks = program[
                        'program_length_weeks']
                except Exception:
                    pass

                try:
                    new_program.prerequisite_id = program[
                        'prerequisite_id']
                except Exception:
                    pass

                try:
                    new_program.program_soc = program[
                        'program_soc']
                except Exception:
                    pass

                try:
                    new_program.funding_sources = program[
                        'funding_sources']
                except Exception:
                    pass

                try:
                    new_program.on_etpl = program[
                        'on_etpl']
                except Exception:
                    pass

                try:
                    new_program.cost_of_books_and_supplies = program[
                        'cost_of_books_and_supplies']
                except Exception:
                    pass

                try:
                    db.session.add(new_program)
                    db.session.commit()
                    return new_program.to_dict(), 201
                except Exception:
                    return {'message': 'Failed to create new program'}, 400
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

    def delete_program_by_id(self, id):
        try:
            program = Program.query.filter_by(program_id=id).first()
            if program is not None:
                program_data = program.to_dict()
                db.session.delete(program)
                db.session.commit()
                return {'program': program_data}, 200

        except Exception:
            return {
                'status': 404,
                'error': 'Program with id {} does not exist'.format(id)}, 404
