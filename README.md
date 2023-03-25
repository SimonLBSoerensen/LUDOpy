# LUDOpy

This is an implementation of the LUDO game in python for use in AI or whatever you want.  
 
For normal use of ludopy, only "ludopy.Game" should be needed.

[![PyPI version](https://badge.fury.io/py/ludopy.svg)](https://badge.fury.io/py/ludopy) [![GitHub license](https://img.shields.io/github/license/SimonLBSoerensen/LUDOpy.svg)](https://github.com/SimonLBSoerensen/LUDOpy/blob/master/LICENSE) 



# Documentation

<!--- [![Documentation Status](https://readthedocs.org/projects/ludopy/badge/?version=latest)](https://ludopy.readthedocs.io/en/latest/?badge=latest) --->
https://ludopy.readthedocs.io/en/latest/index.html

# Installation
### Recommended: Install ludopy from PyPI: 
```sh
pip install ludopy
```
### Alternatively: install ludopy from the GitHub source:

First, clone ludopy using `git`:

```sh
git clone https://github.com/SimonLBSoerensen/LUDOpy
```

Then, `cd` to the folder and run the installation command:
```sh
cd LUDOpy
python setup.py install
```

# Examples
## Random "walk" example:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SimonLBSoerensen/LUDOpy/blob/master/demo/random_walk.ipynb)
```python
import ludopy
import numpy as np

g = ludopy.Game()
there_is_a_winner = False

while not there_is_a_winner:
    (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()

    if len(move_pieces):
        piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
    else:
        piece_to_move = -1

    _, _, _, _, _, there_is_a_winner = g.answer_observation(piece_to_move)

print("Saving history to numpy file")
g.save_hist(f"game_history.npy")
print("Saving game video")
g.save_hist_video(f"game_video.mp4")
```
If you only want to play with a certain amount of players:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SimonLBSoerensen/LUDOpy/blob/master/demo/random_walk_two_players.ipynb)
```python
import ludopy
import numpy as np

g = ludopy.Game(ghost_players=[1, 3])  # This will prevent players 1 and 3 from moving out of the start and thereby they are not in the game
there_is_a_winner = False

while not there_is_a_winner:
    (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()

    if len(move_pieces):
        piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
    else:
        piece_to_move = -1

    _, _, _, _, _, there_is_a_winner = g.answer_observation(piece_to_move)

print("Saving history to numpy file")
g.save_hist(f"game_history.npy")
print("Saving game video")
g.save_hist_video(f"game_video.mp4")
```
If you want to render the environment:
```python
import ludopy
import numpy as np
import cv2

g = ludopy.Game()
there_is_a_winner = False

while not there_is_a_winner:
    (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()

    enviroment_image_rgb = g.render_environment() # RGB image of the enviroment
    enviroment_image_bgr = cv2.cvtColor(enviroment_image_rgb, cv2.COLOR_RGB2BGR)
    cv2.imshow("Enviroment", enviroment_image_bgr)
    cv2.waitKey(1)

    if len(move_pieces):
        piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
    else:
        piece_to_move = -1

    _, _, _, _, _, there_is_a_winner = g.answer_observation(piece_to_move)

cv2.destroyAllWindows()

print("Saving history to numpy file")
g.save_hist(f"game_history.npy")
print("Saving game video")
g.save_hist_video(f"game_video.mp4")
```

# The rules of the game:

### The dice
Six-sided dice are used. With it, you have to hit six to move a piece out of the starting area, 
while all other throws give the right to move a piece the number of fields the eyes show.
Extra throws are given when hitting six (no limit to how many times in a row). 

### At the start
Players take turns alternating with the dice.
At the stroke of 6, you can move a piece out on the board.
In the first round, you have three attempts to get 6.
The active player goes in a clockwise direction (player 1 to 4).

### The course of the game
A 6's entitles you to an extra roll.
The player moves the number of squares corresponding to the eyes of the dice. 
If you land in a field where there is already a piece, the first arrived piece must return to
starting field. If, on the other hand, there are two pieces on the field, then the last to arrive has to return to the starting field.
You have to move a piece (if there is one that can be moved), even if it means you have to back to start.
If you cannot move forward, you must stand for the next turn.

### Fields
On the playing board, there are several special areas and fields.

- The starting area is where the four pieces start. You have to hit a six to take a piece out of the starting area. If you have all your pieces in the starting area, you get up to three strokes with the dice before the tour is passed.
- The target area is where the four pieces should end and can get to the goal. Each player has their own target area, and no other player is allowed to take their pieces in there. To reach the end of the target area (the goal), it must hit precisely - otherwise, you have to move your piece in the opposite direction by the amount you have left over.
- Glob fields protect the pieces from being knocked home. If an opponent's piece lands on a protected piece, it is hit home. However, there is an exception to the coloured globe fields. For example, only red chips can be protected in the red globe field, regardless of the number of chips in the field. If you have two pieces standing on the opponent's coloured globe, they can both be knocked home.
- Starfields act as shortcuts that bring the pieces to the target area faster. If a piece lands on a star, it must be moved to the next star. If it is the star in front of the target area that lands on, the chip is moved directly to the goal.

### The winner
The one who first gets all four pieces in the goal is the winner. (But you choose if the game ends there or if the other players still have to fight)
The goal is the centre. When you have entered the coloured fields, you can not be hit home.
The piece has to be moved precisely into the goal. Otherwise, the piece is struck back the exact number of eyes there are too many.

The rules are taken from this danish site: http://spilregler.dk/ludo/

## The Board

The number inside a piece indicates how many pieces that are at the same tail

### Example 1

![The image show a example of the board](https://github.com/SimonLBSoerensen/LUDOpy/blob/master/board_example.png?raw=true "Board example")

### Example 2

![The image show a example of the board](https://github.com/SimonLBSoerensen/LUDOpy/blob/master/board_example_2.png?raw=true "Board example 2")

### Example of the index method (shown for player 1)

Here the number indicate which index the piece are at

![Example of the index method (shown for player 1)](https://github.com/SimonLBSoerensen/LUDOpy/blob/master/track.png?raw=true "Index method")


Change log:
- 1.5.0
  - Better fix for game history
```python 
# Convert from new history to old history
old_hist = [[new_hist["pieces"][i], new_hist["current_dice"][i],
             new_hist["current_player"][i], new_hist["round"][i]] for i in range(len(new_hist[list(new_hist.keys())[0]]))]

# Convert from old history to new history
new_hist = {"pieces": [], "current_dice": [], "current_player": [], "round": []}
for pieces, current_dice, current_player, round in old_hist:
    new_hist["pieces"].append(pieces)
    new_hist["current_dice"].append(current_dice)
    new_hist["current_player"].append(current_player)
    new_hist["round"].append(round)
```
- 1.4.2
  -   Fix error with numpy when saving the game history (a better fix is needed)
- 1.4.1
  - Change the path into the target area (now pieces goes directly from the last star into the target area while before they had to go to the start globe and then to the target area)
  - Minor code changes 

