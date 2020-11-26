from collections import namedtuple
import random
import uuid

class AIPlayer():

    def __init__(self):
        self.username = 'AI-' + uuid.uuid4().hex[:5]



class Game():
    def __init__(self, id, state='UNSTARTED', players=None, hands=None, moves=None):
        self.id = id
        self.state = state
        self.players = players or [None, None, None, None]
        self.hands = hands or {}
        self.moves = moves or []
        self.current_player = None
        self.tricks = []

    def as_dict(self):
        return {
            'id': self.id,
            'state': self.state,
            'players': self.players,
            'hands': self.hands,
            'moves': self.moves,
            'current_player': self.current_player,
        }

    def __str__(self):
        return str(self.as_dict())

    def add_player(self, player, position):
        self.players[position] = player

    def start(self):
        self.fill_empty_players()
        self.state = "STARTED"
        self.deal()

        self.current_player = self._find_starting_player()
        self.tricks.append(Trick(number=0, plays=[]))

        return self

    def fill_empty_players(self):
        for i, p in enumerate(self.players):
            if p is None:
                self.players[i] = AIPlayer().username

    def deal(self, deck=None):
        if not deck:
            deck = Deck.create_shuffled_deck()

        hands = {}
        split_hands = deck.split()
        for i, player in enumerate(self.players):
            hands[player] = split_hands[i]

        self.hands = hands


    def _find_starting_player(self):
        for k, v in self.hands.items():
            if Card.from_shorthand('2c') in v:
                return k

    def as_dict_for_player(self, player):
        attributes = self.as_dict()

        if player in attributes["hands"].keys():
            attributes["hand"] = attributes["hands"][player]
        else:
            attributes["hand"] = None

        # Don't show everyone's hands
        del attributes["hands"]

        current_trick = self.get_current_trick()
        if current_trick:
            attributes["current_trick"] = current_trick.as_dict()

        return attributes

    def get_current_trick(self):
        if not len(self.tricks):
            return None

        return self.tricks[-1]

    def _next_player(self):
        index = self.players.index(self.current_player) + 1 % 4
        return self.players[index]

    def move(self, player, card):
        # Confirm it's the player's turn.
        if self.current_player != player:
            raise ValueError("Not current player's turn")

        # make sure the card is actually in the player's hand
        if card not in self.hands[player]:
            raise ValueError("Card not in player's hand")

        # Ensure it's a valid card to play
        trick = self.get_current_trick()
        hand = self.hands[player]
        if self.is_invalid_card_for_trick(card, trick, hand):
            raise ValueError("Invalid card to play: {}".format(self.is_invalid_card_for_trick(card, trick, hand)))


        # add card to the list of visible moves.
        play = Play(player=player, card=card)
        trick.plays.append(play)

        # update state to:

        # - remove card from hand
        self.hands[player].remove(card)

        if len(trick.plays) != 4:
            self.current_player = self._next_player()

        # - if not end of trick, set new current player's turn
        #     - trigger 'next player'
        # - else if not end of round, set new trick with new starter
        # - else if not end of game:
        # -     start new round
        # - else if end of game:
        # - update game status as EOG
        # - trigger an update.

    def is_invalid_card_for_trick(self, card, trick, hand):
        # TODO: Needs to be fully implemented

        # Trick should be a list of (player, card) tuples, trick number

        # If this is the first trick and first card, must be 2c
        if trick.number == 0 and not trick.plays:
            if not (card.number == '2' and card.suit == 'c'):
                return "2 of clubs must be the first card in a hand, not {}".format(str(card))

        # TODO: if first trick, no hearts or Q of spades can be played if there are any other options
        # if trick.number == 0:


        # If this is the first card, anything goes.
        return False



class Card(namedtuple('Card', ["number", "suit"])):
    def __str__(self):
        return self.number + self.suit

    @classmethod
    def from_shorthand(cls, shorthand):
        return cls(number=shorthand[0], suit=shorthand[1])

class Trick(namedtuple('Trick', ["number", "plays"])):
    pass

    def as_dict(self):
        return {
            'number': self.number,
            'plays': self.plays
        }


class Play(namedtuple('Play', ["player", "card"])):
    pass

    def as_dict(self):
        return {
            'player': player,
            'card': card
        }



# TODO: we need a persisted non-in-memory store of games so that refreshing the
# app doesn't delete all of them :p
GAMES = {}
class GameRepository():
    @staticmethod
    def get(game_id):
        print(GAMES)
        return GAMES[game_id]

    @staticmethod
    def create():
        game = Game(id=uuid.uuid4().hex[:5], state='UNSTARTED', players=[], hands={}, moves=[])
        GAMES[game.id] = game
        print(GAMES)
        return game

class Deck:
    NUMBERS = range(1, 13)
    SUITS = ('h', 'd', 'c', 's')

    CARDS = []
    for s in SUITS:
        for n in NUMBERS:
            CARDS.append(Card(suit=s, number=str(n)))

    # CARDS = [str(n) + s for n in NUMBERS for s in SUITS]

    def __init__(self):
        self.cards =  self.CARDS[:]

    @classmethod
    def create_shuffled_deck(cls):
        deck = cls()
        deck.shuffle()
        return deck

    def shuffle(self):
        random.shuffle(self.cards)

    def split(self):
        return [
            self.cards[:13],
            self.cards[14:26],
            self.cards[27:39],
            self.cards[40:52]
        ]
