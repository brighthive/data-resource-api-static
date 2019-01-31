""" Unit tests for API Endpoints """

from pocha import describe, it, before
from expects import expect, be
from app import app


client = app.test_client()


@describe('Test API Endpoints')
def _():
    @it('Should return all programs')
    def get_all_programs():
        response = client.get('/programs')
        expect(response.status_code).to(be(200))

    @it('Should return all credentials')
    def get_all_credentials():
        response = client.get('/credentials')
        expect(response.status_code).to(be(200))

    @it('Should return all participants')
    def get_all_participants():
        response = client.get('/participants')
        expect(response.status_code).to(be(200))
