""" Application Configuration """

import os
import json


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRES_USER = 'test_user'
    POSTGRES_PASSWORD = 'test_password'
    POSTGRES_DATABASE = 'tpot_programs'
    POSTGRES_HOSTNAME = 'localhost'
    POSTGRES_PORT = 5432
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOSTNAME,
        POSTGRES_PORT,
        POSTGRES_DATABASE
    )
    DEFAULT_VALIDATOR_HOME = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '../schema')
    VALIDATOR_HOME = os.getenv('VALIDATOR_HOME', DEFAULT_VALIDATOR_HOME)

    @staticmethod
    def get_api_version():
        api_version = None
        settings_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'settings.json')
        if os.path.exists(settings_file) and os.path.isfile(settings_file):
            with open(settings_file, 'r') as f:
                settings = json.load(f)
            api_version = settings['API_VERSION']
        return str(api_version).strip()


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        os.environ['FLASK_ENV'] = 'development'


class TestConfig(Config):
    def __init__(self):
        super().__init__()
        os.environ['FLASK_ENV'] = 'testing'

    CONTAINER_NAME = 'postgres-test'
    IMAGE_NAME = 'postgres'
    IMAGE_VERSION = '11.1'
    POSTGRES_DATABASE = 'tpot_programs_test'
    POSTGRES_PORT = 5433
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        Config.POSTGRES_USER,
        Config.POSTGRES_PASSWORD,
        Config.POSTGRES_HOSTNAME,
        POSTGRES_PORT,
        POSTGRES_DATABASE
    )

    def get_postgresql_image(self):
        return '{}:{}'.format(self.IMAGE_NAME, self.IMAGE_VERSION)


class SandboxConfig(Config):
    def __init__(self):
        super().__init__()
        os.environ['FLASK_ENV'] = 'production'


class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        os.environ['FLASK_ENV'] = 'production'


class ConfigurationFactory(object):
    @staticmethod
    def get_config(config_type: str):
        if config_type.upper() == 'TEST':
            return TestConfig()
        elif config_type.upper() == 'DEVELOPMENT':
            return DevelopmentConfig()
        elif config_type.upper() == 'SANDBOX':
            return SandboxConfig()
        elif config_type.upper() == 'PRODUCTION':
            return ProductionConfig()

    @staticmethod
    def from_env():
        environment = os.getenv('APP_ENV', 'DEVELOPMENT')
        return ConfigurationFactory.get_config(environment)
