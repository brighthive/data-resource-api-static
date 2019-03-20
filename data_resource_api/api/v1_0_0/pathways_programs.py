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
                    existing_program.program_name = program['ProgramName']
                except Exception:
                    pass

                try:
                    existing_program.program_provider = program['ProgramProvider']
                except Exception:
                    pass

                try:
                    existing_program.program_description = program[
                        'ProgramDescription']
                except Exception:
                    pass

                try:
                    existing_program.provider_url = program['ProviderUrl']
                except Exception:
                    pass

                try:
                    existing_program.provider_address = program['ProviderAddress']
                except Exception:
                    pass

                try:
                    existing_program.major = program['Major']
                except Exception:
                    pass

                try:
                    existing_program.program_url = program['ProgramUrl']
                except Exception:
                    pass

                try:
                    existing_program.program_potential_outcome = program[
                        'ProgramPotentialOutcome']
                except Exception:
                    pass

                try:
                    existing_program.program_fees = program[
                        'ProgramFees']
                except Exception:
                    pass
                try:
                    existing_program.salary_paid = program['SalaryPaid']
                except Exception:
                    pass

                try:
                    existing_program.program_length = program[
                        'ProgramLength']
                except Exception:
                    pass

                try:
                    existing_program.cost_of_books_and_supplies = program[
                        'CostOfBooksAndSupplies']
                except Exception:
                    pass

                try:
                    existing_program.credential_earned = program[
                        'CredentialEarned']
                except Exception:
                    pass

                try:
                    existing_program.accreditation_name = program['AccreditationName']
                except Exception:
                    pass

                try:
                    existing_program.provider_id = program[
                        'ProviderId']
                except Exception:
                    pass

                try:
                    existing_program.provider_latitude = program[
                        'ProviderLatitude']
                except Exception:
                    pass

                try:
                    existing_program.provider_longitude = program[
                        'ProviderLongitude']
                except Exception:
                    pass

                try:
                    existing_program.program_address = program[
                        'ProgramAddress']
                except Exception:
                    pass

                try:
                    existing_program.total_units = program[
                        'TotalUnits']
                except Exception:
                    pass

                try:
                    existing_program.unit_cost = program[
                        'UnitCost']
                except Exception:
                    pass

                try:
                    existing_program.is_preparation = program[
                        'IsPreparation']
                except Exception:
                    pass

                try:
                    existing_program.is_occupational_requirement = program[
                        'IsOccupationalRequirement']
                except Exception:
                    pass

                try:
                    existing_program.start_date = program[
                        'StartDate']
                except Exception:
                    pass

                try:
                    existing_program.is_diploma_required = program[
                        'IsDiplomaRequired']
                except Exception:
                    pass

                try:
                    existing_program.prerequisites = program[
                        'Prerequisites']
                except Exception:
                    pass

                try:
                    existing_program.financial_aid5 = program[
                        'FinancialAid5']
                except Exception:
                    pass

                try:
                    existing_program.financial_aid4 = program[
                        'FinancialAid4']
                except Exception:
                    pass

                try:
                    existing_program.financial_aid3 = program[
                        'FinancialAid3']
                except Exception:
                    pass

                try:
                    existing_program.financial_aid2 = program[
                        'FinancialAid2']
                except Exception:
                    pass

                try:
                    existing_program.financial_aid1 = program[
                        'FinancialAid1']
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
                    program_provider = program['ProgramProvider'],
                    provider_url = program['ProviderUrl'],
                    provider_address = program['ProviderAddress'],
                    major = program['Major'],
                    program_name = program['ProgramName'],
                    program_url = program['ProgramUrl'],
                    program_description = program['ProgramDescription'],
                    program_potential_outcome = program['ProgramPotentialOutcome'],
                    program_fees = program['ProgramFees'],
                    salary_paid = program['SalaryPaid'],
                    program_length = program['ProgramLength'],
                    cost_of_books_and_supplies = program['CostOfBooksAndSupplies'],
                    credential_earned = program['CredentialEarned'],
                    accreditation_name = program['AccreditationName'])

                try:
                    new_program.provider_id = program['ProviderId']
                except Exception:
                    pass
                try:
                    new_program.provider_latitude = program['ProviderLatitude']
                except Exception:
                    pass
                try:
                    new_program.provider_longitude = program['ProviderLongitude']
                except Exception:
                    pass
                try:
                    new_program.program_address = program['ProgramAddress']
                except Exception:
                    pass
                try:
                    new_program.total_units = program['TotalUnits']
                except Exception:
                    pass
                try:
                    new_program.unit_cost = program['UnitCost']
                except Exception:
                    pass
                try:
                    new_program.is_preparation = program['IsPreparation']
                except Exception:
                    pass
                try:
                    new_program.is_occupational_requirement = program['IsOccupationalRequirement']
                except Exception:
                    pass
                try:
                    new_program.start_date = program['StartDate']
                except Exception:
                    pass
                try:
                    new_program.is_diploma_required = program['IsDiplomaRequired']
                except Exception:
                    pass
                try:
                    new_program.prerequisites = program['Prerequisites']
                except Exception:
                    pass
                try:
                    new_program.financial_aid5 = program['FinancialAid5']
                except Exception:
                    pass
                try:
                    new_program.financial_aid4 = program['FinancialAid4']
                except Exception:
                    pass
                try:
                    new_program.financial_aid3 = program['FinancialAid3']
                except Exception:
                    pass
                try:
                    new_program.financial_aid2 = program['FinancialAid2']
                except Exception:
                    pass
                try:
                    new_program.financial_aid1 = program['FinancialAid1']
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
