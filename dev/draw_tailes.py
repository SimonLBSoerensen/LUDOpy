from ludopy import visualizer
import cv2

board = visualizer.draw_basic_board(draw_taile_number=False)
visualizer.draw_taile_indxs(board)

board = cv2.cvtColor(board, cv2.COLOR_RGB2BGR)
cv2.imwrite("tailes.png", board)
cv2.imshow("board", board)
cv2.waitKey(0)
cv2.destroyAllWindows()
