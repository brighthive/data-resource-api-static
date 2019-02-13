""" Sample Data Generator

A utility for generating sample datasets for populating the Program Outcomes
API.

"""

import os
import sys
import json
import pandas as pd


def usage():
    print('You are doing it incorrectly.')


def create_datasets(csv_file_path, skip_first_row=True):

    # datasets
    program_prerequisites = {'program_prerequisites': []}
    program_potential_outcomes = {'program_potential_outcomes': []}
    entity_types = {'entity_types': []}
    credential_types = {'credential_types': []}
    providers = {'providers': []}
    locations = {'locations': []}
    addresses = {'addresses': []}
    credentials = {'credentials': []}
    programs = {'programs': []}
    participants = {'participants': []}

    # Paths to sample data sheets
    programs_ds = os.path.join(csv_file_path, 'programs.csv')
    participants_ds = os.path.join(csv_file_path, 'participants.csv')
    credentials_ds = os.path.join(csv_file_path, 'credentials.csv')

    # Load datasheets as pandas data frames
    programs_df = pd.read_csv(programs_ds)
    participants_df = pd.read_csv(participants_ds)
    credentials_df = pd.read_csv(credentials_ds)

    # ***** Program Prerequisites (from Datasheet) *****
    program_prerequisites['program_prerequisites'] = [
        {
            'id': 0,
            'name': 'None'
        },
        {
            'id': 1,
            'name': 'High School Diploma or Equivalent'
        },
        {
            'id': 2,
            'name': 'Associate\'s Degree'
        },
        {
            'id': 3,
            'name': 'Bachelor\'s Degree'
        },
        {
            'id': 4,
            'name': 'Course(s)'
        },
        {
            'id': 5,
            'name': 'Combination of Education and Course(s)'
        }
    ]

    # ***** Program Potential Outcome (from Datasheet) *****
    program_potential_outcomes['program_potential_outcomes'] = [
        {
            'id': 1,
            'name': 'A program of study leading to an ' +
            'industry-recognized certificate or certification'
        },
        {
            'id': 2,
            'name': 'A program of study leading to a certificate ' +
            'of completion of an apprenticeship'
        },
        {
            'id': 3,
            'name': 'A program of study leading to a license recognized ' +
            'by the State involved or the Federal Government'
        },
        {
            'id': 4,
            'name': 'A program of study leading to an associate degree'
        },
        {
            'id': 5,
            'name': 'A program of study leading to a baccalaureate degree'
        },
        {
            'id': 6,
            'name': 'A program of study leading to a community college ' +
            'certificate of completion'
        },
        {
            'id': 7,
            'name': 'A program of study leading to a secondary ' +
            'school diploma or its equivalent'
        },
        {
            'id': 8,
            'name': 'A program of study leading to employment'
        },
        {
            'id': 9,
            'name': 'A program of study leading to a measureable ' +
            'skills gain leading to a credential'
        },
        {
            'id': 0,
            'name': 'A program of study leading to a measureable ' +
            'skills gain leading to employment'
        }
    ]

    # ***** Entity Type (Placeholder) *****
    entity_types['entity_types'] = [
        {
            'id': 1,
            'name': 'Educational Institution'
        }
    ]

    # ***** Credential Types *****
    credential_types['credential_types'] = credentials_df[[
        'credential_type', 'audience_level']].drop_duplicates().to_dict(
            'records')

    for idx, credential_type in enumerate(credential_types[
            'credential_types']):
        credential_type['credential_type_id'] = idx + 1

    # ***** Provider *****
    provider_names = programs_df[[
        'program_provider']].drop_duplicates().to_dict(
        'records')

    provider_details = programs_df[[
        'program_provider', 'program_address', 'program_description',
        'program_contact_email',
        'program_url', 'geographic_areas']].drop_duplicates().to_dict(
        'records')

    provider_locations = programs_df[[
        'program_provider', 'geographic_areas']].drop_duplicates().to_dict(
        'records')

    provider_states = programs_df[['geographic_areas']
                                  ].drop_duplicates().to_dict('records')

    # construct the initial list of providers
    for idx, provider in enumerate(provider_names):
        provider = {
            'provider_id': idx + 1,
            'provider_name': provider['program_provider'],
            'provider_alternate_name': provider['program_provider'],
            'entity_type_id': 1,
            'provider_full_address': '',
            'provider_description': 'An education provider',
            'provider_contact_email': '',
            'provider_url': '',
            'year_incorporated': 2019
        }
        providers['providers'].append(provider)

    # capture the additional information from the provider
    for idx, provider in enumerate(providers['providers']):
        for provider_detail in provider_details:
            if provider_detail['program_provider'] == provider[
                    'provider_name']:
                provider['provider_full_address'] = provider_detail[
                    'program_address']
                provider['provider_contact_email'] = provider_detail[
                    'program_contact_email']
                provider['provider_url'] = provider_detail['program_url']
                break

    # ***** Geographic Location *****
    for idx, provider_detail in enumerate(provider_details):
        location = {
            'location_id': idx + 1,
            'location_name': provider_detail['program_provider'],
            'provider_id': 0,
            'location_description': 'A location in the United States',
            'transportation': 'Automobile, Bus, Walk',
            'latitude': 39.629,
            'longitude': -79.955,
            'location_full_address': '{}, {}'.format(
                provider_detail['program_address'],
                provider_detail['geographic_areas'])
        }
        for provider in providers['providers']:
            if provider['provider_name'] == location['location_name']:
                location['provider_id'] = provider['provider_id']
        locations['locations'].append(location)

    # ***** Physical Address *****
    for idx, location in enumerate(locations['locations']):
        address = {
            'address_id': idx + 1,
            'location_id': location['location_id'],
            'address': location['location_full_address'].split(',')[0].strip(),
            'city': 'Some City',
            'state': location['location_full_address'].split(',')[1].strip(),
            'postal_code': '12345',
            'country': 'US'
        }
        addresses['addresses'].append(address)

    # ***** Credentials *****
    credential_providers = credentials_df[[
        'program_provider', 'program_code', 'credential_name',
        'credential_description', 'credential_type',
        'credential_status_type', 'audience', 'audience_level', 'language',
        'ctid', 'webpage']
    ].drop_duplicates().to_dict('records')

    for idx, credential_provider in enumerate(credential_providers):
        credential = {
            'credential_id': idx + 1,
            'provider_id': '',
            'credential_name': credential_provider['credential_name'],
            'credential_description': credential_provider[
                'credential_description'],
            'credential_type_id': '',
            'credential_status_type': credential_provider[
                'credential_status_type'],
            'audience': credential_provider['audience'],
            'language': credential_provider['language'],
            'ce_ctid': credential_provider['ctid'],
            'webpage': credential_provider['webpage']
        }
        # find the provider ids
        for provider in providers['providers']:
            if provider['provider_name'].strip() == credential_provider[
                    'program_provider'].strip():
                credential['provider_id'] = provider['provider_id']
                break

        # find the credential type id
        for credential_type in credential_types['credential_types']:
            if credential_provider['credential_type'] == \
                    credential_type['credential_type'] and \
                    credential_provider['audience_level'] == \
                    credential_type['audience_level']:
                credential['credential_type_id'] = credential_type[
                    'credential_type_id']
                break
        credentials['credentials'].append(credential)

    # ***** Programs *****

    program_details = programs_df[[
        'program_provider',
        'program_name',
        'program_code',
        'program_description',
        'program_status',
        'program_fees',
        'geographic_areas',
        'program_address',
        'eligibility_criteria',
        'credential_earned',
        'program_potential_outcome',
        'program_url',
        'program_contact_phone',
        'program_contact_email',
        'languages',
        'current_intake_capacity',
        'program_offering_model',
        'program_length_hours',
        'program_length_weeks',
        'prerequisites',
        'program_soc',
        'funding_sources',
        'on_etpl'
    ]].drop_duplicates().to_dict(
        'records')

    for idx, program_detail in enumerate(program_details):
        program = {
            'program_id': idx + 1,
            'program_name': program_detail['program_name'],
            'program_code': program_detail['program_code'],
            'program_description': program_detail['program_description'],
            'program_status': program_detail['program_status'],
            'program_fees': program_detail['program_fees'],
            'provider_id': '',
            'location_id': '',
            'eligibility_criteria': program_detail['eligibility_criteria'],
            'credential_earned': program_detail['credential_earned'],
            'potential_outcome_id': program_detail[
                'program_potential_outcome'],
            'program_url': program_detail['program_url'],
            'program_contact_phone': program_detail['program_contact_phone'],
            'program_contact_email': program_detail['program_contact_email'],
            'languages': program_detail['languages'],
            'current_intake_capacity': program_detail[
                'current_intake_capacity'],
            'program_offering_model': program_detail[
                'program_offering_model'],
            'program_length_hours': program_detail['program_length_hours'],
            'program_length_weeks': program_detail['program_length_weeks'],
            'prerequisite_id': program_detail['prerequisites'],
            'program_soc': program_detail['program_soc'],
            'funding_sources': program_detail['funding_sources'],
            'on_etpl': program_detail['on_etpl'],
            'cost_of_books_and_supplies': 0.00
        }

        # find provider id
        for provider in providers['providers']:
            if provider['provider_name'] == program_detail['program_provider']:
                program['provider_id'] = provider['provider_id']
                break

        # find location id
        for address in addresses['addresses']:
            if address['state'] == program_detail['geographic_areas'] \
                and address['address'] == \
                    program_detail['program_address']:
                program['location_id'] = address['location_id']
                break

        programs['programs'].append(program)
    # print(programs)

    # ***** Participants *****
    participant_details = participants_df.to_dict('records')
    for participant_detail in participant_details:
        participant = {
            'participant_id': participant_detail['participant_id'],
            'program_id': '',
            'entry_date': participant_detail['entry_date'],
            'exit_date': participant_detail['exit_date'],
            'exit_type': participant_detail['exit_type'],
            'exit_reason': participant_detail['exit_type']
        }

        # find program id
        for provider in providers['providers']:
            if provider['provider_name'] == participant_detail[
                    'program_provider']:
                provider_id = provider['provider_id']
                for program in programs['programs']:
                    if program['provider_id'] == provider_id:
                        participant['program_id'] = program['program_id']
                        break
        participants['participants'].append(participant)

    # Write out datasets to JSON files
    # program_prerequisites = {'program_prerequisites': []}
    # program_potential_outcomes = {'program_potential_outcomes': []}
    # entity_types = {'entity_types': []}
    # credential_types = {'credential_types': []}
    # providers = {'providers': []}
    # locations = {'locations': []}
    # addresses = {'addresses': []}
    # credentials = {'credentials': []}
    # programs = {'programs': []}
    # participants = {'participants': []}

    # output files
    program_prerequisites_outfile = os.path.join(
        csv_file_path, 'program_prerequisites.json')
    program_potential_outcomes_outfile = os.path.join(
        csv_file_path, 'program_potential_outcomes.json')
    entity_types_outfile = os.path.join(csv_file_path, 'entity_types.json')
    credential_types_outfile = os.path.join(
        csv_file_path, 'credential_types.json')
    providers_outfile = os.path.join(csv_file_path, 'providers.json')
    locations_outfile = os.path.join(csv_file_path, 'locations.json')
    addresses_outfile = os.path.join(csv_file_path, 'addresses.json')
    credentials_outfile = os.path.join(csv_file_path, 'credentials.json')
    programs_outfile = os.path.join(csv_file_path, 'programs.json')
    participants_outfile = os.path.join(csv_file_path, 'participants.json')

    with open(program_prerequisites_outfile, 'w') as f:
        json.dump(program_prerequisites, f, indent=4)

    with open(program_potential_outcomes_outfile, 'w') as f:
        json.dump(program_potential_outcomes, f, indent=4)

    with open(entity_types_outfile, 'w') as f:
        json.dump(entity_types, f, indent=4)

    with open(credential_types_outfile, 'w') as f:
        json.dump(credential_types, f, indent=4)

    with open(providers_outfile, 'w') as f:
        json.dump(providers, f, indent=4)

    with open(locations_outfile, 'w') as f:
        json.dump(locations, f, indent=4)

    with open(addresses_outfile, 'w') as f:
        json.dump(addresses, f, indent=4)

    with open(credentials_outfile, 'w') as f:
        json.dump(credentials, f, indent=4)

    with open(programs_outfile, 'w') as f:
        json.dump(programs, f, indent=4)

    with open(participants_outfile, 'w') as f:
        json.dump(participants, f, indent=4)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
    else:
        print('Invalid number of arguments specified')
        usage()
        sys.exit(1)

    if os.path.exists(file_path) and os.path.isdir(file_path):
        create_datasets(file_path)
    else:
        print('Invalid directory specified: {}'.format(file_path))
        usage()
        sys.exit(1)
