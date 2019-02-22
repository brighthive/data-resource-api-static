""" Unit tests for API Endpoints """

import json
import copy
from pocha import describe, it, before, after
from expects import expect, be, equal, be_above
from data_resource_api import app, Config

client = app.test_client()

TOKEN = '269952015c751bcd64428e6e77c355a7'
AUTHENTICATED_HEADER = {
    'X-Api-Version': '1.0.0',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {}'.format(TOKEN)
}

UNAUTHENTICATED_HEADER = {
    'X-Api-Version': '1.0.0',
    'Content-Type': 'application/json'
}


@describe('Test API Auth Mechanism')
def _():
    @it('Should allow only authenticated users to access secured resources')
    def test_api_auth_header():
        response = client.get(
            '/programs', headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
        response = client.get(
            '/programs', headers=UNAUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(401))


@describe('Test Health Check Resource')
def _():
    @it('Should return a health check status')
    def test_get_healthcheck():
        response = client.get('/health', headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
        data = json.loads(response.data)
        expect(data['api_status']).to(equal('OK'))


@describe('Test Programs Resource')
def _():

    @it('Should return all programs')
    def test_get_all_programs():
        response = client.get('/programs', headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
        data = json.loads(response.data)
        expect(len(data['programs'])).to(be_above(1))

    @it('Should return a program by its identifer')
    def test_get_program_by_id():
        response = client.get('/programs', headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
        selected_program = json.loads(response.data)['programs'][0]

        # should return a not found status code
        response = client.get(
            '/programs/{}'.format(selected_program['program_id'] * 1000),
            headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(404))

        # should return a 200 status code
        response = client.get(
            '/programs/{}'.format(selected_program['program_id']),
            headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
        program = json.loads(response.data)
        expect(program['program_id']).to(equal(selected_program['program_id']))
        expect(program['program_name']).to(
            equal(selected_program['program_name']))

    @it('Should perform CRUD operations on program endpoints')
    def test_program_crud_ops():
        # get an existing program
        response = client.get('/programs', headers=AUTHENTICATED_HEADER)
        programs = json.loads(response.data)['programs']
        expect(len(programs)).to(be_above(1))
        selected_program = programs[0]
        del(selected_program['program_id'])

        # attempt to post the data
        response = client.post(
            '/programs', headers=AUTHENTICATED_HEADER, data=json.dumps(
                selected_program))

        # will initally fail due to validation rules
        expect(response.status_code).to(equal(400))

        # change fields to integer
        selected_program['program_length_hours'] = 0
        selected_program['program_length_weeks'] = 0

        # will now successfully load
        response = client.post(
            '/programs', headers=AUTHENTICATED_HEADER, data=json.dumps(
                selected_program))
        expect(response.status_code).to(equal(201))

        # get the program by it's id
        expected_program = json.loads(response.data)
        response = client.get(
            '/programs/{}'.format(expected_program['program_id']),
            headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
        actual_program = json.loads(response.data)
        expect(expected_program['program_id']).to(equal(actual_program[
            'program_id']))

        # update the program
        updated_program = copy.deepcopy(expected_program)
        del(updated_program['program_id'])
        updated_program['program_length_hours'] = 80
        updated_program['program_length_weeks'] = 2
        response = client.put('/programs/{}'.format(expected_program[
            'program_id']), headers=AUTHENTICATED_HEADER, data=json.dumps(
            updated_program))
        expect(response.status_code).to(equal(201))
        updated_program = json.loads(response.data)
        expect(updated_program['program_length_hours']).to(equal(80))
        expect(updated_program['program_length_weeks']).to(equal(2))

        # delete the program
        response = client.delete(
            '/programs/{}'.format(updated_program['program_id']),
            headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))


@describe('Test Providers Resource')
def _():
    @it('Should return all providers')
    def test_get_all_providers():
        response = client.get('/providers', headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
        data = json.loads(response.data)
        expect(len(data['providers'])).to(be_above(1))

    @it('Should return a provider by its identifer')
    def test_get_provider_by_id():
        response = client.get('/providers', headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
        selected_provider = json.loads(response.data)['providers'][0]

        # should return a not found status code
        response = client.get(
            '/providers/{}'.format(
                selected_provider['provider_id'] * 1000),
            headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(404))

        # should return a 200 status code
        response = client.get(
            '/providers/{}'.format(selected_provider['provider_id']),
            headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
        provider = json.loads(response.data)
        expect(provider['provider_id']).to(
            equal(selected_provider['provider_id']))
        expect(provider['provider_name']).to(
            equal(selected_provider['provider_name']))

    @it('Should perform CRUD operations on provider endpoints')
    def test_provider_crud_ops():
        # get an existing provider
        response = client.get('/providers', headers=AUTHENTICATED_HEADER)
        providers = json.loads(response.data)['providers']
        expect(len(providers)).to(be_above(1))
        selected_provider = providers[0]
        del(selected_provider['provider_id'])

        # attempt to post the data
        response = client.post(
            '/providers', headers=AUTHENTICATED_HEADER, data=json.dumps(
                selected_provider))
        expect(response.status_code).to(equal(201))

        # get the provider by it's id
        expected_provider = json.loads(response.data)
        response = client.get(
            '/providers/{}'.format(expected_provider['provider_id']),
            headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
        actual_provider = json.loads(response.data)
        expect(expected_provider['provider_id']).to(equal(actual_provider[
            'provider_id']))

        # update the program
        updated_provider = copy.deepcopy(expected_provider)
        del(updated_provider['provider_id'])
        updated_provider['provider_name'] = 'A Learning Institution'
        updated_provider['year_incorporated'] = 1776
        response = client.put('/providers/{}'.format(expected_provider[
            'provider_id']), headers=AUTHENTICATED_HEADER, data=json.dumps(
            updated_provider))
        expect(response.status_code).to(equal(201))
        updated_provider = json.loads(response.data)
        expect(updated_provider['provider_name']).to(equal(
            'A Learning Institution'))
        expect(updated_provider['year_incorporated']).to(equal(1776))

        # delete the provider
        response = client.delete(
            '/providers/{}'.format(updated_provider['provider_id']),
            headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
