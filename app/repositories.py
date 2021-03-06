from collections import namedtuple, defaultdict
import random
import uuid


class AIPlayer:
    def __init__(self, username=None):
        if not username:
            username = "AI-" + uuid.uuid4().hex[:5]

        self.username = username

    def make_move(self, hand, trick):

        # TODO: make this actually follow the rules
        # If first trick, first hand, play 2clubs
        if trick.number == 0 and not trick.plays:
            return Card.from_shorthand("2c")

        # if first play of trick, play non heart/Qs
        # if
        # otherwise, follow suit,
        # otherwise play non heart

        return random.choice(hand)


def is_ai(player):
    return "AI-" in player


class Game:
    SCORE_TO_WIN = 100

    def __init__(
        self,
        id,
        state="UNSTARTED",
        players=None,
        hands=None,
        moves=None,
        deck_class=None,
    ):
        self.id = id
        self.state = state
        self.players = players or [None, None, None, None]
        self.hands = hands or {}
        self.moves = moves or []
        self.current_player = None
        self.tricks = []
        self.score_history = defaultdict(list)
        self.deck_class = deck_class or Deck

        self.round_number = None
        self.rounds = []

    def as_dict(self):
        return {
            "id": self.id,
            "state": self.state,
            "players": self.players,
            "hands": self.hands,
            "moves": self.moves,
            "current_player": self.current_player,
            "score_history": self.score_history,
        }

    def __str__(self):
        return str(self.as_dict())

    def add_player(self, player, position):
        self.players[position] = player

    def start(self):
        self.fill_empty_players()
        self.state = "STARTED"
        self.start_round()

        return self

    def start_round(self):
        if self.round_number is None:
            self.round_number = 0
        else:
            self.round_number += 1

        self.deal()
        self.current_player = self._find_starting_player()
        self.rounds.append(self.tricks)

        # Reset tricks for this round
        self.tricks = [Trick(number=0, plays=[])]
        self.make_ai_moves()

    def fill_empty_players(self):
        for i, p in enumerate(self.players):
            if p is None:
                self.players[i] = AIPlayer().username

    def deal(self, deck=None):
        if not deck:
            deck = self.deck_class.create_shuffled_deck()

        hands = {}
        split_hands = deck.split()
        for i, player in enumerate(self.players):
            hands[player] = split_hands[i]

        self.hands = hands

    def _find_starting_player(self):
        for k, v in self.hands.items():
            if Card.from_shorthand("2c") in v:
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
        index = (self.players.index(self.current_player) + 1) % 4
        return self.players[index]

    def make_ai_moves(self):
        while is_ai(self.current_player):
            card_to_play = AIPlayer(self.current_player).make_move(
                hand=self.hands[self.current_player], trick=self.get_current_trick()
            )

            self._move(self.current_player, card_to_play)

    def move(self, player, card):
        self._move(player, card)

        self.make_ai_moves()

    def _move(self, player, card):
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
            raise ValueError(
                "Invalid card to play: {}".format(
                    self.is_invalid_card_for_trick(card, trick, hand)
                )
            )

        # add card to the list of visible moves.
        play = Play(player=player, card=card)
        trick.plays.append(play)

        # update state to:

        # - remove card from hand
        self.hands[player].remove(card)

        # Continue trick
        if len(trick.plays) < 4:
            self.current_player = self._next_player()
            return

        # get winner of trick:
        winning_play = trick.get_winner_of_trick()
        if trick.number < 12:  # 0-based indexing
            # Got to next trick
            self._start_next_trick()
            self.current_player = winning_play.player

        # End of round!
        else:
            # Tally up tricks in round, add scores, and end round
            scores = Round(tricks=self.tricks).calculate_scores()
            for player, score in scores.items():
                self.score_history[player].append(score)

            self.current_player = None

            # If scores are under the max score, start a new round
            if max(self.tally_scores().values()) < self.SCORE_TO_WIN:
                self.start_round()

            # Game is over
            else:
                self.end_game()

        # - if not end of trick, set new current player's turn
        #     - trigger 'next player'
        # - else if not end of round, set new trick with new starter
        # - else if not end of game:
        # -     start new round
        # - else if end of game:
        # - update game status as EOG
        # - trigger an update.

    def end_game(self):
        self.state = "ENDED"
        self.current_player = None

    def tally_scores(self) -> dict:
        scores = {}
        for player, score_history in self.score_history.items():
            scores[player] = sum(score_history)

        return scores

    def _start_next_trick(self):
        trick = self.get_current_trick()
        self.tricks.append(Trick(number=trick.number + 1, plays=[]))

    def is_invalid_card_for_trick(self, card, trick, hand):
        # TODO: Needs to be fully implemented

        # Trick should be a list of (player, card) tuples, trick number

        # If this is the first trick and first card, must be 2c
        if trick.number == 0 and not trick.plays:
            if not (card.number == "2" and card.suit == "c"):
                return "2 of clubs must be the first card in a hand, not {}".format(
                    str(card)
                )

        # TODO: if first trick, no hearts or Q of spades can be played if there are any other options
        # if trick.number == 0:

        # If this is the first card, anything goes.
        return False


