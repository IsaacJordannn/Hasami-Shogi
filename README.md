# Hasami-Shogi
A variant of shogi (Japanese chess) that can be played in the terminal.

Program is written using the rules for "**Variant 1**" on [the Wikipedia page](https://en.wikipedia.org/wiki/Hasami_shogi), including the diagram of the starting position. Custodian captures may be made on multiple sides (up to 3 sides) of the moved piece. For example if the black piece on square h6 in the diagram below moves to square c6, then the red pieces at c4, c5, and b6 would be captured. If instead, the black piece at h6 moves to h1, then the red pieces at e1, f1, g1, and i1 would be captured.

  1  2  3  4  5  6  7  8  9
  _________________________   
A |と|と|と|と|と|と|と|と|と|
B |・|・|・|・|・|・|・|・|・|
C |・|・|・|・|・|・|・|・|・|
D |・|・|・|・|・|・|・|・|・|
E |・|・|・|・|・|・|・|・|・|
F |・|・|・|・|・|・|・|・|・|
G |・|・|・|・|・|・|・|・|・|
H |・|・|・|・|・|・|・|・|・|
I |歩|歩|歩|歩|歩|歩|歩|歩|歩|
  ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

Locations on the board will be specified using "algebraic notation", with rows labeled a-i and rows labeled 1-9, as shown in the diagram of the starting position shown on the Wikipedia page.

* A method called `get_game_state` takes no parameters and returns 'UNFINISHED', 'RED_WON' or 'BLACK_WON'.
* A method called `get_active_player` takes no parameters and returns whose turn it is - either 'RED' or 'BLACK'.
* A method called `get_num_captured_pieces` takes one parameter, 'RED' or 'BLACK', and returns the number of pieces of that color that have been captured.
* A method called `make_move` takes two parameters - strings that represent the square moved from and the square moved to.  For example, make_move('b3', 'b9').  If the square being moved from does not contain a piece belonging to the player whose turn it is, or if the indicated move is not legal, or if the game has already been won, then it should just return False.  Otherwise it should make the indicated move, remove any captured pieces, update the game state if necessary, update whose turn it is, and return True.
* A method called `get_square_occupant` takes one parameter, a string representing a square (such as 'i7'), and returns 'RED', 'BLACK', or 'NONE', depending on whether the specified square is occupied by a red piece, a black piece, or neither.

Here's a very simple example of how the class could be used:
```
game = HasamiShogiGame()
move_result = game.make_move('i6', 'e3')
print(game.get_active_player())
print(game.get_square_occupant('a4'))
print(game.get_game_state())
```
