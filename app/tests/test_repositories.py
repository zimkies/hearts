from app.repositories import Game, Card, Trick, Play, Deck
import unittest
import uuid


class TestGame(unittest.TestCase):
    def _create_game(self):
        game = Game(
            id=uuid.uuid4().hex[:5],
            state="STARTED",
            players=["ben", "ada", "michael", "pule"],
            hands={},
            moves=[],
        )

        game.start()

        unshuffled_deck = Deck()

        game.deal(unshuffled_deck)
        game.current_player = game._find_starting_player()

        return game

    def test_move(self):
        game = self._create_game()

        starting_player = game._find_starting_player()
        self.assertEqual(starting_player, "michael")

        card = Card.from_shorthand("2c")
        game.move(starting_player, card=card)

        self.assertEqual(game.tricks, [Trick(0, [Play(starting_player, card)])])

        self.assertTrue(card not in game.hands[starting_player])

        self.assertEqual(game.current_player, "pule")

    def test_starting_game_fills_empty_players(self):
        game = Game(id=uuid.uuid4().hex[:5], players=["ben", None, None, None])

        self.assertEqual(game.players, ["ben", None, None, None])

        game.start()

        self.assertEqual(len(game.players), 4)
        for i, p in enumerate(game.players):
            if i != 0:
                self.assertTrue("AI-" in p)
            else:
                self.assertEqual(p, "ben")


    def test_move_at_end_of_trick(self):
        game = self._create_game()

        starting_player = game._find_starting_player()
        self.assertEqual(starting_player, "michael")

        game.move("michael", Card.from_shorthand("2c"))
        game.move("pule", Card.from_shorthand("2s"))
        game.move("ben", Card.from_shorthand("2h"))
        game.move("ada", card=Card.from_shorthand("2d"))

        self.assertEqual(game.current_player, "michael")

        self.assertEqual(game.tricks, [
            Trick(0, [
                Play("michael", Card.from_shorthand("2c")),
                Play("pule", Card.from_shorthand("2s")),
                Play("ben", Card.from_shorthand("2h")),
                Play("ada", Card.from_shorthand("2d")),
            ]),
            Trick(1, [
            ])
        ])


class TestTrick(unittest.TestCase):
    def test_get_winner_of_trick(self):
        trick = Trick(0, plays=[
            Play("michael", Card.from_shorthand("2c")),
            Play("pule", Card.from_shorthand("2s")),
            Play("ben", Card.from_shorthand("2h")),
            Play("ada", Card.from_shorthand("2d")),
        ])

        self.assertEqual(
            trick.get_winner_of_trick(),
            Play("michael", Card.from_shorthand("2c")),
            )
