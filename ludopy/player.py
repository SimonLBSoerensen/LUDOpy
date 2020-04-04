import numpy as np
import logging

# print("NUMPY IS SEEDED!!!!")
# np.random.seed(321)

# log_level = logging.ERROR
# logging.basicConfig(filename='player.log', level=log_level)
TOTAL_NUMBER_OF_TAILES = 60
DICE_MOVE_OUT_OF_HOME = 6
NO_ENEMY = -1

# This roule is that if, there are two pieces on the field, the last one has to return is to start
PLAY_WITH_RULE_A = True

TAILE_FREE = 0
TAILE_HOME = 1
TAILE_START = 2
TAILE_GLOB = 3
TAILE_GOAL_AREAL = 4
TAILE_STAR = 5
TAILE_GOAL = 6
TAILE_ENEMY_1_GLOB = 7
TAILE_ENEMY_2_GLOB = 8
TAILE_ENEMY_3_GLOB = 9
LIST_TAILE_ENEMY_GLOBS = [TAILE_ENEMY_1_GLOB, TAILE_ENEMY_2_GLOB, TAILE_ENEMY_3_GLOB]

NULL_POS = -1
HOME_INDEX = 0
START_INDEX = 1
STAR_INDEXS = [5, 12, 18, 25, 31, 38, 44, 51]

HOME_AREAL_INDEXS = [53, 54, 55, 56, 57, 58]
GOAL_INDEX = 59
GLOB_INDEXS = [9, 22, 35, 48]
ENEMY_1_GLOB_INDX = 14
ENEMY_2_GLOB_INDX = 27
ENEMY_3_GLOB_INDX = 40
STAR_AT_GOAL_AREAL_INDX = STAR_INDEXS[-1]

BORD_TILES = np.full(TOTAL_NUMBER_OF_TAILES, TAILE_FREE)
BORD_TILES[HOME_INDEX] = TAILE_HOME
BORD_TILES[START_INDEX] = TAILE_START
BORD_TILES[STAR_INDEXS] = TAILE_STAR
BORD_TILES[GLOB_INDEXS] = TAILE_GLOB
BORD_TILES[HOME_AREAL_INDEXS] = TAILE_GOAL_AREAL
BORD_TILES[GOAL_INDEX] = TAILE_GOAL
BORD_TILES[ENEMY_1_GLOB_INDX] = TAILE_ENEMY_1_GLOB
BORD_TILES[ENEMY_2_GLOB_INDX] = TAILE_ENEMY_2_GLOB
BORD_TILES[ENEMY_3_GLOB_INDX] = TAILE_ENEMY_3_GLOB

ENEMY_1_INDX_AT_HOME = 40  # HOME_AREAL_INDEXS[0] - 6 - i * 13 # i = 1
ENEMY_2_INDX_AT_HOME = 27  # HOME_AREAL_INDEXS[0] - 6 - i * 13 # i = 2
ENEMY_3_INDX_AT_HOME = 14  # HOME_AREAL_INDEXS[0] - 6 - i * 13 # i = 3


