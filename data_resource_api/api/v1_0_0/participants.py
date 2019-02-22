""" API Version 1.0 Participants Handler """

from data_resource_api.db import Participant
from data_resource_api.validator import ParticipantValidator
from data_resource_api.app.app import db


class ParticipantsHandler(object):
    def get_all_participants(self):
        results = Participant.query.all()
        participants = {'participants': []}
        for participant in results:
            participants['participants'].append(participant.to_dict())
        return participants

    def add_new_participant(self, participant):
        if participant is not None:
            validator = ParticipantValidator()
            result = validator.validate(participant)
            if len(result) > 0:
                return {'error': result}, 400
            else:
                if participant['participant_id'] is None:
                    return {'error': 'Participant id must be provided.'}, 400
                new_participant = Participant(
                    program_id=participant['program_id'],
                    entry_date=participant['entry_date'],
                    exit_date=participant['exit_date'],
                    exit_type=participant['exit_type'],
                    exit_reason=participant['exit_type'],
                    id=participant['participant_id'])
                try:
                    db.session.add(new_participant)
                    db.session.commit()
                    return new_participant.to_dict(), 201
                except Exception:
                    return {'error': 'Failed to create new participant, most'
                            + 'likely because of a duplicate participant id.'
                            }, 400
        else:
            return {'error': 'Request body cannot be empty'}, 400

    def get_participant_by_id(self, id):
        try:
            participant = Participant.query.filter_by(
                participant_id=id).first()
            if participant is not None:
                return participant.to_dict(), 200
            else:
                return {
                    'error': 'Participant with id {} does not exist.'.format(
                        id)}, 404
        except Exception:
            return {'error': 'Invalid request.'}, 400

    def update_participant(self, participant, id):
        existing_participant = Participant.query.filter_by(
            participant_id=id).first()
        if existing_participant is None:
            return {'message': 'Participant with id {} does not exist'.format(
                id)}, 404
        if participant is not None:
            validator = ParticipantValidator()
            result = validator.validate(participant)
            if len(result) > 0:
                return {'error': result}, 400
            else:
                try:
                    existing_participant.program_id = participant['program_id']
                except Exception:
                    pass

                try:
                    existing_participant.entry_date = participant['entry_date']
                except Exception:
                    pass

                try:
                    existing_participant.exit_date = participant['exit_date']
                except Exception:
                    pass

                try:
                    existing_participant.exit_type = participant['exit_type']
                except Exception:
                    pass

                try:
                    db.session.commit()
                    return existing_participant.to_dict(), 201
                except Exception:
                    return {'error': 'Failed to update participant.'}, 400
        else:
            return {'error': 'Request body cannot be empty.'}, 400

    def delete_participant_by_id(self, id):
        try:
            participant = Participant.query.filter_by(
                participant_id=id).first()
            if participant is not None:
                participant_data = participant.to_dict()
                db.session.delete(participant)
                db.session.commit()
                return participant_data, 200
            else:
                return {
                    'error': 'Participant with id {} does not exist.'.format(
                        id)
                }, 404
        except Exception:
            return {
                'error': 'Participant with id {} does not exist.'.format(id)
            }, 404
