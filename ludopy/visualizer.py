import cv2
import numpy as np
from collections import defaultdict
import os

GOAL_COLOR = (234, 255, 0)
PLAYER_1_COLOR = (74, 214, 39)
PLAYER_1_AREAL_COLOR = (173, 185, 58)
PLAYER_2_COLOR = (210, 219, 105)
PLAYER_2_AREAL_COLOR = (241, 184, 53)
PLAYER_3_COLOR = (46, 171, 255)
PLAYER_3_AREAL_COLOR = (79, 78, 127)
PLAYER_4_COLOR = (255, 107, 107)
PLAYER_4_AREAL_COLOR = (239, 59, 74)
TAILE_BACKGROUND_COLOR = (174, 95, 74)
BOARD_BACKGROUND_COLOR = (186, 202, 215)

TAILE_SICE_FULL = np.array([64, 64])
TAILE_PIECE_R = 20
BOARD_TAILE_SIZE = np.array([17, 20])
BOARS_SIZE = TAILE_SICE_FULL * BOARD_TAILE_SIZE

COLOR_TEST_TAILES = [
    [[8, 3], [8, 4], [8, 5], [8, 6]],
    [[8, 10], [8, 11], [8, 12], [8, 13]],
    [[6, 8], [5, 8], [4, 8], [3, 8]],
    [[10, 8], [11, 8], [12, 8], [13, 8]],
    [[7, 7], [7, 9], [9, 7], [9, 9]],
    [[7, 6], [7, 10], [9, 6], [9, 10]],
    [[13, 4], [4, 3], [3, 12], [12, 13]]
]

GOAL_TAILES = [
    [7, 7],
    [7, 8],
    [7, 9],
    [8, 7],
    [8, 8],
    [8, 9],
    [9, 7],
    [9, 8],
    [9, 9]
]

PLAYER_1_GOAL_AREAL = [
    [14, 7],
    [14, 8],
    [13, 8],
    [12, 8],
    [11, 8],
    [10, 8],
]
PLAYER_1_HOME_TAILES = [
    [12, 3],
    [14, 3],
    [12, 5],
    [14, 5]
]

PLAYER_2_GOAL_AREAL = [
    [7, 2],
    [8, 2],
    [8, 3],
    [8, 4],
    [8, 5],
    [8, 6]
]

PLAYER_2_HOME_TAILES = [
    [5, 2],
    [5, 4],
    [3, 4],
    [3, 2]
]

PLAYER_3_GOAL_AREAL = [
    [2, 9],
    [2, 8],
    [3, 8],
    [4, 8],
    [5, 8],
    [6, 8]
]

PLAYER_3_HOME_TAILES = [
    [2, 11],
    [2, 13],
    [4, 11],
    [4, 13]
]

PLAYER_4_GOAL_AREAL = [
    [9, 14],
    [8, 14],
    [8, 13],
    [8, 12],
    [8, 11],
    [8, 10]
]

PLAYER_4_HOME_TAILES = [
    [11, 14],
    [13, 14],
    [13, 12],
    [11, 12]
]

STARS_TAILES = [
    [15, 8],
    [10, 7],
    [8, 1],
    [7, 6],
    [1, 8],
    [6, 9],
    [8, 15],
    [9, 10]
]

GLOBS_TIALES = [
    [13, 9],
    [14, 7],
    [9, 3],
    [7, 2],
    [3, 7],
    [2, 9],
    [7, 13],
    [9, 14]
]
FREE_TAIALES = [
    [10, 9],
    [11, 9],
    [12, 9],
    [14, 9],
    [15, 9],
    [15, 7],
    [13, 7],
    [12, 7],
    [11, 7],
    [9, 6],
    [9, 5],
    [9, 4],
    [9, 2],
    [9, 1],
    [7, 1],
    [7, 3],
    [7, 4],
    [7, 5],
    [6, 7],
    [5, 7],
    [4, 7],
    [2, 7],
    [1, 7],
    [1, 9],
    [3, 9],
    [4, 9],
    [5, 9],
    [7, 10],
    [7, 11],
    [7, 12],
    [7, 14],
    [7, 15],
    [9, 15],
    [9, 13],
    [9, 12],
    [9, 11]
]

