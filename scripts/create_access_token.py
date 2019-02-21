""" Random access token generator for mock service """

import os
import sys
from uuid import uuid4

relative_path = os.path.dirname(os.path.relpath(__file__))
absolute_path = os.path.dirname(os.path.abspath(__file__))
root_path = absolute_path.split(relative_path)[0]

# add the path of the application to the system path
if root_path:
    sys.path.append(root_path)
    from data_resource_api import db, Token


def usage():
    print('You are doing it incorrectly')


def create_access_token():
    new_token = str(uuid4()).replace('-', '')
    try:
        token = Token(new_token)
        db.session.add(token)
        db.session.commit()
        print('Successfully created new access token -> {}'.format(
            token.token))
        sys.exit(0)
    except Exception:
        print('Failed to create new token.')


if __name__ == '__main__':
    if len(sys.argv) != 1:
        usage()
        sys.exit(1)
    create_access_token()
