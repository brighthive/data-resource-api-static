""" Unit tests for API Endpoints """

import json
from pocha import describe, it, before, after
from expects import expect, be, equal, be_above
from outcomes_api import app, Config

client = app.test_client()

TOKEN = '269952015c751bcd64428e6e77c355a7'
AUTHENTICATED_HEADER = {
    'X-Api-Version': 'v1.0',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {}'.format(TOKEN)
}

UNAUTHENTICATED_HEADER = {
    'X-Api-Version': 'v1.0',
    'Content-Type': 'application/json'
}


@describe('Test API GET Endpoints')
def _():
    @it('Should return all programs')
    def get_all_programs():
        response = client.get(
            '/programs', headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))

        response = client.get(
            '/programs', headers=UNAUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(401))

    @it('Should return all credentials')
    def get_all_credentials():
        response = client.get('/credentials', headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))
        data = json.loads(response.data)
        expect(len(data)).to(be_above(0))

        response = client.get('/credentials', headers=UNAUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(401))

    @it('Should return all participants')
    def get_all_participants():
        response = client.get('/participants', headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(200))

        response = client.get('/participants', headers=UNAUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(401))


@describe('Test API POST Endpoints')
def _():
    @it('Should add a new program if the data is valid')
    def add_new_program():
        response = client.post(
            '/programs', headers=AUTHENTICATED_HEADER)
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
            '/credentials', headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(400))

        content = {'message': 'a thing'}
        response = client.post(
            '/credentials',
            headers=AUTHENTICATED_HEADER,
            data=json.dumps(content))
        expect(response.status_code).to(equal(201))

    @it('Should add a new participant if the data is valid')
    def add_new_participant():
        response = client.post(
            '/participants', headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(400))

        content = {'message': 'a thing'}
        response = client.post(
            '/participants',
            headers=AUTHENTICATED_HEADER,
            data=json.dumps(content))
        expect(response.status_code).to(equal(201))

    @it('Should add a new provider if the data is valid')
    def add_new_provider():
        response = client.post(
            '/providers', headers=AUTHENTICATED_HEADER)
        expect(response.status_code).to(equal(400))

        content = {'message': 'a thing'}
        response = client.post(
            '/providers',
            headers=AUTHENTICATED_HEADER,
            data=json.dumps(content))
        expect(response.status_code).to(equal(201))