TRACK_PLAYER_1 = np.array(
    [[14, 7], [13, 7], [12, 7], [11, 7], [10, 7], [9, 6], [9, 5], [9, 4], [9, 3], [9, 2], [9, 1], [8, 1], [7, 1],
     [7, 2], [7, 3], [7, 4], [7, 5], [7, 6], [6, 7], [5, 7], [4, 7], [3, 7], [2, 7], [1, 7], [1, 8], [1, 9], [2, 9],
     [3, 9], [4, 9], [5, 9], [6, 9], [7, 10], [7, 11], [7, 12], [7, 13], [7, 14], [7, 15], [8, 15], [9, 15], [9, 14],
     [9, 13], [9, 12], [9, 11], [9, 10], [10, 9], [11, 9], [12, 9], [13, 9], [14, 9], [15, 9], [15, 8], [15, 7],
     [14, 7], [14, 8], [13, 8], [12, 8], [11, 8], [10, 8], [9, 8]])
DIFF_1 = TRACK_PLAYER_1 - TRACK_PLAYER_1[0]
DIFF_2 = np.array([DIFF_1[:, 1], -DIFF_1[:, 0]]).T
DIFF_3 = np.array([-DIFF_1[:, 0], -DIFF_1[:, 1]]).T
DIFF_4 = np.array([-DIFF_1[:, 1], DIFF_1[:, 0]]).T

TRACK_PLAYER_2 = np.array([7, 2]) + DIFF_2
TRACK_PLAYER_3 = np.array([2, 9]) + DIFF_3
TRACK_PLAYER_4 = np.array([9, 14]) + DIFF_4

HOME_TAILES = {
    0: PLAYER_1_HOME_TAILES,
    1: PLAYER_2_HOME_TAILES,
    2: PLAYER_3_HOME_TAILES,
    3: PLAYER_4_HOME_TAILES
}

TRACKS = {
    0: TRACK_PLAYER_1,
    1: TRACK_PLAYER_2,
    2: TRACK_PLAYER_3,
    3: TRACK_PLAYER_4
}

PLAYER_COLORS = {
    0: PLAYER_1_COLOR,
    1: PLAYER_2_COLOR,
    2: PLAYER_3_COLOR,
    3: PLAYER_4_COLOR
}
folder, _ = os.path.split(__file__)

big_glob = cv2.imread(os.path.join(folder, "glob.png"))
big_glob = cv2.cvtColor(big_glob, cv2.COLOR_BGR2RGB)
small_glob = cv2.resize(big_glob, (40, 40))
glob_mask = cv2.inRange(small_glob, (255, 255, 255), (255, 255, 255)) == 0

big_star = cv2.imread(os.path.join(folder, "star.png"))
big_star = cv2.cvtColor(big_star, cv2.COLOR_BGR2RGB)
small_star = cv2.resize(big_star, (40, 40))
star_mask = cv2.inRange(small_star, (255, 255, 255), (255, 255, 255)) == 0


def get_taile_cord(n, m):
    top_left = (m * TAILE_SICE_FULL[0], n * TAILE_SICE_FULL[1])
    top_right = ((m + 1) * TAILE_SICE_FULL[0], n * TAILE_SICE_FULL[1])
    bot_left = (m * TAILE_SICE_FULL[0], (n + 1) * TAILE_SICE_FULL[1])
    bot_right = ((m + 1) * TAILE_SICE_FULL[0], (n + 1) * TAILE_SICE_FULL[1])
    center = (top_left[0] + int(np.round((top_right[0] - top_left[0]) / 2)),
              top_left[1] + int(np.round((bot_left[1] - top_left[1]) / 2)))

    return top_left, bot_left, top_right, bot_right, center


def draw_tail(img, n, m, line_color=None, fill_color=None, thickness=2):
    top_left, bot_left, top_right, bot_right, center = get_taile_cord(n, m)

    if fill_color is not None:
        cv2.rectangle(img, top_left, bot_right, fill_color, thickness=-1)
    if line_color is not None:
        cv2.rectangle(img, top_left, bot_right, line_color, thickness)


def get_all_tailes_within(n_start, n_end, m_start, m_end):
    return np.concatenate(np.mgrid[n_start:n_end, m_start:m_end].transpose())


