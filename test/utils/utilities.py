""" Generic Testing Utilities. """

import docker
from outcomes_api import Config


def setup_database():
    client = docker.from_env()
    containers = client.containers.list()
    for container in containers:
        container.stop()
        container.remove()


def populate_database():
    print('Populating database')


def teardown_database():
    print('Tearing down database')
