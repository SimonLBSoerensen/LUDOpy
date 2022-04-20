import cv2

import ludopy
from ludopy.player import GOAL_INDEX
import numpy as np

g = ludopy.Game()
there_is_a_winner = False

i = 0
target_n_in_goal = 2
players_in_goal = []
player_for_fill = 1

while len(players_in_goal) < player_for_fill:
    (dice, move_pieces, player_pieces, enemy_pieces,
     player_is_a_winner, there_is_a_winner), player_i = g.get_observation()

    n_in_goal = 0
    for p in player_pieces:
        if p == GOAL_INDEX:
            n_in_goal += 1

    if n_in_goal == target_n_in_goal and player_i not in players_in_goal:
        players_in_goal.append(player_i)

    if len(move_pieces):
        piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
    else:
        piece_to_move = -1

    _, _, _, _, _, there_is_a_winner = g.answer_observation(piece_to_move)

    if i == 0:
        board = g.render_environment()
        cv2.imwrite("board_example.png", cv2.cvtColor(board, cv2.COLOR_RGB2BGR))
    i += 1

board = g.render_environment()
cv2.imwrite("board_example_2.png", cv2.cvtColor(board, cv2.COLOR_RGB2BGR))
