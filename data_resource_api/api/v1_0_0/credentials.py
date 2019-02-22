""" API Version 1.0 Credentials Handler """

import json
from data_resource_api.db import Credential
from data_resource_api.validator import CredentialValidator
from data_resource_api.app.app import db


class CredentialsHandler(object):
    def get_all_credentials(self):
        all_results = Credential.query.all()
        credentials = {'credentials': []}
        for result in all_results:
            credentials['credentials'].append(result.to_dict())
        return credentials

    def add_new_credential(self, credential):
        if credential is not None:
            validator = CredentialValidator()
            result = validator.validate(credential)
            if len(result) > 0:
                return {'error': result}, 400
            else:
                new_credential = Credential(
                    provider_id=credential['provider_id'],
                    name=credential['credential_name'],
                    description=credential['credential_description'],
                    credential_type_id=credential['credential_type_id'],
                    credential_status_type=credential[
                        'credential_status_type'],
                    audience=credential['audience'],
                    language=credential['language'],
                    ce_ctid=credential['ctid'],
                    webpage=credential['webpage']
                )
                try:
                    db.session.add(new_credential)
                    db.session.commit()
                    return new_credential.to_dict(), 201
                except Exception as e:
                    print(e)
                    return {'error': 'Failed to create new credential.'}, 400
        else:
            return {'error': 'Request body cannot be empty'}, 400

    def get_credential_by_id(self, id):
        try:
            credential = Credential.query.filter_by(credential_id=id).first()
            if credential is not None:
                return credential.to_dict(), 200
            else:
                return {'error': 'Credential with id {} does not exist.'
                        .format(id)}, 404
        except Exception:
            return {'error': 'Invalid request.'}, 400

    def update_credential(self, credential, id):
        existing_credential = Credential.query.filter_by(
            credential_id=id).first()
        if existing_credential is None:
            return {'message': 'Credential with id {} does not exist'.format(
                id)}, 404
        if credential is not None:
            validator = CredentialValidator()
            result = validator.validate(credential)
            if len(result) > 0:
                return {'error': result}, 400
            else:
                try:
                    existing_credential.provider_id = credential['provider_id']
                except Exception:
                    pass

                try:
                    existing_credential.credential_name = credential[
                        'credential_name']
                except Exception:
                    pass

                try:
                    existing_credential.credential_description = credential[
                        'credential_description']
                except Exception:
                    pass

                try:
                    existing_credential.credential_type_id = credential[
                        'credential_type_id']
                except Exception:
                    pass

                try:
                    existing_credential.credential_status_type = credential[
                        'credential_status_type']
                except Exception:
                    pass

                try:
                    existing_credential.audience = credential['audience']
                except Exception:
                    pass

                try:
                    existing_credential.language = credential['language']
                except Exception:
                    pass

                try:
                    existing_credential.ce_ctid = credential['ctid']
                except Exception:
                    pass

                try:
                    existing_credential.webpage = credential['webpage']
                except Exception:
                    pass

                try:
                    db.session.commit()
                    return existing_credential.to_dict(), 201
                except Exception:
                    return {'error': 'Failed to update credential.'}, 400
        else:
            return {'error': 'Request body cannot be empty.'}, 400

    def delete_credential_by_id(self, id):
        try:
            credential = Credential.query.filter_by(credential_id=id).first()
            if credential is not None:
                credential_data = credential.to_dict()
                db.session.delete(credential)
                db.session.commit()
                return credential_data, 200
            else:
                return {
                    'error': 'Credential with id {} does not exist.'.format(id)
                }, 404
        except Exception:
            return {
                'error': 'Credential with id {} does not exist.'.format(id)
            }, 404
