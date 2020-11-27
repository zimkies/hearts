from app.repositories import Game, Card, Trick, Play, Deck, Round, TestingDeck
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
            deck_class=TestingDeck
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

    def test_move_at_end_of_round(self):
        game = self._create_game()

        starting_player = game._find_starting_player()
        self.assertEqual(starting_player, "michael")

        # Play all 13 tricks
        for i in range(13):
            number = ((i + 1) % 13) + 1


            game.move("michael", Card.from_shorthand(f'{number}c'))
            game.move("pule", Card.from_shorthand(f'{number}s'))
            game.move("ben", Card.from_shorthand(f'{number}h'))
            game.move("ada", Card.from_shorthand(f'{number}d'))

        # Current Player gets reset to Michael in the new round
        self.assertEqual(game.current_player, 'michael')
        self.assertEqual(game.round_number, 1)

        for i in range(13):
            number = ((i + 1) % 13) + 1
            self.assertEqual(game.rounds[-1][i],
                Trick(i, [
                    Play("michael", Card.from_shorthand(f'{number}c')),
                    Play("pule", Card.from_shorthand(f'{number}s')),
                    Play("ben", Card.from_shorthand(f'{number}h')),
                    Play("ada", Card.from_shorthand(f'{number}d')),
                ])
        )


        self.assertEqual(game.tricks, [Trick(0, [])])


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


class TestRound(unittest.TestCase):
    def test_calculate_scores(self):
        # Play all 13 tricks
        tricks = []
        for i in range(13):
           number = ((i + 1) % 13) + 1

           trick = Trick(i, [
               Play("michael", Card.from_shorthand(f'{number}c')),
               Play("pule", Card.from_shorthand(f'{number}s')),
               Play("ben", Card.from_shorthand(f'{number}h')),
               Play("ada", Card.from_shorthand(f'{number}d'))
           ])

           tricks.append(trick)

        self.assertEqual(
            Round(tricks=tricks).calculate_scores(),
            {
                "michael": 0,
                "pule": 26,
                "ben": 26,
                "ada": 26,

            }
        )
