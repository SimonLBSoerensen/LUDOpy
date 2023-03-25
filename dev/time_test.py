import ludopy
import numpy as np
import time


def make_time_test():
    g = ludopy.Game()
    there_is_a_winner = False

    n_moves = 0
    start_time = time.time()
    while not there_is_a_winner:
        (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner,
         there_is_a_winner), player_i = g.get_observation()

        if len(move_pieces):
            piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
        else:
            piece_to_move = -1

        _, _, _, _, _, there_is_a_winner = g.answer_observation(piece_to_move)
        n_moves += 1
    end_time = time.time()
    used_time = end_time - start_time
    moves_per_sec = n_moves / used_time
    return moves_per_sec


n = 100

times = []
for _ in range(n):
    moves_per_sec = make_time_test()
    times.append(moves_per_sec)

print("Mean moves per sec over", n, "times")
print(np.mean(times))
