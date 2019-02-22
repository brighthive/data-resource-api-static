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

    @it('Should list the credentials that a program provides')
    def test_program_credential():
        # get an existing program
        response = client.get('/programs', headers=AUTHENTICATED_HEADER)
        programs = json.loads(response.data)['programs']
        expect(len(programs)).to(be_above(1))
        selected_program = programs[0]
        response = client.get('/programs/{}/credentials'.format(
            selected_program['program_id']), headers=AUTHENTICATED_HEADER)
        program_credential = json.loads(response.data)
        expect(program_credential['program_id']).to(
            equal(selected_program['program_id']))
        expect(len(program_credential['credentials'])).to(be_above(0))

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

    @it('Should list the programs provided by providers')
    def test_get_program_by_provider():
        response = client.get('/providers', headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
        selected_provider = json.loads(response.data)['providers'][0]
        response = client.get('/providers/{}/programs'.format(
            selected_provider['provider_id']), headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
        provider = json.loads(response.data)
        expect(len(provider['programs'])).to(be_above(0))


@describe('Test Credentials Resource')
def _():
    @it('Should return all credentials')
    def test_get_all_credentials():
        response = client.get('/credentials', headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
        data = json.loads(response.data)
        expect(len(data['credentials'])).to(be_above(1))

    @it('Should return a credential by its identifer')
    def test_get_credential_by_id():
        response = client.get('/credentials', headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
        selected_credential = json.loads(response.data)['credentials'][0]

        # should return a not found status code
        response = client.get(
            '/credentials/{}'.format(
                selected_credential['credential_id'] * 1000),
            headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(404))

        # should return a 200 status code
        response = client.get(
            '/credentials/{}'.format(selected_credential['credential_id']),
            headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
        provider = json.loads(response.data)
        expect(provider['credential_id']).to(
            equal(selected_credential['credential_id']))
        expect(provider['credential_name']).to(
            equal(selected_credential['credential_name']))

    @it('Should perform CRUD operations on credential endpoints')
    def test_credential_crud_ops():
        # get an existing credential
        response = client.get('/credentials', headers=AUTHENTICATED_HEADER)
        credentials = json.loads(response.data)['credentials']
        expect(len(credentials)).to(be_above(1))
        selected_credential = credentials[0]
        del(selected_credential['credential_id'])

        # attempt to post the data
        response = client.post(
            '/credentials', headers=AUTHENTICATED_HEADER, data=json.dumps(
                selected_credential))
        expect(response.status_code).to(equal(201))

        # get the credential by it's id
        expected_credential = json.loads(response.data)
        response = client.get(
            '/credentials/{}'.format(expected_credential['credential_id']),
            headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
        actual_provider = json.loads(response.data)
        expect(expected_credential['credential_id']).to(equal(actual_provider[
            'credential_id']))

        # update the credential
        updated_credential = copy.deepcopy(expected_credential)
        del(updated_credential['credential_id'])
        updated_credential['credential_name'] = 'A New Credential'
        updated_credential['language'] = 'Sprench'
        response = client.put('/credentials/{}'.format(expected_credential[
            'credential_id']), headers=AUTHENTICATED_HEADER, data=json.dumps(
            updated_credential))
        expect(response.status_code).to(equal(201))
        updated_credential = json.loads(response.data)
        expect(updated_credential['credential_name']).to(equal(
            'A New Credential'))
        expect(updated_credential['language']).to(equal('Sprench'))

        # delete the credential
        response = client.delete(
            '/credentials/{}'.format(updated_credential['credential_id']),
            headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
