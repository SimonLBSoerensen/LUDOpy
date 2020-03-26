from .player import Player
from .visualizer import make_img_of_board, save_hist_video
import numpy as np
from tqdm import tqdm


class Game:
    def __init__(self):
        self.reset()
        self.enemys_order = {
            0: [1, 2, 3],
            1: [2, 3, 0],
            2: [3, 0, 1],
            3: [0, 1, 2]
        }
        self.round = 1
        self.current_player = 0
        self.first_winner_was = -1
        self.current_dice = -1
        self.observation_pending = False
        self.current_move_pieces = []
        self.current_enemys = []
        self.current_start_attempts = 0

    def __dice_generator(self):
        self.current_dice = np.random.randint(1, 6 + 1)

    def __add_to_hist(self):
        pieces = [p.get_pieces() for p in self.players]
        self.hist.append([pieces, self.current_dice, self.current_player+1, self.round])

    def reset(self):
        self.players = [Player(), Player(), Player(), Player()]
        self.hist = []

    def __gen_observation(self, player_idx):
        # Roll the dice
        self.__dice_generator()
        dice = self.current_dice

        player = self.players[player_idx]
        # Get the pieces there can be moved with the current dice
        move_pieces = player.get_pieces_that_can_move(dice)
        self.current_move_pieces = move_pieces
        # Get where the players piece are
        player_pieces = player.get_pieces()
        # Get where the enemy's piece are
        enemy_pieces = [self.players[e].get_pieces() for e in self.enemys_order[player_idx]]
        self.current_enemys = enemy_pieces
        # Check if the player is a winner
        player_is_a_winner = player.player_winner()
        # Check if there is a winner
        there_is_a_winner = any([p.player_winner() for p in self.players])
        return dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner

    def __set_enemy_pieces(self, player_idx, enemy_pieces):
        # Go throng the enemy's and set the changes in there piece
        for e_i, e in enumerate(self.enemys_order[player_idx]):
            self.players[e].set_pieces(enemy_pieces[e_i])

    def get_observation(self):
        """

        :return: (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), current_player
        """
        # Check if there is a observation pending
        if self.observation_pending:
            raise RuntimeError("There is already a pending observation. "
                               "The pending observation has to be answered first")
        # Set pending observation to true
        self.observation_pending = True
        # Get the current en environment
        obs = self.__gen_observation(self.current_player)

        # Add the bord and dice before the move to the history
        self.__add_to_hist()
        return obs, self.current_player + 1

    def __count_player(self):
        # Count up the player
        self.current_player += 1
        # If the count is over 3 then reset to player 0 and count up the round
        if self.current_player > 3:
            self.current_player = 0
            self.round += 1

    def answer_observation(self, piece_to_move):
        """

        :return: dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner
        """
        # Check if there is a observation pending
        if not self.observation_pending:
            raise RuntimeError("There is no pending observation. "
                               "There has to be a pending observation has to be answered first")
        # Check if the given piece_to_move is among the current_move_pieces
        if len(self.current_move_pieces) and piece_to_move not in self.current_move_pieces:
            raise RuntimeError("The piece given has to be among the given move_pieces")
        # If it is then move the piece
        elif len(self.current_move_pieces):
            new_enemys = self.players[self.current_player].move_piece(piece_to_move,
                                                                      self.current_dice, self.current_enemys)
            self.__set_enemy_pieces(self.current_player, new_enemys)
        # If there was no pieces there could be moved then nothing can be done
        else:
            pass # This line is present for readability

        # Check if the player now is the winner
        if self.first_winner_was != -1 and self.players[self.current_player].player_winner():
            self.first_winner_was = self.current_player

        # Add the bord after the move to the history
        self.__add_to_hist()

        next_player = True
        # In the first round the players has 3 attempts to get a piece out of home
        if self.round == 1 and \
                all(p_piece == 0 for p_piece in self.players[self.current_player].get_pieces()) and \
                self.current_start_attempts < 3:
            self.current_start_attempts += 1
            next_player = False
        else:
            self.current_start_attempts = 0
        # If it is not in the first round a dice on 6 will give a extra move
        if self.round != 1 and self.current_dice == 6:
            next_player = False
        # If it is the next players turn then change current_player
        if next_player:
            self.__count_player()

        # Set the observation pending to false as the last given observation was handled
        self.observation_pending = False

        # Get the environment after the move
        after_obs = self.__gen_observation(self.current_player)

        return after_obs

    def get_hist(self):
        """
        :returns list of [pieces, current_dice, first_winner_was, current_player, round]
        """
        return self.hist

    def render_environment(self):
        board_img = make_img_of_board(*self.hist[-1])
        return board_img

    def save_hist(self, file_name):
        file_ext = file_name.split(".")[-1]
        assert file_ext == "npy", "The file extension has to be npy (numpy file)"
        np.save(file_name, self.hist)

    def save_hist_video(self, video_out, fps=8, frame_size=None, fourcc=None):
        save_hist_video(video_out, self.hist, fps=fps, frame_size=frame_size, fourcc=fourcc)


if __name__ == "__main__":
    import uuid

    g = Game()

    rounds = 400
    for _ in tqdm(range(rounds)):
        (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()

        if len(move_pieces):
            piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
        else:
            piece_to_move = -1
        g.answer_observation(piece_to_move)

    run_uuid = str(uuid.uuid4())

    print("Saving hist to numpy file")
    g.save_hist(f"{run_uuid}.npy")
    print("Saving hist as video")
    g.save_hist_video(f"{run_uuid}.mp4")
