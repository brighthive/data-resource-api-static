""" Provision A Database with Test Data """

import os
import sys
from flask_migrate import upgrade

relative_path = os.path.dirname(os.path.relpath(__file__))
absolute_path = os.path.dirname(os.path.abspath(__file__))
root_path = absolute_path.split(relative_path)[0]

# add the path of the application to the system path
if root_path:
    sys.path.append(root_path)
    from data_resource_api import app, ConfigurationFactory


def usage():
    print('You are doing it incorrectly')


def provision_database():
    app.config.from_object(ConfigurationFactory.from_env())
    with app.app_context():
        migrations_dir = os.path.join(
            root_path, 'data_resource_api', 'db', 'migrations')
        upgrade(directory=migrations_dir)


if __name__ == '__main__':
    if len(sys.argv) != 1:
        usage()
        sys.exit(1)
    provision_database()
