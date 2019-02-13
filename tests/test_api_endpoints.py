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
        program = json.loads(response.data)['program']
        expect(program['program_id']).to(equal(selected_program['program_id']))
        expect(program['program_name']).to(
            equal(selected_program['program_name']))