class Player:
    """
    A class used by the Game class
    This class is not needed for normal use

    ...

    Attributes
    ----------
    pieces : list
        List of the index's of the players pieces
    number_of_pieces : int
        The number of pieces the player has
    sound : str
        the sound that the animal makes
    num_legs : int
        the number of legs the animal has (default 4)

    Methods
    -------
    other_enemy_pos(pos)
        Returns the index's the other players has to be in to be in the same location as the one given in pos
    get_enemy_at_pos(pos, enemys)
        Returns the enemy's and the pieces they have at the given location
    get_pieces_that_can_move(dice)
        Return the pieces that can move with the given dice
    player_winner()
        Returns rather the player is a winner or not
    set_pieces(pieces)
        Sets the players pieces
    get_pieces()
        Returns the players pieces
    move_piece(piece, dice, enemys)
        Move the players piece the given dice following the game rules. Returns the new locations of the enemy's pieces
    set_all_pices_to_home()
        Sets all the players pieces to the home index
    """
    def __init__(self):
        self.pieces = []
        self.number_of_pieces = 4
        self.set_all_pices_to_home()

    def other_enemy_pos(self, pos):
        """
        Returns the index's the other players has to be in to be in the same location as the one given in pos

        :param pos (int): The location to check for

        :return: The locations the enemy's pieces has to be at
        """
        if pos == 0:
            return [[-1], [-1], [-1], [-1]]

        enemy_pos = []

        for enemy_start_pos, enemy_pos_at_start in [[ENEMY_1_GLOB_INDX, ENEMY_1_INDX_AT_HOME],
                                                    [ENEMY_2_GLOB_INDX, ENEMY_2_INDX_AT_HOME],
                                                    [ENEMY_3_GLOB_INDX, ENEMY_3_INDX_AT_HOME]]:
            post_offset = enemy_start_pos - 1
            pre_offset = enemy_pos_at_start - 1

            if pos == enemy_start_pos:
                pos_enemy = [START_INDEX, HOME_AREAL_INDEXS[0]]
            elif START_INDEX <= pos < enemy_start_pos:
                pos_enemy = [pos + pre_offset]
            elif pos > HOME_AREAL_INDEXS[0]:
                pos_enemy = [-1]
            else:
                pos_enemy = [pos - post_offset]
            enemy_pos.append(pos_enemy)

        return enemy_pos

    def get_enemy_at_pos(self, pos, enemys):
        """
        Returns the enemy's and the pieces they have at the given location

        :param pos (int): The location to check for

        :param enemys: The lications for the enemy's pieces in a list of 4 lists

        :returns:
        - enemy_at_pos: The enemy's there are at the location
        - enemy_pieces_at_pos: The pieces the enemy's has at the location
        """
        # Get the pos the enemy's has to be at to be at the same pos
        other_enemy_pos_at_pos = self.other_enemy_pos(pos)
        # Check if there is a enemy and how many pieces the enemy has there
        enemy_at_pos = NO_ENEMY
        enemy_pieces_at_pos = []

        for enemy_i, other_enemy_pos in enumerate(other_enemy_pos_at_pos):
            # Check if there already is found a enemy at pos.
            if enemy_at_pos != NO_ENEMY:
                # If there is then stop checking for more (there can only be one)
                break

            for o_pos in other_enemy_pos:
                if o_pos == NULL_POS:
                    continue

                for enemy_pice, enemy_pos in enumerate(enemys[enemy_i]):
                    if enemy_pos == o_pos:
                        enemy_pieces_at_pos.append(enemy_pice)
                        enemy_at_pos = enemy_i

        return enemy_at_pos, enemy_pieces_at_pos

    def get_pieces_that_can_move(self, dice):
        """
        Return the pieces that can move with the given dice

        :param dice: The dice the move will be done with

        :return: movable_pieces (list): A list with the pieces that can be moved
        """
        movable_pieces = []
        # Go though all the pieces
        for piece_i, piece_place in enumerate(self.pieces):
            # If the piece is a goal then the piece can't move
            if BORD_TILES[piece_place] == TAILE_GOAL:
                continue

            # If the piece is at home and the dice is DICE_MOVE_OUT_OF_HOME then the dice can move out of the home place
            elif BORD_TILES[piece_place] == TAILE_HOME and dice == DICE_MOVE_OUT_OF_HOME:
                movable_pieces.append(piece_i)
            # If the piece is not at home or at the goal it can move
            elif BORD_TILES[piece_place] != TAILE_HOME:
                movable_pieces.append(piece_i)
        return movable_pieces

    def player_winner(self):
        """
        Returns rather the player is a winner or not

        :return: winner (bool): A bool that indicate rather the player is a winner or not
        """
        # Go though all the pieces
        for piece_place in self.pieces:
            # If a piece is not at the goal is not the winner
            if BORD_TILES[piece_place] != TAILE_GOAL:
                return False
        # If no piece was not at the goal the player is the winner
        return True

    def set_pieces(self, pieces):
        """
        Sets the players pieces

        :param pieces: The pieces to set the players pieces to
        """
        self.pieces = pieces.copy()

    def get_pieces(self):
        """
        Returns the players pieces

        :return pieces: The players pieces
        """
        return self.pieces.copy()

    def move_piece(self, piece, dice, enemys):
        """
        Move the players piece the given dice following the game rules. Returns the new locations of the enemy's pieces

        :param piece: The piece to move
        :param dice: The dice to make the move with
        :param enemys: The enemy's pieces
        :return: The new locations of the enemy's pieces
        """
        old_piece_pos = self.pieces[piece]
        new_piece_pos = old_piece_pos + dice

        move_enemy_home_from_poss = []
        do_not_check_rule_a = False
        enemy_at_pos, enemy_pieces_at_pos = self.get_enemy_at_pos(new_piece_pos, enemys)

        if new_piece_pos < len(BORD_TILES):
            goging_to = BORD_TILES[new_piece_pos]
        else:
            goging_to = BORD_TILES[old_piece_pos]
        # logging.debug(f"Moving piece {piece} with dice {dice} to {new_piece_pos} that are a {goging_to} and the enemys is {enemys} at the new pos there is {enemy_at_pos} there has {enemy_pieces_at_pos}")

        # If the dice is 0 then no movement can be done
        if dice == 0:
            pass

        # At goal
        elif BORD_TILES[old_piece_pos] == TAILE_GOAL:
            # The piece can not move
            # logging.debug(f"Pice is at goal")
            pass

        # Goal areal
        elif BORD_TILES[old_piece_pos] == TAILE_GOAL_AREAL:
            # logging.debug(f"Pice is at Goal areal")
            if new_piece_pos <= GOAL_INDEX:
                self.pieces[piece] = new_piece_pos
            else:
                overshoot = new_piece_pos - GOAL_INDEX
                new_piece_pos_corrected = old_piece_pos - overshoot
                self.pieces[piece] = new_piece_pos_corrected

        # The Home areal
        elif BORD_TILES[old_piece_pos] == TAILE_HOME:
            # logging.debug(f"Pice is at Home areal")
            if dice == DICE_MOVE_OUT_OF_HOME:
                self.pieces[piece] = START_INDEX

                # Set the enemy there might be at START_INDEX to moved
                do_not_check_rule_a = True
                move_enemy_home_from_poss.append(START_INDEX)

        # Star before the home areal
        elif new_piece_pos == STAR_AT_GOAL_AREAL_INDX:
            # logging.debug(f"Pice is at Star before the home areal")
            self.pieces[piece] = GOAL_INDEX

            # Set the enemy there might be at STAR_AT_GOAL_AREAL_INDX to moved
            move_enemy_home_from_poss.append(new_piece_pos)

        # The other stars
        elif BORD_TILES[new_piece_pos] == TAILE_STAR:
            present_star_staridx = STAR_INDEXS.index(new_piece_pos)
            next_star_staridx = present_star_staridx + 1
            if next_star_staridx >= len(STAR_INDEXS):
                next_star_staridx = 0
            next_star_pos = STAR_INDEXS[next_star_staridx]

            self.pieces[piece] = next_star_pos
            # logging.debug(f"Pice is at one of the other starts, moving from start {(present_star_staridx, new_piece_pos)} to star {(next_star_staridx, next_star_pos)}")

            # Set the enemy there might be at first star or the start there will be jump to to be moved
            if enemy_at_pos != NO_ENEMY:
                move_enemy_home_from_poss.append(new_piece_pos)

            next_star_enemy_at_pos, next_star_enemy_pieces_at_pos = self.get_enemy_at_pos(next_star_pos, enemys)
            if next_star_enemy_at_pos != NO_ENEMY:
                move_enemy_home_from_poss.append(next_star_pos)

        # Globs there are not own by enemy
        elif BORD_TILES[new_piece_pos] == TAILE_GLOB:
            # logging.debug(f"Pice is at a glob there is NOT own by a other player")
            if enemy_at_pos != NO_ENEMY:
                self.pieces[piece] = HOME_INDEX
            else:
                self.pieces[piece] = new_piece_pos

        # Globs there are own by enemy
        elif BORD_TILES[new_piece_pos] in LIST_TAILE_ENEMY_GLOBS:
            # logging.debug(f"Pice is at a glob there is own by a other player")
            # Get the enemy there own the glob
            globs_enemy = LIST_TAILE_ENEMY_GLOBS.index(BORD_TILES[new_piece_pos])
            # Check if there is a enemy at the glob
            if enemy_at_pos != NO_ENEMY:
                # If there is a other enemy then send them home and move there
                if enemy_at_pos != globs_enemy:
                    move_enemy_home_from_poss.append(new_piece_pos)
                    self.pieces[piece] = new_piece_pos
                # If it is the same enemy there is there them move there
                else:
                    self.pieces[piece] = HOME_INDEX
            # If there ant any enemy at the glob then move there
            else:
                self.pieces[piece] = new_piece_pos

        # If it is a TAILE_FREE or if we move from a GLOB/STAR to a not done case
        elif BORD_TILES[old_piece_pos] == TAILE_FREE or \
                BORD_TILES[new_piece_pos] == TAILE_FREE or \
                BORD_TILES[old_piece_pos] == TAILE_GLOB or \
                BORD_TILES[old_piece_pos] == TAILE_STAR:
            # logging.debug(f"Pice is at free taile. enemy_at_pos:{enemy_at_pos}")
            if enemy_at_pos != NO_ENEMY:
                move_enemy_home_from_poss.append(new_piece_pos)
                # logging.debug(f"There was a nermy at free taile. Adding pos: {new_piece_pos}")
            else:
                pass
                # logging.debug(f"There was no enemy")
            self.pieces[piece] = new_piece_pos

        # If the case was not caught then there is a error
        else:
            print("\nold_piece_pos:", old_piece_pos, "\nnew_piece_pos", new_piece_pos,
                  "\nBORD_TILES[old_piece_pos]:", BORD_TILES[old_piece_pos],
                  "\nBORD_TILES[new_piece_pos]:", BORD_TILES[new_piece_pos], "\ndice:", dice)
            raise RuntimeError("The new_piece_pos case was not handel")

        # Check if there is any enemy there has to be moved
        if len(move_enemy_home_from_poss):
            # logging.debug(f"There is pices to move home")
            # Go through the pos where enemy has to be moved from
            for pos in move_enemy_home_from_poss:
                # Get the enemy at the pos
                enemy_at_pos, enemy_pieces_at_pos = self.get_enemy_at_pos(pos, enemys)
                # logging.debug(f"Moving from pos {pos} where there are {(enemy_at_pos, enemy_pieces_at_pos)}")
                # Check if there was a enemy at the pos
                if enemy_at_pos != NO_ENEMY:
                    # If there is only one enemy then move the enemy home.
                    if not do_not_check_rule_a and not PLAY_WITH_RULE_A or len(enemy_pieces_at_pos) == 1:
                        for enemy_piece in enemy_pieces_at_pos:
                            enemys[enemy_at_pos][enemy_piece] = HOME_INDEX
                            # logging.debug(f"Moving enemy {enemy_at_pos}'s pice {enemy_piece} to home")
                    # If there is more than one then move own piece home
                    else:
                        # logging.debug(f"Moving own piece to home. There was more than one enemy piece")
                        self.pieces[piece] = HOME_INDEX

        return enemys

    def set_all_pices_to_home(self):
        """
        Sets all the players pieces to the home index
        """
        self.pieces = []
        for i in range(self.number_of_pieces):
            self.pieces.append(HOME_INDEX)


