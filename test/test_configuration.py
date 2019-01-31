""" Unit tests for Configuration Object """

from pocha import describe, it, before
from expects import expect, equal
from config import Config


@describe('Test Application Configuration')
def _():
    @it('Should return the API version number')
    def get_api_version():
        expected_api_version = 'v1.0'
        api_version = Config.get_api_version()
        expect(api_version).to(equal(expected_api_version))
