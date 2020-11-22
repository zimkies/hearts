from collections import namedtuple
import uuid


class Game(namedtuple('Game', ["id", "state", "players"])):
    def start(self):
        self.state = 'STARTED'

    def play(self, move):
        self.moves.append(move)

    def as_dict(self):
        return self._asdict()


GAMES = {}
class GameRepository():
    @staticmethod
    def get(id):
        return GAMES[i]

    @staticmethod
    def create():
        game = Game(id=uuid.uuid4().hex[:5], state='UNSTARTED', players=[])
        GAMES[game.id] = game
        return game
