import collections

from .player import Player
from .visualizer import make_img_of_board, save_hist_video
import numpy as np


class Game:
    """
    The Game. This class is the only needed class for normal use
    """

    def __init__(self, ghost_players=None):
        """
        Maked a game with 4 players

        :param ghost_players: Players there are not in the game
        :type ghost_players: list of int
        """
        if ghost_players is None:
            ghost_players = []
        self.reset()
        self.enemys_order = {
            0: [1, 2, 3],
            1: [2, 3, 0],
            2: [3, 0, 1],
            3: [0, 1, 2]
        }
        self.ghost_players = ghost_players

    def _dice_generator(self):
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
        - pieces: The pieces for all the players (if seen_from = None) else the pieces for the player given in seen_from
        - enemy_pieces: The pieces of the enemys if a player is given in seen_from
        :rtype pieces: list of 4 int's
        :rtype enemy_pieces: list with 4 lists each with 4 int's

        """
        if seen_from is None:
            pieces = [p.get_pieces() for p in self.players]
            enemy_pieces = None
        else:
            assert 0 <= seen_from <= 3, "The seen_from has to be between 0 and 3. Indicating the player the pieces " \
                                        "are seen from and the enemies are seen from "
            # Get where the player's pieces are
            pieces = self.players[seen_from].get_pieces()
            # Get where the enemy's piece are
            enemy_pieces = [self.players[e].get_pieces() for e in self.enemys_order[seen_from]]
        return pieces, enemy_pieces

    def _make_moment(self):
        pieces, _ = self.get_pieces()
        moment = [pieces, self.current_dice, self.current_player, self.round]
        return moment

    def _add_to_hist(self):
        """
        Adds the state of the game to the history

        """
        pieces, current_dice, current_player, round = self._make_moment()
        self.hist["pieces"].append(pieces)
        self.hist["current_dice"].append(current_dice)
        self.hist["current_player"].append(current_player)
        self.hist["round"].append(round)

    def _get_from_hist_moment(self, i: int):
        moment = [self.hist["pieces"][i], self.hist["current_dice"][i],
                  self.hist["current_player"][i], self.hist["round"][i]]
        return moment

    def reset(self):
        """
        Resets the game and the game history

        """
        self.players = [Player(), Player(), Player(), Player()]
        self.hist = collections.defaultdict(list)
        self.round = 1
        self.current_player = 0
        self.first_winner_was = -1
        self.current_dice = -1
        self.observation_pending = False
        self.current_move_pieces = []
        self.current_enemys = []
        self.current_start_attempts = 0
        self.game_winners = []

    def _gen_observation(self, player_idx, roll_dice=True):
        if roll_dice:
            # Roll the dice
            self._dice_generator()
        dice = self.current_dice

        player = self.players[player_idx]
        # Get the pieces that can be moved with the current dice
        move_pieces = player.get_pieces_that_can_move(dice)
        self.current_move_pieces = move_pieces

        # Get where the player's pieces are and the enemy's pieces are
        player_pieces, enemy_pieces = self.get_pieces(player_idx)
        self.current_enemys = enemy_pieces
        # Check if the player is a winner
        player_is_a_winner = player.player_winner()
        # Check if there is a winner
        there_is_a_winner = any([p.player_winner() for p in self.players])

        return dice, np.copy(move_pieces), np.copy(player_pieces), np.copy(
            enemy_pieces), player_is_a_winner, there_is_a_winner

    def _set_enemy_pieces(self, player_idx, enemy_pieces):
        """
        Will set the enemy pieces to the pieces given in enemy_pieces

        :param player_idx: The player the enemys are seen from
        :type player_idx: int
        :param enemy_pieces: The pieces to update
        :type enemy_pieces: list with 4 lists each with 4 int's
        """
        # Go through the enemies and set the changes in their pieces
        for e_i, e in enumerate(self.enemys_order[player_idx]):
            self.players[e].set_pieces(enemy_pieces[e_i])

    def get_observation(self):
        """
        Return the state/observation of the game and which players turn it is
        A given observation has to be answered before a new one can be given.

        :returns:
        - obs: The observation taken of the state of the game seen from the player given in the return current_player (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner). enemy_pieces's index are seen from the specific enemy
        - current_player: Which players turn it is
        :rtype obs: (int, list with upto 4 int's, list with 4 int's, list of 4 lists with 4 int's, bool, bool)
        :rtype current_player: int

        """
        # Check if there is an observation pending
        if self.observation_pending:
            raise RuntimeError("There is already a pending observation. "
                               "The pending observation has to be answered first")
        # Set pending observation to true
        self.observation_pending = True
        # Get the current environment
        obs = self._gen_observation(self.current_player, roll_dice=True)

        # Add the bord and dice before the move to the history
        self._add_to_hist()
        return obs, self.current_player

    def _count_player(self):
        """
        Updates the current player and the round if the current player was the last player

        """
        # Count up the player
        self.current_player += 1

        # Check is the self.current_player is a ghost player
        while self.current_player in self.ghost_players:
            self.current_player += 1

        # If the count is over 3 then reset to player 0 and count up the round
        if self.current_player > 3:
            self.current_player = 0
            self.round += 1

    def answer_observation(self, piece_to_move):
        """
        Answers an observation. An observation has to be given before an answer can be given.

        :param piece_to_move: Which piece to move. If there was no pieces that could be moved the parameter is ignored
        :type piece_to_move: int
        :return obs: Who the game was after the given move was done. obs is: (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner)
        :rtype obs: (int, list with upto 4 int's, list with 4 int's, list of 4 lists with 4 int's, bool, bool)
        """
        # Check if there is an observation pending
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
            self._set_enemy_pieces(self.current_player, new_enemys)
        # If there was no pieces that could be moved then nothing can be done
        else:
            pass  # This line is present for readability

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
        self._add_to_hist()

        next_player = True
        # In the first round the players has 3 attempts to get a piece out of home
        if self.round == 1 and \
                all(p_piece == 0 for p_piece in self.players[self.current_player].get_pieces()) and \
                self.current_start_attempts < 3:
            self.current_start_attempts += 1
            next_player = False
        else:
            self.current_start_attempts = 0
        # If it is not in the first round a dice on 6 will give an extra move
        if self.round != 1 and self.current_dice == 6:
            next_player = False

        # Set the observation pending to false as the last given observation was handled
        self.observation_pending = False

        # Get the environment after the move
        after_obs = self._gen_observation(self.current_player, roll_dice=False)

        # If it is the next players turn then change current_player
        if next_player:
            self._count_player()

        return after_obs

    def get_winner_of_game(self):
        """
        Returns the winner of the game

        :return winner: If there has been a winner the winner is return if not -1 is returned
        :rtype winner: int
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
        Returns the history that has been recorded during the game. This history can be used to make
        a video of the game. The history will have been extended when a observation was given and when an
        answer to a observation was given.

        :return hist: a dict with lists for [pieces, current_dice, first_winner_was, current_player, round]
        :rtype hist: [list with 4 lists with 4 int's, int, bool, int, int]
        """
        return self.hist

    def get_piece_hist(self, mode=0):
        """
        Will return how the pieces were recorded during the game.

        :param mode: 0: All recorded pieces are returned. 1: Only if a change is done there will be a new set of pieces. 2: Only unique set of pieces (order is preserved)
        :type mode: int
        :return piece_hist: List of sets of pieces [player 1, player 2, player 3, player 4]
        :rtype piece_hist: list of 4 lists with 4 int's
        """
        all_piece_hists = self.hist["piece"]
        piece_hist = [all_piece_hists[0]]
        for pieces in all_piece_hists[1:]:
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
        if len(self.hist):
            moment = self._get_from_hist_moment(-1)
        else:
            moment = self._make_moment()

        board_img = make_img_of_board(*moment)
        return board_img

    def save_hist(self, file_name):
        """
        Saves the history of the game as an npy file

        :param file_name: The file name to save under. Has to have the .npy (numpy file) extension
        :type file_name: str

        """
        file_ext = file_name.split(".")[-1]
        assert file_ext == "npz", "The file extension has to be npy (numpy file)"
        np.savez(file_name, **self.hist)

    def save_hist_video(self, video_out, fps=8, frame_size=None, fourcc=None):
        """
        Saves a video of the game history

        :param video_out: The file name to save under
        :type video_out: str
        :param fps: Frames per second
        :type fps: float
        :param frame_size: The frame size to save in (width, height). If None is given the full board size is used
        :type frame_size: tuple
        :param fourcc: FourCC code to be used. If None is given the FourCC code will be tried to create from the file extension (works on .mp4 and .avi)
        :type fourcc: str

        """
        moment_hist = [self._get_from_hist_moment(i) for i in range(len(self.hist[list(self.hist.keys())[0]]))]
        save_hist_video(video_out, moment_hist, fps=fps, frame_size=frame_size, fourcc=fourcc)
