from .player import Player
from .visualizer import make_img_of_board, save_hist_video
import numpy as np
from tqdm import tqdm


class Game:
    """
    The Game. This class is the only needed class for normal use
    """

    def __init__(self):
        """
        Maked a game with 4 players
        """
        self.players = [Player(), Player(), Player(), Player()]
        self.hist = []
        self.round = 1
        self.current_player = 0
        self.first_winner_was = -1
        self.current_dice = -1
        self.observation_pending = False
        self.current_move_pieces = []
        self.current_enemys = []
        self.current_start_attempts = 0
        self.enemys_order = {
            0: [1, 2, 3],
            1: [2, 3, 0],
            2: [3, 0, 1],
            3: [0, 1, 2]
        }
        self.game_winners = []

    def __dice_generator(self):
        """
        Will update self.current_dice with a new random number on the dice

        """
        self.current_dice = np.random.randint(1, 6 + 1)

    def get_pieces(self, seen_from=None):
        """
        Returns the pieces places on the board

        :param seen_from: indicate which player the pieces and enemy pieces are seen from. If None then the pieces from all 4 player are given and no enemy pieces
        :type seen_from: int
        :returns:
        - pieces: The pieces for alle the players (if seen_from = None) else the pieces for the player given in seen_from
        - enemy_pieces: The pieces of the enemys if a player is given in seen_from
        :rtype pieces: list of 4 int's
        :rtype enemy_pieces: list with 4 lists each with 4 int's

        """
        if seen_from is None:
            pieces = [p.get_pieces() for p in self.players]
            enemy_pieces = None
        else:
            assert 0 <= seen_from <= 3, "The seen_from has to be between 0 and 3. Indicating the player the pieces " \
                                        "are seen from and the nemys are seen from "
            # Get where the players piece are
            pieces = self.players[seen_from].get_pieces()
            # Get where the enemy's piece are
            enemy_pieces = [self.players[e].get_pieces() for e in self.enemys_order[seen_from]]
        return pieces, enemy_pieces

    def __add_to_hist(self):
        """
        Adds the state of the game to the history

        """
        pieces, _ = self.get_pieces()
        self.hist.append([pieces, self.current_dice, self.current_player, self.round])

    def reset(self):
        """
        Resets the game and the game history

        """
        self.players = [Player(), Player(), Player(), Player()]
        self.hist = []
        self.round = 1
        self.current_player = 0
        self.first_winner_was = -1
        self.current_dice = -1
        self.observation_pending = False
        self.current_move_pieces = []
        self.current_enemys = []
        self.current_start_attempts = 0
        self.game_winners = []

    def __gen_observation(self, player_idx, roll_dice = True):
        if roll_dice:
            # Roll the dice
            self.__dice_generator()
        dice = self.current_dice

        player = self.players[player_idx]
        # Get the pieces there can be moved with the current dice
        move_pieces = player.get_pieces_that_can_move(dice)
        self.current_move_pieces = move_pieces

        # Get where the players piece are and the enemy's piece are
        player_pieces, enemy_pieces = self.get_pieces(player_idx)
        self.current_enemys = enemy_pieces
        # Check if the player is a winner
        player_is_a_winner = player.player_winner()
        # Check if there is a winner
        there_is_a_winner = any([p.player_winner() for p in self.players])

        return dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner

    def __set_enemy_pieces(self, player_idx, enemy_pieces):
        """
        Will set the enemy pieces to the pieces given in enemy_pieces

        :param player_idx: The player the enemys are seen from
        :type player_idx: int
        :param enemy_pieces: The pieces to update
        :type enemy_pieces: list with 4 lists each with 4 int's
        """
        # Go throng the enemy's and set the changes in there piece
        for e_i, e in enumerate(self.enemys_order[player_idx]):
            self.players[e].set_pieces(enemy_pieces[e_i])

    def get_observation(self):
        """
        Return the state/observation of the game and which players turn it is
        A given observation has to be answered before a new one can be given.

        :returns:
        - obs: The observation taken of the state of the game seen from the player given in the return current_player (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner)
        - current_player: Which players turn it is
        :rtype obs: (int, list with upto 4 int's, list with 4 int's, list of 4 lists with 4 int's, bool, bool)
        :rtype current_player: int

        """
        # Check if there is a observation pending
        if self.observation_pending:
            raise RuntimeError("There is already a pending observation. "
                               "The pending observation has to be answered first")
        # Set pending observation to true
        self.observation_pending = True
        # Get the current en environment
        obs = self.__gen_observation(self.current_player, roll_dice=True)

        # Add the bord and dice before the move to the history
        self.__add_to_hist()
        return obs, self.current_player

    def __count_player(self):
        """
        Updates the current player and the round if the current player was the last player

        """
        # Count up the player
        self.current_player += 1
        # If the count is over 3 then reset to player 0 and count up the round
        if self.current_player > 3:
            self.current_player = 0
            self.round += 1

    def answer_observation(self, piece_to_move):
        """
        Answers a observation. A observation has to be given before a answer can be given.

        :param piece_to_move: Which piece to move. If there was no pieces there cloud be moved the parameter is ignored
        :type piece_to_move: int
        :return obs: Who the game was after the given move was done. obs is: (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner)
        :rtype obs: (int, list with upto 4 int's, list with 4 int's, list of 4 lists with 4 int's, bool, bool)
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
        player_is_a_winner = self.players[self.current_player].player_winner()
        if player_is_a_winner:
            # Check if player is the first winner
            if self.first_winner_was == -1:
                self.first_winner_was = self.current_player
            # Check if player has been added to game_winners
            if self.current_player not in self.game_winners:
                self.game_winners.append(self.current_player)

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
        after_obs = self.__gen_observation(self.current_player, roll_dice=False)

        return after_obs

    def get_winner_of_game(self):
        """
        Returns the winner of the game

        :return winner: If there has been a winner the winner is return if not -1 is returned
        :rtype winner: bool
        """
        return self.first_winner_was

    def get_winners_of_game(self):
        """
        Returns the winners of the game

        :return gameWinners: A list of the winners of the game in the order they got all piece in goal
        :rtype gameWinners: list with upto 4 int's
        """
        return self.game_winners

    def all_players_finish(self):
        """
        Returns rather all players has finish

        :return allFinish: Bool rather all players has finish the game
        :rtype allFinish: bool
        """
        return len(self.game_winners) == len(self.players)

    def get_hist(self):
        """
        Returns the history there has been recorded during the game. This history can be used to make
        a video of the game. The history will have been extended when a observation was given and when a
        answer to a observation was given.

        :return hist: list of [pieces, current_dice, first_winner_was, current_player, round]
        :rtype hist: [list with 4 lists with 4 int's, int, bool, int, int]
        """
        return self.hist

    def get_piece_hist(self, mode=0):
        """
        Will return the how the pieces was recorded during the game.

        :param mode: 0: All recorded pieces is returnt. 1: Only if a change is done there will be a new set of pieces. 2: Only unique set of pieces (order is preserved)
        :type mode: int
        :return piece_hist: List of sets of pieces [player 1, player 2, player 3, player 4]
        :rtype piece_hist: list of 4 lists with 4 int's
        """
        piece_hist = [self.hist[0][0]]
        for h in self.hist[1:]:
            pieces = h[0]

            add_to_hist = False
            if mode == 0:
                add_to_hist = True
            if mode == 1:
                if pieces != piece_hist[-1]:
                    add_to_hist = True
            if mode == 2:
                if pieces not in piece_hist:
                    add_to_hist = True

            if add_to_hist:
                piece_hist.append(pieces)
        return piece_hist

    def render_environment(self):
        """
        Will render the last record in the history

        :return board_img: A image of the board
        :rtype board_img: ndarray, RGB colorspace
        """
        board_img = make_img_of_board(*self.hist[-1])
        return board_img

    def save_hist(self, file_name):
        """
        Saves the history of the game as a npy file

        :param file_name: The file name to save under. Has to have the .npy (numpy file) extension
        :type file_name: str

        """
        file_ext = file_name.split(".")[-1]
        assert file_ext == "npy", "The file extension has to be npy (numpy file)"
        np.save(file_name, self.hist)

    def save_hist_video(self, video_out, fps=8, frame_size=None, fourcc=None):
        """
        Saves a video of the game history

        :param video_out: The file name to save under
        :type video_out: str
        :param fps: Frames per second
        :type fps: float
        :param frame_size: The frame size to save in (width, height). If None is given the full board size is used
        :type frame_size: tuple
        :param fourcc: FourCC code to be used. If None is given the FourCC code will be tried to create fro the file extension (works on .mp4 and .avi)
        :type fourcc: str

        """
        save_hist_video(video_out, self.hist, fps=fps, frame_size=frame_size, fourcc=fourcc)

