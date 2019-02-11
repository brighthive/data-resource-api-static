""" API Version 1.0 Participants Handler """

from db import Participant


class ParticipantsHandler(object):
    def get_all_participants(self):
        return {'message': 'participants api version 1.0'}

    def add_new_participant(self, participant):
        if participant is not None:
            return {'message': 'added a new participant'}, 201
        else:
            return {'message': 'request body cannot be empty'}, 400
