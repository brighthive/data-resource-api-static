""" API Version 1.0 Health Check Handler """

from datetime import datetime
from data_resource_api import ConfigurationFactory


class HealthCheckHandler(object):
    def get_health(self):
        config = ConfigurationFactory.from_env()
        return {
            'api_name': 'BrightHive Data Access API',
            'current_time': str(datetime.utcnow()),
            'current_api_version': config.get_api_version(),
            'api_status': 'OK'}, 200