def draw_text(board, text, center, color, thickness=1, fontScale=0.5):
    font = cv2.FONT_HERSHEY_SIMPLEX

    (label_width, label_height), baseline = cv2.getTextSize(text, font, fontScale, thickness)

    bot_left = (center[0] - label_width / 2, center[1] + label_height / 2)
    bot_left = (int(np.round(bot_left[0])), int(np.round(bot_left[1])))

    cv2.putText(board, text, bot_left, font, fontScale, color, thickness, cv2.LINE_AA)


def draw_taile_indxs(board):
    for n in range(0, BOARD_TAILE_SIZE[0]):
        for m in range(0, BOARD_TAILE_SIZE[1]):
            top_left, bot_left, top_right, bot_right, center = get_taile_cord(n, m)
            draw_text(board, f"{n},{m}", center, (0, 0, 0))


def draw_piece(board, n, m, amount, color, thickness=5, lineType=8, shift=0):
    top_left, bot_left, top_right, bot_right, center = get_taile_cord(n, m)

    cv2.circle(board, center, TAILE_PIECE_R, color, thickness=thickness, lineType=8, shift=0)
    draw_text(board, f"{amount}", center, color, thickness=2, fontScale=1)


def draw_basic_board(draw_taile_number=False):
    board = np.full(shape=(*BOARS_SIZE, 3), fill_value=BOARD_BACKGROUND_COLOR, dtype=np.uint8)

    draw_multi_box(board, (7, 7), (9, 9), line_color=(0, 0, 0), fill_color=GOAL_COLOR)

    for n, m in STARS_TAILES + GLOBS_TIALES + FREE_TAIALES:
        draw_tail(board, n, m, line_color=(0, 0, 0), fill_color=TAILE_BACKGROUND_COLOR)

    for n, m in PLAYER_1_HOME_TAILES + PLAYER_1_GOAL_AREAL:
        draw_tail(board, n, m, line_color=(0, 0, 0), fill_color=PLAYER_1_AREAL_COLOR)

    for n, m in PLAYER_2_HOME_TAILES + PLAYER_2_GOAL_AREAL:
        draw_tail(board, n, m, line_color=(0, 0, 0), fill_color=PLAYER_2_AREAL_COLOR)

    for n, m in PLAYER_3_HOME_TAILES + PLAYER_3_GOAL_AREAL:
        draw_tail(board, n, m, line_color=(0, 0, 0), fill_color=PLAYER_3_AREAL_COLOR)

    for n, m in PLAYER_4_HOME_TAILES + PLAYER_4_GOAL_AREAL:
        draw_tail(board, n, m, line_color=(0, 0, 0), fill_color=PLAYER_4_AREAL_COLOR)

    for n, m in GLOBS_TIALES:
        put_image_at_taile(board, small_glob, n, m, glob_mask)

    for n, m in STARS_TAILES:
        put_image_at_taile(board, small_star, n, m, star_mask)

    if draw_taile_number:
        draw_taile_indxs(board)

    return board


def get_tailes_player(player_pieces, player):
    tailes_in_use = defaultdict(lambda: 0)

    for i, piece in enumerate(player_pieces):
        if piece == 0:
            taile = HOME_TAILES[player][i]
        else:
            taile = TRACKS[player][piece - 1]

        tailes_in_use[tuple(taile)] += 1

    return list(tailes_in_use.items())


def get_tailes(player_pieces):
    tailes = []
    for player_i, player_pieces in enumerate(player_pieces):
        tailes.append(get_tailes_player(player_pieces, player_i))
    return tailes


def draw_players(board, player_pieces):
    player_tailes = get_tailes(player_pieces)
    for player_i, tailes in enumerate(player_tailes):
        player_color = PLAYER_COLORS[player_i]
        for taile, amount in tailes:
            draw_piece(board, taile[0], taile[1], amount, player_color)


def draw_multi_box(board, top_left_taile, bottom_right_taile, line_color=None, fill_color=None, thickness=2):
    top_left, _, _, _, _ = get_taile_cord(top_left_taile[0], top_left_taile[1])
    _, _, _, bot_right, _ = get_taile_cord(bottom_right_taile[0], bottom_right_taile[1])

    if fill_color is not None:
        cv2.rectangle(board, top_left, bot_right, fill_color, thickness=-1)
    if line_color is not None:
        cv2.rectangle(board, top_left, bot_right, line_color, thickness)


