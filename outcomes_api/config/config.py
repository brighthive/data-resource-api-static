""" Application Configuration """

import os
import json


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USER = 'test_user'
    PASSWORD = 'test_password'
    DATABASE = 'tpot_programs'
    HOSTNAME = 'localhost'
    PORT = 5432
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        USER,
        PASSWORD,
        HOSTNAME,
        PORT,
        DATABASE
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


class TestConfig(Config):
    CONTAINER_NAME = 'postgres-test'
    IMAGE_NAME = 'postgres'
    IMAGE_VERSION = '11.1'
    DATABASE = 'tpot_programs_test'
    PORT = 5433


class ConfigurationFactory(object):
    @staticmethod
    def get_config(config_type: str):
        if config_type.upper() == 'TEST':
            return TestConfig()
        else:
            return Config()

    @staticmethod
    def from_env():
        environment = os.getenv('APP_ENV', 'DEVELOPMENT')
        ConfigurationFactory.get_config(environment)
