""" API Version 1.0 Health Check Handler """


class HealthCheckHandler(object):
    def get_health(self):
        return {'message': 'Data Resource API is Alive!'}, 200
