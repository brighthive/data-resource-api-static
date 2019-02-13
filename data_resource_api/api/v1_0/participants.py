""" API Version 1.0 Participants Handler """

from data_resource_api.db import Participant


class ParticipantsHandler(object):
    def get_all_participants(self):
        results = Participant.query.all()
        participants = {'participants': []}
        for participant in results:
            participants['participants'].append(participant.to_dict())
        return participants

    def add_new_participant(self, participant):
        if participant is not None:
            return {'message': 'added a new participant'}, 201
        else:
            return {'message': 'request body cannot be empty'}, 400
