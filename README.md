# LUDOpy

This is a implementation of the LUDO game in python for use in AI or whatever you want.  

For normal use of ludopy only ludopy.Game should be needed.

## The rules the game follows:

### The dice
A a six-sided dice is used. With it, you have to hit six to move a piece out of the starting area, while all other throws give the right to move a piece the number of fields the eyes show. Extra throws are given when hitting six (no limit to how many times in a row). 

### At the start
Players take turns alternating with the dice.
At the stroke of 6, you have the right to throw a piece out on the board.
If all the pieces are in the starting field, you have three attempts to beat a 6.
Players turn in turn in a clockwise direction (player 1 to 4).

### The course of the game
A 6's entitles you to an extra roll.
The player moves the number of squares corresponding to the eyes of the dice. 
If you land in a field where there is already a piece, the first arrived piece must return to
starting field. If, on the other hand, there are two pieces on the field, then the last to arrive has to return to the starting field.
You have to move a piece (if there is one that can be moved), even if it means you have to back to start.
If you cannot move forward, you must stand for the next turn.

### Fields
On the playing board there are several special areas and fields.

- The starting area is where the four pieces start. To take a piece out of the starting area, you have to hit a six. If you have all your pieces in the starting area, you get up to three strokes with the dice before the tour is passed.
- The target area is where the four pieces should end and can get to the goal. Each player has their own target area, and no other player is allowed to take their pieces in there. To reach the end of the target area (the goal), it must hit precisely - otherwise you have to move your piece in the opposite direction by the amount you have leftover.
- Globus fields protect the pieces from being knocked home. If an opponent's piece lands on a protected piece, it is hit home. However, there is an exception to the colored globe fields. For example, only red chips can be protected in the red globe field, regardless of the number of chips in the field. If you have two pieces standing on the opponent's colored globe, they can both be knocked home.
- Star fields act as shortcuts that can bring the pieces faster to the target area. If a piece lands on a star, it must be moved to the next star. If it is the star in front of the target area that lands on, the chip is moved directly to the goal.

### The winner
The one who first gets all 4 pieces in the finish is the winner. (But you choose if the game ends there or the other players has to fight to the last man standing)
Goals are the center, and you have to go all the way in and out via your own color to get to the finish. When you have entered the colored fields you can not be hit home.
The piece has to be move precisely into the goal otherwise the piece are struck back the exact number of eyes there are to many.

The rules are taken from the danish site: http://spilregler.dk/ludo/

## The Board

![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")


## Random "walk" example:
```python
import ludopy
import numpy as np
from tqdm import tqdm

g = ludopy.Game()

rounds = 100
for _ in tqdm(range(rounds)):
    (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()

    if len(move_pieces):
        piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
    else:
        piece_to_move = -1
    g.answer_observation(piece_to_move)

print("Saving history to numpy file")
g.save_hist(f"game_history.npy")
print("Saving game video")
g.save_hist_video(f"game_video.mp4")
```

# Installation
- Recommended: Install ludopy from PyPI: 
```sh
pip install ludopy
```
- Alternatively: install ludopy from the GitHub source:

First, clone ludopy using `git`:

```sh
git clone https://github.com/SimonLBSoerensen/LUDOpy
```

Then, `cd` to the folder and run the install command:
```sh
cd LUDOpy
python setup.py install
```

# Attribution 

The star and glob icons are taken from:
- Star made by <a href="https://www.flaticon.com/authors/pixel-perfect" title="Pixel perfect">Pixel perfect</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
- Glob made by <a href="https://www.flaticon.com/authors/turkkub" title="turkkub">turkkub</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>