class Card(namedtuple("Card", ["number", "suit"])):
    def __str__(self):
        return self.number + self.suit

    @classmethod
    def from_shorthand(cls, shorthand):
        return cls(number=shorthand[:-1], suit=shorthand[-1])

    def get_value(self):
        if str(self) == "12c":  # Queen of clubs
            return 13
        elif self.suit == "h":  # hearts
            return 1
        else:
            return 0


class Trick(namedtuple("Trick", ["number", "plays"])):
    pass

    def as_dict(self):
        return {"number": self.number, "plays": [p.as_dict() for p in self.plays]}

    def get_winner_of_trick(self):
        if len(self.plays) < 4:
            raise ValueError("trick isn't finished yet, no winner")

        winning_suit = self.plays[0].card.suit
        winner = self.plays[0]

        for play in self.plays:
            # TODO: Fix ordering for Aces
            if play.card.suit == winning_suit and play.card.number > winner.card.number:
                winner = play

        return winner


class Round(namedtuple("Round", ["tricks"])):
    def calculate_scores(self):
        # initialize players to ensure everyone has a score
        scores = defaultdict(int)
        for play in self.tricks[0].plays:
            scores[play.player] = 0

        # sum up scores for all tricks
        for trick in self.tricks:
            winning_play = trick.get_winner_of_trick()
            for play in trick.plays:
                scores[winning_play.player] += play.card.get_value()

        # account for shooting the moon
        moonshooters = [p for p, s in scores.items() if s == 26]
        if len(moonshooters) > 0:
            moonshooter = moonshooters[0]
            for player in scores.keys():
                if player == moonshooter:
                    scores[player] = 0
                else:
                    scores[player] = 26

        return scores


class Play(namedtuple("Play", ["player", "card"])):
    pass

    def as_dict(self):
        return {"player": self.player, "card": self.card}


# TODO: we need a persisted non-in-memory store of games so that refreshing the
# app doesn't delete all of them :p
GAMES = {}


class GameRepository:
    @staticmethod
    def get(game_id):
        print(GAMES)
        return GAMES[game_id]

    @staticmethod
    def create():
        game = Game(
            id=uuid.uuid4().hex[:5], state="UNSTARTED", players=[], hands={}, moves=[]
        )
        GAMES[game.id] = game
        print(GAMES)
        return game


class Deck:
    NUMBERS = range(1, 14)
    SUITS = ("h", "d", "c", "s")

    CARDS = []
    for s in SUITS:
        for n in NUMBERS:
            CARDS.append(Card(suit=s, number=str(n)))

    def __init__(self):
        self.cards = self.CARDS[:]

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
            self.cards[13:26],
            self.cards[26:39],
            self.cards[39:52],
        ]


class TestingDeck(Deck):
    """
    A special type of deck that doesn't shuffle cards even when you ask it to.
    Useful for testing, because it always returns the same order of cards.
    """

    def shuffle(self):
        pass
