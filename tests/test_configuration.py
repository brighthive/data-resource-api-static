""" Unit tests for Configuration Object """

from pocha import describe, it, before
from expects import expect, equal
from data_resource_api import ConfigurationFactory


@describe('Test Application Configuration')
def _():
    @it('Should return the API version number')
    def get_api_version():
        expected_api_version = 'v1.0'
        config = ConfigurationFactory.get_config('TEST')
        api_version = config.get_api_version()
        expect(api_version).to(equal(expected_api_version))
