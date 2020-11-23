from collections import namedtuple
import random
import uuid


class Game(namedtuple('Game', ["id", "state", "players", "hands"])):
    def as_dict(self):
        return self._asdict()

    def add_player(self, player):
        self.players.append(player)

    def as_dict_for_player(self, player):
        attributes = self._asdict()

        if player in attributes["hands"].keys():
            attributes["hand"] = attributes["hands"][player]
        else:
            attributes["hand"] = None

        # Don't show everyone's hands
        del attributes["hands"]

        return attributes
        # attributes["hand"] =
        # del attributes.hands



# TODO: we need a persisted non-in-memory store of games so that refreshing the
# app doesn't delete all of them :p
GAMES = {}
class GameRepository():
    @staticmethod
    def get(game_id):
        print(GAMES)
        return GAMES[game_id]

    @classmethod
    def start(cls, game_id):
        game_json = GAMES[game_id].as_dict()
        game_json["state"] = "STARTED"
        deck = Deck()
        hands = {}
        split_hands = deck.split()
        for i, player in enumerate(game_json["players"]):
            hands[player] = split_hands[i]

        game_json["hands"] = hands
        GAMES[game_id] = Game(**game_json)
        return GAMES[game_id]

    @staticmethod
    def create():
        game = Game(id=uuid.uuid4().hex[:5], state='UNSTARTED', players=[], hands={})
        GAMES[game.id] = game
        print(GAMES)
        return game


class Deck:
    NUMBERS = range(1, 13)
    SUITS = ('h', 'd', 'c', 's')

    CARDS = [str(n) + s for n, s in zip(NUMBERS, SUITS)]

    def __init__(self):
        self.cards =  self.CARDS[:]
        random.shuffle(self.cards)

    def split(self):
        return [
            self.cards[:13],
            self.cards[14:26],
            self.cards[27:39],
            self.cards[40:52]
        ]