if __name__ == "__main__":
    from tqdm import tqdm
    import uuid

    players = [Player(), Player(), Player(), Player()]

    enemys_order = {
        0: [1, 2, 3],
        1: [2, 3, 0],
        2: [3, 0, 1],
        3: [0, 1, 2]
    }

    rounds = 200
    hist = []

    first_winner_at = None
    first_winner_was = None

    pieces = [p.get_pieces() for p in players]
    hist.append([pieces, -1, first_winner_was, -1, -1])

    for round_i in tqdm(range(rounds)):
        # logging.debug(f'Round number: {round_i}')
        for i, p in enumerate(players):
            # logging.debug(f"Player {i}")
            dice = np.random.randint(1, 6 + 1)

            pieces = [p.get_pieces() for p in players]
            hist.append([pieces, dice, first_winner_was, i + 1, round_i])

            mover_pieces = p.get_pieces_that_can_move(dice)
            if len(mover_pieces):
                piece_to_move = mover_pieces[np.random.randint(0, len(mover_pieces))]

                enemys = [players[e].get_pieces() for e in enemys_order[i]]

                enemys_new = p.move_piece(piece_to_move, dice, enemys)

                for e_i, e in enumerate(enemys_order[i]):
                    players[e].set_pieces(enemys_new[e_i])

            if p.player_winner():
                if first_winner_at is None:
                    first_winner_at = round_i
                    first_winner_was = i + 1

            pieces = [p.get_pieces() for p in players]
            hist.append([pieces, dice, first_winner_was, i + 1, round_i])

        if all([p.player_winner() for p in players]):
            print(f"All are done at: {round_i} and first winner was at: {first_winner_at}")
            break

        pieces = [p.get_pieces() for p in players]
        print(f"Pieces at {round_i}:", pieces)

    print(f"Pieces at end:", [p.get_pieces() for p in players])

    np.save(f"../GameSaves/RandomMove/{str(uuid.uuid4())}.npy", hist)
    print(hist[1])
    print(hist[-1])
