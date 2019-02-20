""" Launch PostgreSQL Development Container

Launches a PostgreSQL development container and populates it with sample
datasets.

"""

import os
import sys
import docker
import json
from time import sleep
from flask_migrate import upgrade

relative_path = os.path.dirname(os.path.relpath(__file__))
absolute_path = os.path.dirname(os.path.abspath(__file__))
root_path = absolute_path.split(relative_path)[0]

# add the path of the application to the system path
if root_path:
    sys.path.append(root_path)
    from data_resource_api import DatabaseConfigurationUtility

db_config = DatabaseConfigurationUtility('DEVELOPMENT', True)


def usage():
    print('Not doing it right...')


def start_dev_container():
    db_config.start_database(True)


def stop_dev_container():
    db_config.stop_database()


def restart_dev_container():
    db_config.stop_database()
    sleep(5)
    db_config.start_database(True)


def manage_command(command: str):
    if command == '--start':
        start_dev_container()
    elif command == '--stop':
        stop_dev_container()
    elif command == '--restart':
        restart_dev_container()
    else:
        print('Unrecognized flag: {}'.format(command))
        usage()
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        manage_command(str.lower(sys.argv[1]))
