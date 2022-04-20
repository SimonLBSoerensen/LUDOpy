from ludopy import visualizer
import cv2

board = visualizer.draw_basic_board(draw_taile_number=False)

for n, m in visualizer.PLAYER_1_HOME_TAILES:
    visualizer.draw_piece(board, n, m, 0, (0, 0, 0))

for i, (n, m) in enumerate(visualizer.TRACK_PLAYER_1):
    visualizer.draw_piece(board, n, m, i+1, (0, 0, 0))

board = cv2.cvtColor(board, cv2.COLOR_RGB2BGR)
cv2.namedWindow("Board", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Board", 640, 480)
cv2.imwrite("track.png", board)
cv2.imshow("Board", board)
cv2.waitKey(0)
cv2.destroyAllWindows()
