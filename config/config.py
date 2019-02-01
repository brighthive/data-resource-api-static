""" Application Configuration """

import os
import json


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://test_user:test_password@localhost:5432/tpot_programs'

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
