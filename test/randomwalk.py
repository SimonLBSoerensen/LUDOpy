import unittest


def randwalk():
    import ludopy
    import numpy as np
    from tqdm import tqdm

    g = ludopy.Game()
    there_is_a_winner = False

    while not there_is_a_winner:
        (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner,
         there_is_a_winner), player_i = g.get_observation()

        if len(move_pieces):
            piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
        else:
            piece_to_move = -1

        _, _, _, _, _, there_is_a_winner = g.answer_observation(piece_to_move)
    return True


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, randwalk())


if __name__ == '__main__':
    unittest.main()