def draw_dice_backgound(board):
    draw_multi_box(board, (3, 17), (4, 18), line_color=(0, 0, 0))
    draw_multi_box(board, (3, 17), (4, 18), fill_color=(255, 255, 255))
    _, _, _, bot_right, center = get_taile_cord(2, 17)
    draw_text(board, f"Dice:", (bot_right[0], center[1]), (0, 0, 0), fontScale=1, thickness=2)


def draw_dice(board, dice, player):
    _, _, _, bot_right, _ = get_taile_cord(3, 17)
    draw_text(board, f"{dice}", bot_right, PLAYER_COLORS[player], fontScale=3, thickness=3)


def draw_move_count_backgound(board):
    draw_multi_box(board, (1, 17), (1, 18), line_color=(0, 0, 0))
    draw_multi_box(board, (1, 17), (1, 18), fill_color=(255, 255, 255))
    _, _, _, bot_right, center = get_taile_cord(0, 17)
    draw_text(board, f"Round:", (bot_right[0], center[1]), (0, 0, 0), fontScale=1, thickness=2)


def draw_move_count(board, count):
    _, _, _, bot_right, center = get_taile_cord(1, 17)
    draw_text(board, f"{count}", (bot_right[0], center[1]), (0, 0, 0), fontScale=1, thickness=2)


def draw_moment(board, moment):
    pieces, dice, players_dice, round_i = moment

    draw_players(board, pieces)
    draw_dice_backgound(board)

    if dice != -1:
        draw_dice(board, dice, players_dice)

    draw_move_count_backgound(board)
    draw_move_count(board, round_i)


def save_video(filename, ar, fps=8, frame_size=None, fourcc=None, cvt_color_flag=cv2.COLOR_RGB2BGR):
    if fourcc is None:
        file_ext = os.path.split(filename)[-1].split(os.path.extsep)[-1]
        if file_ext == "mp4":
            encoder = cv2.VideoWriter_fourcc(*'MP4V')
        elif file_ext == "avi":
            encoder = cv2.VideoWriter_fourcc(*'MJPG')
        else:
            raise RuntimeError("The video format is not supported. Use a other or add it to the code")
    else:
        encoder = cv2.VideoWriter_fourcc(*fourcc)

    if frame_size is None:
        save_frame_size = ar[0].shape[:2]
        save_frame_size = (save_frame_size[1], save_frame_size[0])
    else:
        save_frame_size = frame_size

    video_out = cv2.VideoWriter(filename, encoder, fps, save_frame_size)

    for frame in ar:
        if frame_size is not None:
            frame = cv2.resize(frame, save_frame_size)

        if cvt_color_flag is not None:
            frame = cv2.cvtColor(frame, cvt_color_flag)

        video_out.write(frame)

    video_out.release()


def save_hist_video(filename, hist, fps=8, frame_size=None, fourcc=None):
    board = draw_basic_board()

    boards = []

    for i, moment in enumerate(hist):
        board_take = board.copy()

        draw_moment(board_take, moment)

        boards.append(board_take)

    save_video(filename, boards, fps=fps, frame_size=frame_size, fourcc=fourcc)


def put_image_at_taile(board, image, n, m, mask=None):
    if mask is None:
        mask = np.full(shape=image.shape[:2], fill_value=True)

    top_left, bot_left, top_right, bot_right, center = get_taile_cord(n, m)

    image_hight, image_width = image.shape[:2]

    board[center[1] - image_hight // 2:center[1] + image_hight // 2,
          center[0] - image_width // 2:center[0] + image_width // 2][mask] = image[mask]


def make_video_from_hist_file(hist_file, video_out, fps=8, frame_size=None, fourcc=None):
    hist = np.load(hist_file, allow_pickle=True)
    save_hist_video(video_out, hist, fps=fps, frame_size=frame_size, fourcc=fourcc)


def make_img_of_board(pieces, dice, players_dice, round_number):
    board = draw_basic_board()
    draw_moment(board, (pieces, dice, players_dice, round_number))
    return board
