""" API Version 1.0 Programs Handler """

import os
import json
from data_resource_api.db import PathwaysProgram
from data_resource_api.validator import PathwaysProgramValidator
from data_resource_api.app.app import db


class PathwaysProgramsHandler(object):
    def get_all_programs(self):
        results = PathwaysProgram.query.all()
        programs = {'programs': []}
        for program in results:
            programs['programs'].append(program.to_dict())
        return programs, 200

    def update_program(self, program, id):
        existing_program = PathwaysProgram.query.filter_by(program_id=id).first()
        if existing_program is None:
            return {'message': 'Program with id {} does not exist'.format(
                id)}, 404

        if program is not None:
            validator = PathwaysProgramValidator()
            result = validator.validate(program)
            if len(result) > 0:
                return {'error': result}, 400
            else:
                try:
                    existing_program.program_provider = program["OrganizationName"]
                except Exception:
                    pass
                try:
                    existing_program.program_name = program["ProgramName"]
                except Exception:
                    pass
                try:
                    existing_program.program_address = program["ProgramAddress"]
                except Exception:
                    pass
                try:
                    existing_program.program_city = program["ProgramCity"]
                except Exception:
                    pass
                try:
                    existing_program.program_url = program["UrlOfProgram"]
                except Exception:
                    pass
                try:
                    existing_program.phone_number = program["PhoneNumber"]
                except Exception:
                    pass
                try:
                    existing_program.program_potential_outcome = program["CredentialLevelEarned"]
                except Exception:
                    pass
                try:
                    existing_program.program_fees = program["InStateTuition"]
                except Exception:
                    pass
                try:
                    existing_program.apprenticeship_paid_training = program["ApprenticeshipOrPaidTrainingAvailable"]
                except Exception:
                    pass
                try:
                    existing_program.provider_id = program["OrganizationIpedsId"]
                except Exception:
                    pass
                try:
                    existing_program.provider_url = program["OrganizationUrl"]
                except Exception:
                    pass
                try:
                    existing_program.program_code = program["CipCode"]
                except Exception:
                    pass
                try:
                    existing_program.major = program["MajorCluster"]
                except Exception:
                    pass
                try:
                    existing_program.program_description = program["ProgramDescription"]
                except Exception:
                    pass
                try:
                    existing_program.regional_accredition_body = program["RegionalAccreditionBody"]
                except Exception:
                    pass
                try:
                    existing_program.program_accredition_body = program["ProgrammaticAccreditionBody"]
                except Exception:
                    pass
                try:
                    existing_program.program_length = program["Duration"]
                except Exception:
                    pass
                try:
                    existing_program.total_units = program["TotalUnits"]
                except Exception:
                    pass
                try:
                    existing_program.unit_cost = program["UnitCost"]
                except Exception:
                    pass
                try:
                    existing_program.salary_paid = program["AverageWagePaidToStudent"]
                except Exception:
                    pass
                try:
                    existing_program.program_format = program["Format"]
                except Exception:
                    pass
                try:
                    existing_program.program_timing = program["Timing"]
                except Exception:
                    pass
                try:
                    existing_program.cost_of_books_and_supplies = program["ProgramFeesBooksMaterialsSupplies"]
                except Exception:
                    pass
                try:
                    existing_program.credential_earned = program["Certification"]
                except Exception:
                    pass
                try:
                    existing_program.prerequisites = program["OtherPrerequisites"]
                except Exception:
                    pass
                try:
                    existing_program.start_date = program["StartDate"]
                except Exception:
                    pass
                try:
                    existing_program.is_diploma_required = program["HsDiplomaRequired"]
                except Exception:
                    pass
                try:
                    existing_program.salary_post_graduation = program["SalaryPostGraduation"]
                except Exception:
                    pass

                try:
                    db.session.commit()
                    return existing_program.to_dict(), 201
                except Exception:
                    return {'message': 'Failed to update program.'}, 400
        else:
            return {'error': 'Request body cannot be empty.'}, 400

    def add_new_program(self, program):
        if program is not None:
            validator = PathwaysProgramValidator()
            result = validator.validate(program)
            if len(result) > 0:
                return {'error': result}, 400
            else:
                new_program = PathwaysProgram(
                    program_provider = program["OrganizationName"],
                    program_name = program["ProgramName"],
                    program_address = program["ProgramAddress"],
                    program_city = program["ProgramCity"],
                    program_url = program["UrlOfProgram"],
                    phone_number = program["PhoneNumber"],
                    program_potential_outcome = program["CredentialLevelEarned"],
                    program_fees = program["InStateTuition"],
                    apprenticeship_paid_training = \
                        program["ApprenticeshipOrPaidTrainingAvailable"])

                try:
                    new_program.provider_id = program["OrganizationIpedsId"]
                except Exception:
                    pass
                try:
                    new_program.provider_url = program["OrganizationUrl"]
                except Exception:
                    pass
                try:
                    new_program.program_code = program["CipCode"]
                except Exception:
                    pass
                try:
                    new_program.major = program["MajorCluster"]
                except Exception:
                    pass
                try:
                    new_program.program_description = program["ProgramDescription"]
                except Exception:
                    pass
                try:
                    new_program.regional_accredition_body = program["RegionalAccreditionBody"]
                except Exception:
                    pass
                try:
                    new_program.program_accredition_body = program["ProgrammaticAccreditionBody"]
                except Exception:
                    pass
                try:
                    new_program.program_length = program["Duration"]
                except Exception:
                    pass
                try:
                    new_program.total_units = program["TotalUnits"]
                except Exception:
                    pass
                try:
                    new_program.unit_cost = program["UnitCost"]
                except Exception:
                    pass
                try:
                    new_program.salary_paid = program["AverageWagePaidToStudent"]
                except Exception:
                    pass
                try:
                    new_program.program_format = program["Format"]
                except Exception:
                    pass
                try:
                    new_program.program_timing = program["Timing"]
                except Exception:
                    pass
                try:
                    new_program.cost_of_books_and_supplies = program["ProgramFeesBooksMaterialsSupplies"]
                except Exception:
                    pass
                try:
                    new_program.credential_earned = program["Certification"]
                except Exception:
                    pass
                try:
                    new_program.prerequisites = program["OtherPrerequisites"]
                except Exception:
                    pass
                try:
                    new_program.start_date = program["StartDate"]
                except Exception:
                    pass
                try:
                    new_program.is_diploma_required = program["HsDiplomaRequired"]
                except Exception:
                    pass
                try:
                    new_program.salary_post_graduation = program["SalaryPostGraduation"]
                except Exception:
                    pass
        
                try:
                    db.session.add(new_program)
                    db.session.commit()
                    return new_program.to_dict(), 201
                except Exception:
                    return {'error': 'Failed to create new program.'}, 400
        else:
            return {'error': 'Request body cannot be empty.'}, 400

    def get_program_by_id(self, id):
        try:
            program = PathwaysProgram.query.filter_by(program_id=id).first()
            if program is not None:
                return program.to_dict(), 200
            else:
                return {'error': 'PathwaysProgram with id {} does not exist.'.format(
                    id)}, 404
        except Exception:
            return {'error': 'Invalid request.'}, 400

    def delete_program_by_id(self, id):
        try:
            program = PathwaysProgram.query.filter_by(program_id=id).first()
            if program is not None:
                program_data = program.to_dict()
                db.session.delete(program)
                db.session.commit()
                return program_data, 200
            else:
                return {
                    'error': 'Program with id {} does not exist.'.format(id)
                }, 404
        except Exception:
            return {
                'error': 'Program with id {} does not exist.'.format(id)}, 404
