# Author: Isaac Hernandez
# Date: 12/2/21
# Description: A HasamiShogiGame class is created to represent the board game. When the class is initialized the private
#              data members are defined and the function creating the board is called. There is an optional function
#              that will display the board in a somewhat accurate representation to the user. The function that the
#              class structure is centered around is the make_move function. It takes as parameters the algebraic
#              notations for the start and finish pieces and validates the move through helper functions. These
#              validation functions ensure that the correct player is playing, the piece being moved is theirs, their
#              destination is blank, a diagonal move isn't taking place, the game hasn't been won, and the move doesn't
#              jump other pieces. If all these return True, the start square is made blank and the destination square
#              takes on the character of the player playing. There is then a check to see if captures take place as a
#              result of the move. Captures are checked for the three directions that are not the direction where the
#              piece started. When captures can be made, the number of pieces captured for that color is added and those
#              squares on the board are made blank. When no captures are possible or all possible captures have been
#              made, there is a check to see if a winner has been found by looking at the number of pieces captured.
#              Whoever has had 8 or more pieces captured is the loser. If game has been won, the state of the game is
#              updated, and if not only the turn will be updated.

class HasamiShogiGame:
    """Represents the Hasami Shogi board game."""

    def __init__(self):
        """Initialize all private data members."""
        self._turn = "BLACK"
        self._state = "UNFINISHED"
        self._red_captured = 0
        self._black_captured = 0
        self._letter = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8}
        self._number = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8}
        self._start_row = 0
        self._start_column = 0
        self._finish_row = 0
        self._finish_column = 0
        self._start_piece = ""
        self._finish_piece = ""
        self._board = []
        self._create_board()

    def _create_board(self):
        """Fills board with 9 lists, each containing 9 spaces that correspond to a square on the board."""
        for row in range(0, 9):
            board_row = []
            for column in range(0, 9):
                if row == 0:
                    board_row.append("と")               # creates red row (と represents promoted pawns)
                elif row == 8:
                    board_row.append("歩")               # creates black row (歩 represents unpromoted pawns)
                else:
                    board_row.append("・")               # creates empty spaces that align with length of characters
            self._board.append(board_row)
        return self._display_board()

    def _display_board(self):
        """Creates a printed visual of the board."""
        row_label = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        column_label = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        row_counter = 0
        print("  " + "  ".join(column_label))                       # displays column headers, followed by top of board
        print("  " + "_" * 25)
        for row in range(len(self._board)):
            print(row_label[row_counter] + " " + "|", end="")       # displays row headers, continues line for values
            print("|".join(self._board[row]) + "|")
            row_counter += 1
        print("  " + "¯" * 25)

    def make_move(self, start, finish):
        """Takes a start and finish square and moves the piece if move is valid."""
        self._start_row = self._letter[start[0].upper()]    # indices used to identify starting piece on board
        self._start_column = self._number[start[1]]
        self._finish_row = self._letter[finish[0].upper()]  # indices used to identify final destination on board
        self._finish_column = self._number[finish[1]]
        if HasamiShogiGame._validate_move(self) is True:
            self._board[self._start_row][self._start_column] = "・"
            if self._turn == "BLACK":
                self._board[self._finish_row][self._finish_column] = "歩"
                self._finish_piece = "歩"
            elif self._turn == "RED":
                self._board[self._finish_row][self._finish_column] = "と"
                self._finish_piece = "と"
            HasamiShogiGame._check_capture(self)
        else:
            self._display_board()
            print("Invalid move. Please enter start and finish position again.")
            return False
        self._display_board()
        return True

    def _validate_move(self):
        """Checks each point of validity and returns True or False based on the tests."""
        self._start_piece = self._board[self._start_row][self._start_column]
        self._finish_piece = self._board[self._finish_row][self._finish_column]
        if HasamiShogiGame._validate_start_finish(self) is True:
            pass
        else:
            return False
        if HasamiShogiGame._validate_game_state(self) is True:
            pass
        else:
            return False
        if HasamiShogiGame._validate_continuity(self) is True:
            pass
        else:
            return False
        return True

    def _validate_start_finish(self):
        """Ensures start piece matches turn, finish piece is empty, and doesn't move diagonally."""
        if self._turn == "BLACK" and self._start_piece == "歩" and self._finish_piece == "・":
            pass
        elif self._turn == "RED" and self._start_piece == "と" and self._finish_piece == "・":
            pass                                                                    # ensure correct start piece and
        else:                                                                       # turn, empty destination square
            return False
        if self._start_row == self._finish_row or self._start_column == self._finish_column:    # ensure no diagonals
            pass
        else:
            return False
        return True

    def _validate_game_state(self):
        """Ensures game has not been won."""
        if self._state == "UNFINISHED":
            pass
        else:
            return False
        return True

    def _validate_continuity(self):
        """Checks which direction the piece moves and returns True or False depending on test results."""
        if self._start_row > self._finish_row:                                          # move up
            if HasamiShogiGame._validate_up(self) is True:
                pass
            else:
                return False
        if self._start_row < self._finish_row:                                          # move down
            if HasamiShogiGame._validate_down(self) is True:
                pass
            else:
                return False
        if self._start_column > self._finish_column:                                    # move left
            if HasamiShogiGame._validate_left(self) is True:
                pass
            else:
                return False
        if self._start_column < self._finish_column:                                    # move right
            if HasamiShogiGame._validate_right(self) is True:
                pass
            else:
                return False
        return True

    def _validate_up(self):
        """Checks each square between start and finish when moving up to ensure no jumps occur."""
        check_spaces = abs(self._start_row - self._finish_row)
        for num in range(1, check_spaces):
            square = self._board[self._start_row - num][self._start_column]
            if square != "・":
                return False
        return True

    def _validate_down(self):
        """Checks each square between start and finish when moving down to ensure no jumps occur."""
        check_spaces = abs(self._start_row - self._finish_row)
        for num in range(1, check_spaces):
            square = self._board[self._start_row + num][self._start_column]
            if square != "・":
                return False
        return True

    def _validate_left(self):
        """Checks each square between start and finish when moving left to ensure no jumps occur."""
        check_spaces = abs(self._start_column - self._finish_column)
        for num in range(1, check_spaces):
            square = self._board[self._start_row][self._start_column - num]
            if square != "・":
                return False
        return True

    def _validate_right(self):
        """Checks each square between start and finish when moving right to ensure no jumps occur."""
        check_spaces = abs(self._start_column - self._finish_column)
        for num in range(1, check_spaces):
            square = self._board[self._start_row][self._start_column + num]
            if square != "・":
                return False
        return True

    def _check_capture(self):
        """Checks for direction of movement and determines if pieces can be potentially captured."""
        if self._start_row > self._finish_row:                          # started down, can't capture down
            HasamiShogiGame._potential_up(self)
        elif self._start_row < self._finish_row:                          # started up, can't capture up
            HasamiShogiGame._potential_down(self)
        elif self._start_column > self._finish_column:                    # started right, can't capture right
            HasamiShogiGame._potential_left(self)
        elif self._start_column < self._finish_column:                    # started left, can't capture left
            HasamiShogiGame._potential_right(self)
        HasamiShogiGame._check_for_win(self)
        return

    def _potential_up(self):
        """Check for potential captures up, left, and right from the finish square."""
        if self._finish_row > 0:
            HasamiShogiGame._up_check(self)
        if self._finish_column > 0:
            HasamiShogiGame._left_check(self)
        if self._finish_column < 8:
            HasamiShogiGame._right_check(self)
        return

    def _potential_down(self):
        """Check for potential captures down, left, and right from the finish square."""
        if self._finish_row < 8:
            HasamiShogiGame._down_check(self)
        if self._finish_column > 0:
            HasamiShogiGame._left_check(self)
        if self._finish_column < 8:
            HasamiShogiGame._right_check(self)
        return

    def _potential_left(self):
        """Check for potential captures up, down, and left from the finish square."""
        if self._finish_row > 0:
            HasamiShogiGame._up_check(self)
        if self._finish_row < 8:
            HasamiShogiGame._down_check(self)
        if self._finish_column > 0:
            HasamiShogiGame._left_check(self)
        return

    def _potential_right(self):
        """Check for potential captures up, down, and right from the finish square."""
        if self._finish_row > 0:
            HasamiShogiGame._up_check(self)
        if self._finish_row < 8:
            HasamiShogiGame._down_check(self)
        if self._finish_column < 8:
            HasamiShogiGame._right_check(self)
        return

    def _up_check(self):
        """Determines whether pieces above the finish piece can be captured."""
        row_index = []
        index = 1
        next_piece = self._board[self._finish_row - index][self._finish_column]
        if next_piece == self._finish_piece or next_piece == "・":           # needs to be opposite character
            return
        else:
            row_index.append(self._finish_row - index)
        if self._finish_row - index == 0 and self._finish_column == 0:      # top left corner capture
            if self._board[self._finish_row - index][self._finish_column + index] == self._finish_piece:
                HasamiShogiGame._capture_up(self, row_index)
        elif self._finish_row - index == 0 and self._finish_column == 8:    # top right corner capture
            if self._board[self._finish_row - index][self._finish_column - index] == self._finish_piece:
                HasamiShogiGame._capture_up(self, row_index)
        elif self._finish_row - index == 0:                                 # no possible captures
            return
        index += 1
        while self._finish_row - index >= 0:        # loop until determined whether or not capture can be made
            if self._board[self._finish_row - index][self._finish_column] == "・":
                return
            elif self._board[self._finish_row - index][self._finish_column] != self._finish_piece:
                row_index.append(self._finish_row - index)
            else:
                HasamiShogiGame._capture_up(self, row_index)
                return
        return

    def _down_check(self):
        """Determines whether pieces below the finish piece can be captured."""
        row_index = []
        index = 1
        next_piece = self._board[self._finish_row + index][self._finish_column]
        if next_piece == self._finish_piece or next_piece == "・":           # needs to be opposite character
            return
        else:
            row_index.append(self._finish_row + index)
        if self._finish_row + index == 8 and self._finish_column == 0:      # bottom left corner
            if self._board[self._finish_row + index][self._finish_column + index] == self._finish_piece:
                HasamiShogiGame._capture_down(self, row_index)
        elif self._finish_row + index == 8 and self._finish_column == 8:    # bottom right corner
            if self._board[self._finish_row + index][self._finish_column - index] == self._finish_piece:
                HasamiShogiGame._capture_down(self, row_index)
        elif self._finish_row + index == 8:                                 # no possible captures
            return
        index += 1
        while self._finish_row + index <= 8:        # loop until determined whether or not capture can be made
            if self._board[self._finish_row + index][self._finish_column] == "・":
                return
            elif self._board[self._finish_row + index][self._finish_column] != self._finish_piece:
                row_index.append(self._finish_row + index)
            else:
                HasamiShogiGame._capture_down(self, row_index)
                return
            index += 1
        return

    def _left_check(self):
        """Determines whether pieces left of the finish piece can be captured."""
        column_index = []
        index = 1
        next_piece = self._board[self._finish_row][self._finish_column - index]
        if next_piece == self._finish_piece or next_piece == "・":           # needs to be opposite character
            return
        else:
            column_index.append(self._finish_column - index)
        if self._finish_row == 0 and self._finish_column - index == 0:      # top left corner
            if self._board[self._finish_row + index][self._finish_column - index] == self._finish_piece:
                HasamiShogiGame._capture_left(self, column_index)
        elif self._finish_row == 8 and self._finish_column - index == 0:    # bottom left corner
            if self._board[self._finish_row - index][self._finish_column - index] == self._finish_piece:
                HasamiShogiGame._capture_left(self, column_index)
        elif self._finish_column - index == 0:                              # no possible captures
            return
        index += 1
        while self._finish_column - index >= 0:         # loop until determined whether or not capture can be made
            if self._board[self._finish_row][self._finish_column - index] == "・":
                return
            elif self._board[self._finish_row][self._finish_column - index] != self._finish_piece:
                column_index.append(self._finish_column - index)
            else:
                HasamiShogiGame._capture_left(self, column_index)
                return
            index += 1
        return

    def _right_check(self):
        """Determines whether pieces right of the finish piece can be captured."""
        column_index = []
        index = 1
        next_piece = self._board[self._finish_row][self._finish_column + index]
        if next_piece == self._finish_piece or next_piece == "・":           # needs to be opposite character
            return
        else:
            column_index.append(self._finish_column + index)
        if self._finish_row == 0 and self._finish_column + index == 8:      # top right corner
            if self._board[self._finish_row + index][self._finish_column + index] == self._finish_piece:
                HasamiShogiGame._capture_right(self, column_index)
        elif self._finish_row == 8 and self._finish_column + index == 8:    # bottom right corner
            if self._board[self._finish_row - index][self._finish_column + index] == self._finish_piece:
                HasamiShogiGame._capture_right(self, column_index)
        elif self._finish_column + index == 8:                              # no possible captures
            return
        index += 1
        while self._finish_column + index <= 8:         # loop until determined whether or not capture can be made
            if self._board[self._finish_row][self._finish_column + index] == "・":
                return
            elif self._board[self._finish_row][self._finish_column + index] != self._finish_piece:
                column_index.append(self._finish_column + index)
            else:
                HasamiShogiGame._capture_right(self, column_index)
                return
            index += 1
        return

    def _capture_up(self, row_index_list):
        """Captures opponent pieces between player's pieces."""
        for index in row_index_list:
            self._board[index][self._finish_column] = "・"
            if self._turn == "BLACK":
                self._red_captured += 1
            elif self._turn == "RED":
                self._black_captured += 1
        return

    def _capture_down(self, row_index_list):
        """Captures opponent pieces between player's pieces."""
        for index in row_index_list:
            self._board[index][self._finish_column] = "・"
            if self._turn == "BLACK":
                self._red_captured += 1
            elif self._turn == "RED":
                self._black_captured += 1
        return

    def _capture_left(self, column_index_list):
        """Captures opponent pieces between player's pieces."""
        for index in column_index_list:
            self._board[self._finish_row][index] = "・"
            if self._turn == "BLACK":
                self._red_captured += 1
            elif self._turn == "RED":
                self._black_captured += 1
        return

    def _capture_right(self, column_index_list):
        """Captures opponent pieces between player's pieces."""
        for index in column_index_list:
            self._board[self._finish_row][index] = "・"
            if self._turn == "BLACK":
                self._red_captured += 1
            elif self._turn == "RED":
                self._black_captured += 1
        return

    def _check_for_win(self):
        """Checks if game has been won if 8 or more pieces have been captured by either player."""
        if self._red_captured >= 8 or self._black_captured >= 8:
            HasamiShogiGame._player_wins(self)
        else:
            HasamiShogiGame._next_turn(self)
        return

    def _player_wins(self):
        """Updates the state of the game when winner has been decided."""
        if self._turn == "BLACK":
            self._state = "BLACK_WON"
            HasamiShogiGame._next_turn(self)
        else:
            self._state = "RED_WON"
            HasamiShogiGame._next_turn(self)
        return

    def _next_turn(self):
        """Updates turn when move has been made."""
        if self._turn == "BLACK":
            self._turn = "RED"
        elif self._turn == "RED":
            self._turn = "BLACK"
        return

    def get_game_state(self):
        """Returns whether the game is unfinished or which side has won."""
        return self._state

    def get_active_player(self):
        """Returns whose turn it is."""
        return self._turn

    def get_num_captured_pieces(self, color):
        """Returns the number of pieces captured by a given color."""
        if str(color).lower() == "black":
            return self._black_captured
        elif str(color).lower() == "red":
            return self._red_captured
        else:
            print("The parameter entered was neither 'BLACK' or 'RED'.")

    def get_square_occupant(self, square):
        """Takes square reference and returns either NONE or the color on it."""
        square_row = square[0].upper()
        square_column = square[1]
        row_value = self._letter[square_row]
        column_value = self._number[square_column]
        if self._board[row_value][column_value] == "歩":
            return "BLACK"
        elif self._board[row_value][column_value] == "と":
            return "RED"
        else:
            return "NONE"


# Special Characters: と, 歩, ・
# A = 0, B = 1, C = 2, D = 3, E = 4, F = 5, G = 6, H = 7, I = 8
# 1 = 0, 2 = 1, 3 = 2, 4 = 3, 5 = 4, 6 = 5, 7 = 6, 8 = 7, 9 = 8

if __name__ == "__main__":
    game = HasamiShogiGame()
    print('The player with the "歩" pieces starts the game.')
    while game.get_game_state() == "UNFINISHED":
        print("Enter the position of the piece you wish to move.")
        start = str(input())
        print("Enter the destination you wish to move your piece.")
        finish = str(input())
        game.make_move(start, finish)
    if game.get_game_state() == "BLACK_WON":
        print("Congratulations 歩 player, you have won!")
    elif game.get_game_state() == "RED_WON":
        print("Congratulations と player, you have won!")