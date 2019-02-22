""" API Version 1.0 Providers Handler """

from data_resource_api.db import Provider
from data_resource_api.validator import ProviderValidator
from data_resource_api.app.app import db


class ProvidersHandler(object):
    def get_all_providers(self):
        results = Provider.query.all()
        providers = {'providers': []}
        for provider in results:
            providers['providers'].append(provider.to_dict())
        return providers, 200

    def add_new_provider(self, provider):
        if provider is not None:
            validator = ProviderValidator()
            result = validator.validate(provider)
            if len(result) > 0:
                return {'error': result}, 400
            else:
                new_provider = Provider(
                    name=provider['provider_name'],
                    entity_type_id=provider['entity_type_id'],
                    alternate_name=provider['provider_alternate_name'],
                    full_address=provider['provider_full_address'],
                    description=provider['provider_description'],
                    contact_email=provider['provider_contact_email'],
                    url=provider['provider_url'],
                    incorporated=provider['year_incorporated'])

                try:
                    db.session.add(new_provider)
                    db.session.commit()
                    return new_provider.to_dict(), 201
                except Exception as e:
                    print(e)
                    return {'error': 'Failed to create new provider.'}, 400
        else:
            return {'error': 'Request body cannot be empty'}, 400

    def get_provider_by_id(self, id):
        try:
            provider = Provider.query.filter_by(provider_id=id).first()
            if provider is not None:
                return provider.to_dict(), 200
            else:
                return {'error': 'Provider with id {} does not exist.'.format(
                    id)}, 404
        except Exception:
            return {'error': 'Invalid request.'}, 400

    def update_provider(self, provider, id):
        existing_provider = Provider.query.filter_by(provider_id=id).first()
        if existing_provider is None:
            return {'message': 'Provider with id {} does not exist'.format(
                id)}, 404
        if provider is not None:
            validator = ProviderValidator()
            result = validator.validate(provider)
            if len(result) > 0:
                return {'error': result}, 400
            else:
                try:
                    existing_provider.entity_type_id = provider[
                        'entity_type_id']
                except Exception:
                    pass

                try:
                    existing_provider.provider_name = provider[
                        'provider_name']
                except Exception:
                    pass

                try:
                    existing_provider.provider_alternate_name = provider[
                        'provider_alternate_name']
                except Exception:
                    pass

                try:
                    existing_provider.provider_full_address = provider[
                        'provider_full_address']
                except Exception:
                    pass

                try:
                    existing_provider.provider_description = provider[
                        'provider_description']
                except Exception:
                    pass

                try:
                    existing_provider.provider_contact_email = provider[
                        'provider_contact_email']
                except Exception:
                    pass

                try:
                    existing_provider.url = provider[
                        'provider_url']
                except Exception:
                    pass

                try:
                    existing_provider.year_incorporated = provider[
                        'year_incorporated']
                except Exception:
                    pass

                try:
                    db.session.commit()
                    return existing_provider.to_dict(), 201
                except Exception:
                    return {'error': 'Failed to update provider.'}, 400
        else:
            return {'error': 'Request body cannot be empty.'}, 400

    def delete_provider_by_id(self, id):
        try:
            provider = Provider.query.filter_by(provider_id=id).first()
            if provider is not None:
                provider_data = provider.to_dict()
                db.session.delete(provider)
                db.session.commit()
                return provider_data, 200
            else:
                return {
                    'error': 'Provider with id {} does not exist.'.format(id)
                }, 404
        except Exception:
            return {
                'error': 'Provider with id {} does not exist.'.format(id)}, 404

    def get_programs_by_provider(self, id):
        try:
            provider = Provider.query.filter_by(provider_id=id).first()
            if provider is not None:
                response = {
                    'provider_id': provider.provider_id,
                    'provider_name': provider.provider_name,
                    'provider_alternate_name':
                    provider.provider_alternate_name,
                    'programs': []
                }
                for program in provider.programs:
                    response['programs'].append(program.to_dict())
                return response, 200
            else:
                return {
                    'error': 'Provider with id {} does not exist.'.format(id)
                }, 404
        except Exception:
            return {
                'error': 'Unable to access resource {}.'.format(id)}, 400
        print('Getting programs by provider {}'.format(id))
