import time
import unittest
import sys

sys.path.append("../")


def randwalk():
    import ludopy
    import numpy as np

    g = ludopy.Game()
    there_is_a_winner = False

    n_moves = 0
    start_time = time.perf_counter_ns()
    while not there_is_a_winner:
        (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner,
         there_is_a_winner), player_i = g.get_observation()

        if len(move_pieces):
            piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
        else:
            piece_to_move = -1

        _, _, _, _, _, there_is_a_winner = g.answer_observation(piece_to_move)
        n_moves += 1
    end_time = time.perf_counter_ns()
    used_time = (end_time - start_time) * 1e-9
    moves_per_sec = n_moves / used_time
    print("Moves per sec:", moves_per_sec)

    print("Saving history to numpy file")
    g.save_hist("game_history.npy")
    print("Saving game video")
    g.save_hist_video("game_video.mp4")

    return True


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, randwalk())


if __name__ == '__main__':
    unittest.main()
