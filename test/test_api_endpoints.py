""" Unit tests for API Endpoints """

import json
from pocha import describe, it, before
from expects import expect, be, equal
from app import app


client = app.test_client()


@describe('Test API GET Endpoints')
def _():
    @it('Should return all programs')
    def get_all_programs():
        response = client.get('/programs', headers={'x-api-version': 'v1.0'})
        expect(response.status_code).to(be(200))

    @it('Should return all credentials')
    def get_all_credentials():
        response = client.get('/credentials')
        expect(response.status_code).to(be(200))

    @it('Should return all participants')
    def get_all_participants():
        response = client.get('/participants')
        expect(response.status_code).to(be(200))


@describe('Test API POST Endpoints')
def _():
    @it('Should add a new program if the data is valid')
    def add_new_program():
        response = client.post(
            '/programs', headers={'x-api-version': 'v1.0'})
        expect(response.status_code).to(equal(400))

        content = {'message': 'a thing'}
        # response = client.post(
        #     '/programs',
        #     headers={'content-type': 'application/json'},
        #     data=json.dumps(content))
        # expect(response.status_code).to(equal(201))

    @it('Should add a new credential if the data is valid')
    def add_new_credential():
        response = client.post(
            '/credentials', headers={'x-api-version': 'v1.0'})
        expect(response.status_code).to(equal(400))

        content = {'message': 'a thing'}
        response = client.post(
            '/credentials',
            headers={'content-type': 'application/json'},
            data=json.dumps(content))
        expect(response.status_code).to(equal(201))

    @it('Should add a new participant if the data is valid')
    def add_new_participant():
        response = client.post(
            '/participants', headers={'x-api-version': 'v1.0'})
        expect(response.status_code).to(equal(400))

        content = {'message': 'a thing'}
        response = client.post(
            '/participants',
            headers={'content-type': 'application/json'},
            data=json.dumps(content))
        expect(response.status_code).to(equal(201))

    @it('Should add a new provider if the data is valid')
    def add_new_provider():
        response = client.post(
            '/providers', headers={'x-api-version': 'v1.0'})
        expect(response.status_code).to(equal(400))

        content = {'message': 'a thing'}
        response = client.post(
            '/providers',
            headers={'content-type': 'application/json'},
            data=json.dumps(content))
        expect(response.status_code).to(equal(201))
