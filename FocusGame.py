# Author: Wesley Havens
# Date: November 16th, 2020
# Description: CS162: Portfolio Project: FocusGame

class Player:
    """
    Class definition for a Player object for FocusGame
    """
    def __init__(self, tuple_player):
        """
        Special method __init__ to initialize private data members
        :param tuple_player: Tuple with two elements, argument given by user: ('string name', 'string color')
        _player: Private data member type tuple represents the player name and color
        _captured: Private data member type list, holds captured "pieces" of opposing player
        _reserve: Private data member type list, holds reserve "pieces" of the player
        """
        self._player = tuple_player
        self._captured = []  # initialize a blank list to hold "captured" pieces of opposing player's color
        self._reserve = []   # init blank list to hold reserve pieces for this player

    def get_player(self):
        """Get method to return player (tuple value)"""
        return self._player

    def get_player_name(self):
        """Get method to return player's name (return type string)"""
        return self._player[0]

    def get_player_color(self):
        """Get method to return player's color (return type string)"""
        return self._player[1]

    def add_captured(self, piece):
        """Add method to append game piece to captured pieces list
        arg piece = game piece of opposing player
        """
        self._captured.append(piece)

    def show_captured(self):
        """Get method returns numerical count of captured pieces, zero if the list is empty
        """
        return len(self._captured)

    def add_reserve(self, piece):
        """Add method to append game piece to reserve pieces list
        arg piece = game piece of the player
        """
        self._reserve.append(piece)

    def subtract_reserve(self):
        """Method subtract_reserve returns a reserve piece to be used on the game board,
        and deletes one element from the self._reserve list to account for this.
        """
        temp = self._reserve[0]
        self._reserve.pop()
        return temp

    def show_reserve(self):
        """Get method returns numerical count of reserve pieces, zero if the list is empty
        """
        return len(self._reserve)


class FocusGame:
    """
    Class definition to create an instance of a FocusGame, an abstract board game.
    The game is played by two players an 6x6 board.
    Each player makes one move per turn: Single move, multiple move, or reserved move.
    """
    def __init__(self, tuple_1, tuple_2):
        """
        Special method __init__ to initialize private data members
        tuple_1 contains two values ('player', 'color'), as it was first passed. This will be the first player.
        tuple_2 contains two values ('player', 'color'), initialized to second player.
        _turn: Private data member to keep track of who's turn it is, initialized to first tuple passed as arg
        _board: Private data member representation of game board and pieces
        _current_state: Game state
        """
        self._player_1 = Player(tuple_1)
        self._player_2 = Player(tuple_2)
        self._turn = self._player_1.get_player()  # Set _turn to first tuple argument passed.

        # Initialize game board below, a list of lists to represent rows, columns. Game pieces are also a list.
        self._board = [[] for index in range(6)]
        for i in range(6):  # Initialize game board, first player's (tuple_1) pieces are placed first at 0,0
            if i % 2 == 0:
                self._board[i] = [
                    [tuple_1[1]], [tuple_1[1]], [tuple_2[1]], [tuple_2[1]], [tuple_1[1]], [tuple_1[1]]
                ]
            else:
                self._board[i] = [
                    [tuple_2[1]], [tuple_2[1]], [tuple_1[1]], [tuple_1[1]], [tuple_2[1]], [tuple_2[1]]
                ]

        self._current_state = "UNFINISHED"  # Set game to UNFINISHED


    def win_check(self, player):
        """
        Method to check for two win conditions:
            1) The current player has 6 or more captured pieces
            2) The game board only has one type of "piece" on the top of all occupied spaces.
               As the current player made a move before win_check was called, this "piece" must belong to them.
               Thus, they dominate the game board, and the other player cannot make a move.
        :param player: Current player who made a  move
        :return: True if win condition met
        """
        if player == self._player_1.get_player_name():
            if self._player_1.show_captured() > 5:
                return True  # Win condition met
        elif player == self._player_2.get_player_name():
            if self._player_2.show_captured() > 5:
                return True  # Win condition met

        temp = set()  # Create a blank set to hold values of top-most pieces (no duplicate values this way)
        for list in self._board:         # Iterate through game board's rows
            for item in list:            # Iterate through game board's columns
                if item != []:           # Only consider spots that aren't empty
                    temp.add(item[-1])   # Add the last (top) game piece to the set
        if len(temp) == 1:  # Only one 'color' was found on the topmost piece of every space of game board
            return True      # Win condition met

    def move_piece(self, player=None, tuple_from=None, tuple_to=None, num_pieces=None):
        """
        Method move_piece, attempts to move the piece selected by the player. Validates move, makes move if valid,
        check for win condition, returns status of the move request.
        :param player: Player requesting to make move
        :param tuple_from: Coordinates player requesting to move from
        :param tuple_to:  Coordinates player requesting to move to
        :param num_pieces: Number of pieces player is requesting to move from the "tuple_from" location
        :return: 'successfully moved', or error message if invalid move
        """
        # Call to validate the proposed move
        is_valid_move = self.validate_move(player, tuple_from, tuple_to, num_pieces)

        if is_valid_move is True:  # Move validated
            self.make_move(tuple_from, tuple_to, num_pieces, player)  # Method call to move the piece
            if self.win_check(player) is True:  # A win condition was met
                string = player + ' Wins'
                self._current_state = player + ' Won'
                return string
            else:
                return 'successfully moved'
        else:  # Return error message if not a valid move
            return is_valid_move

    def validate_move(self, player, tuple_from, tuple_to=None, num_pieces=None):
        """
        Method validate_move, calls further sub-methods to validate the player's proposed move.
        :param player: Player requesting to make move
        :param tuple_from: Coordinates player requesting to move from
        :param tuple_to:  Coordinates player requesting to move to,
                          default arg=None [in event called by reserved_move()]
        :param num_pieces: Number of pieces player is requesting to move from the "tuple_from" location,
                           default arg=None [in event called by reserved_move()]
        :return: True if valid move, otherwise return error message relating to why the move is not valid.
        """
        if self.validate_args(player, tuple_from, tuple_to, num_pieces) is False:
            return False  # insufficient number of, or wrong type of args passed
        if self.validate_turn(player) is False:
            return False  # 'not your turn'
        elif self.validate_turn(player) == "gameover":
            return self._current_state
        if self.validate_index_ranges(tuple_from, tuple_to) is False:
            return False  # 'invalid location'
        if tuple_to is None:  # This conditional only checked if reserved_move() called the method validate_move
            if self.validate_has_reserve_in_stock(player) is False:
                return False  # "No pieces in reserve"
        if tuple_to is not None:  # Only check below if move_piece() is called, not checked for reserved_move()
            if self.validate_move_from_is_NOT_empty(tuple_from) is False:
                return False  # 'invalid location'
            if self.validate_top_piece(tuple_from) is False:
                return False  # 'You cant move from here, topmost piece is not yours'
            if self.validate_move_distance(tuple_from, tuple_to, num_pieces) == "NOT_X_OR_Y":
                return False  # 'Invalid move: user tried to move NOT directly up, down, left, or right'
            elif self.validate_move_distance(tuple_from, tuple_to, num_pieces) == "TOOFAR":
                return False  # 'invalid number of pieces'
            elif self.validate_move_distance(tuple_from, tuple_to, num_pieces) == "LESSTHANONE":
                return False  # 'Invalid move: user selected < 1 pieces to move'
        return True

    def validate_turn(self, player):
        """
        Method validate_turn and, to ensure it is the requesting player's turn
        Also checks to make sure game_state is set to "UNFINISHED"
        :param player: Player requesting to make a move
        :return: True if it is the current players turn, false if player requesting move out of turn.
        """
        if self._current_state != "UNFINISHED":
            return 'gameover'
        if self._turn[0] != player:
            return False

    def validate_index_ranges(self, tuple_from, tuple_to=None):
        """ Method to ensure the players move is within the game board
        (Still not necessarily a legal move, further checks to follow)
        :param tuple_from: Coordinates player requesting to move from
        :param tuple_to:  Coordinates player requesting to move to,
                          default arg=None [in event called by reserved_move()]
        :return:
        From and to moves are within range : return True
        Either from or to moves are out of range : return False
        """
        if tuple_to == None:  # This if conditional triggers if reserved_move is making the function call
            reserve_destination = tuple_from  # To avoid confusion switching  "from" and "to"
            # Checking where reserve move is going TO is within the game board
            if reserve_destination[0] < 0 or reserve_destination[0] > len(self._board) - 1:
                return False
            elif reserve_destination[1] < 0 or reserve_destination[1] > len(self._board) - 1:
                return False

        if tuple_from == tuple_to:  # To and from destinations the same
            return False
        # Check rows and columns for FROM location ( acceptable index is 0 through 5):
        elif tuple_from[0] < 0 or tuple_from[0] > len(self._board) - 1:
            return False  # Index range less than zero OR greater than five
        elif tuple_from[1] < 0 or tuple_from[1] > len(self._board) - 1:
            return False
        # Check rows and columns for TO location ( acceptable index is 0 through 5):
        elif tuple_to[0] < 0 or tuple_to[0] > len(self._board) - 1:
            return False
        elif tuple_to[1] < 0 or tuple_to[1] > len(self._board) - 1:
            return False

    def validate_args(self, player, tuple_from, tuple_to, num_pieces):
        """
        Validate move_piece() arguments are of correct types to proceed with other checks,
        Minimum number of args needed to be passed is player and "tuple_from" if reserved_move()
        is making the call
        :return: False if any conditionals below are not cleared
        """
        if isinstance(player, str) is False:
            return False
        if tuple_from is None:
            return False
        if tuple_to is not None and isinstance(tuple_from, tuple) is False:
            return False
        if tuple_from is not None and isinstance(tuple_to, tuple) is False:
            return False
        if tuple_to is not None and num_pieces is None:
            return False
        if tuple_to is not None and isinstance(num_pieces, int) is False:
            return False

    def validate_has_reserve_in_stock(self, player):
        """
        Method validate_has_reserve_in_stock, does just that.
        :param player: Player requesting to make a reserved_move()
        :return: True if player has reserve piece(s) available to make a reserved_move()
                 False if player has no reserve pieces
        """
        if player == self._player_1.get_player_name():
            if self._player_1.show_reserve() == 0:
                return False
        if player == self._player_2.get_player_name():
            if self._player_2.show_reserve() == 0:
                return False

    def validate_move_from_is_NOT_empty(self, tuple_from):
        """
        Method validate_move_from_is_NOT_empty, validates the FROM location has a game piece to move.
        :param tuple_from: Coordinates where game piece would be moving from
        :return: True if this coordinate has piece(s) to move, False if the coordinate is empty.
        """
        if self._board[tuple_from[0]][tuple_from[1]] == []:
            return False

    def validate_top_piece(self, tuple_from):
        """
        Method validate_top_piece, checks the top piece and ensures it belongs to the player who's turn it is to move.
        :param tuple_from:  Coordinates where game piece would be moving from
        :return: True if the top piece belongs to the player whose turn it is
                 False if the top piece does not belong to them
        """
        if self._board[tuple_from[0]][tuple_from[1]][-1] not in self._turn:
            return False

    def validate_move_distance(self, tuple_from, tuple_to, num_pieces):
        """
        Method validate_move_distance, Checks to ensure the proposed move is only along either the X axis or Y axis.
        (up, down, left, right), then ensures the distance the player is requesting to move is exactly equivalent
        to the number of pieces they also wish to move.
        Finally validates the number of pieces proposed to move is not greater than the number of pieces that exist
        at the FROM location.
        :param tuple_from: Coordinates player requesting to move from
        :param tuple_to:  Coordinates player requesting to move to
        :param num_pieces: Number of pieces player is requesting to move from the "tuple_from" location
        :return: True if all conditionals passed.
                 Error type string depending on which conditional failed.
        """
        if tuple_from[0] != tuple_to[0] and tuple_from[1] != tuple_to[1]:
            return "NOT_X_OR_Y"  # From and to: either the y axis (rows), or x axis (columns) must match
            # to maintain only moving up, down, left or right.

        if tuple_from[0] == tuple_to[0]:  # rows match, check move distance for columns:
            request_distance = abs(tuple_from[1] - tuple_to[1])  # Distance user is requesting to move
            if request_distance != num_pieces:
                return "TOOFAR"
        elif tuple_from[1] == tuple_to[1]:  # columns match, check move distance for rows:
            request_distance = abs(tuple_from[0] - tuple_to[0])  # Distance user is requesting to move
            if request_distance != num_pieces:
                return "TOOFAR"

        # the length of the list (stack of pieces) that exists at the specified move from position on the board:
        move_length = len(self._board[tuple_from[0]][tuple_from[1]])  # maximum move distance is move_length
        if num_pieces > move_length:
            return "TOOFAR"  # Requested num_pieces to move is greater than the stack of game pieces
        if num_pieces < 1:
            return "LESSTHANONE"  # or user requested to move <= 0 pieces

    def make_move(self, tuple_from, tuple_to, num_pieces, player):
        """
        Method to make_move after conditionals cleared, switches player turns after the move is made
        :param player: Current player
        :param tuple_from: Where the piece(s) piece will be taken from
        :param tuple_to: Where the piece(s) will be placed
        """
        slice = len(self._board[tuple_from[0]][tuple_from[1]]) - num_pieces
        temp_list = self._board[tuple_from[0]][tuple_from[1]][slice:]  # Slicing operation to obtain pieces to move
        for item in temp_list:  # Iterate through this temp list and add them to end of the destination game piece
            self._board[tuple_to[0]][tuple_to[1]].append(item)
        self.check_stack(tuple_to, player)  # check destination game piece in event it is now > 5 pieces

        # Removes the now duplicate piece(s) that were moved TO another stack from the FROM stack:
        slice_subtract = len(self._board[tuple_from[0]][tuple_from[1]]) - num_pieces
        self._board[tuple_from[0]][tuple_from[1]] = self._board[tuple_from[0]][tuple_from[1]][:slice_subtract]
        self.switch_turns(player)

    def reserved_move(self, player, tuple_to):
        """
        Method reserved_move, first validates the proposed move.
        Then calls self.make_reserved_move if the move is validated.
        Next calls self.win_check to check for win conditions.
        :param player: Current player
        :param tuple_to: Where the reserve piece is proposed to be moved to
        :return 'successfully moved' if valid move made, otherwise returns error message of type of error encountered
        """
        is_valid_move = self.validate_move(player, tuple_to) #  validate move before making it
        if is_valid_move is True:
            self.make_reserved_move(player, tuple_to)
            if self.win_check(player) is True:
                string = player + ' Wins'
                self._current_state = player + ' Won'
                return string
            else:
                return 'successfully moved'
        else:  # Reserved move wasn't valid, return reason why not
            return is_valid_move

    def make_reserved_move(self, player, tuple_to):
        """
        Method to make_reserved_move after conditionals cleared, switches player turns after the move is made
        :param player: Current player
        :param tuple_to: Where the reserve piece will be placed
        """
        if player == self._player_1.get_player_name():  # Subtract reserve piece from correct player's reserve list
            item = self._player_1.subtract_reserve()
        else:
            item = self._player_2.subtract_reserve()
        self._board[tuple_to[0]][tuple_to[1]].append(item)  # Append reserve piece to the location given
        self.check_stack(tuple_to, player)  # Check this location to handle if its now >5 game pieces
        self.switch_turns(player)

    def check_stack(self, tuple_to, player):
        """
        Method check stack, handles sending pieces to the player's captured or reserved lists.
        Updates the game board piece location to account for pieces sent to reserve or captured.
        :param tuple_to: Check the destination game piece if > 5 pieces in length
        :param player: The current player who made the move
        """
        if len(self._board[tuple_to[0]][tuple_to[1]]) > 5:
            num_items_to_remove = len(self._board[tuple_to[0]][tuple_to[1]]) - 5
            for item in range(num_items_to_remove):
                temp_piece = self._board[tuple_to[0]][tuple_to[1]][item]
                self.to_reserve(temp_piece, player)  # To remove this ###################???
            self._board[tuple_to[0]][tuple_to[1]] = self._board[tuple_to[0]][tuple_to[1]][num_items_to_remove:]

    def to_reserve(self, temp_piece, player):
        """
        Method called to send a single game piece to correct player's reserve when a game
        piece is > 5 pieces in length. If the piece doesn't belong to the current player, the piece is instead send to
        their list of captured pieces
        :param temp_piece: Piece to be added to reserve or captured
        :param player: Player who made the move.
        :return:
        """

        if player == self._player_1.get_player_name():  # current player is player 1
            if temp_piece == self._player_1.get_player_color():
                self._player_1.add_reserve(temp_piece)
            else:
                self._player_1.add_captured(temp_piece)
        elif player == self._player_2.get_player_name():  # current player is player 2
            if temp_piece == self._player_2.get_player_color():
                self._player_2.add_reserve(temp_piece)
            else:
                self._player_2.add_captured(temp_piece)

    def switch_turns(self, player):
        """Method to change turns after a successful player move
        :param player: Player who made the move.
        """
        if player == self._player_1.get_player_name():
            self._turn = self._player_2.get_player()
        elif player == self._player_2.get_player_name():
            self._turn = self._player_1.get_player()

    def show_pieces(self, coords):
        """
        A method named `show_pieces` takes a position on the board and returns a list showing the pieces that are
        present at that location with the bottom-most pieces at the 0th index of the array and other pieces on
        it in ascending order.
        """
        if coords[0] < 0 or coords[0] > len(self._board) - 1:
            return "Invalid index"
        elif coords[1] < 0 or coords[1] > len(self._board) - 1:
            return "Invalid index"
        return self._board[coords[0]][coords[1]]

    def show_reserve(self, player_name):
        """
        takes the player name as the parameter and shows the count
        of pieces that are in reserve for the player. If no pieces are in reserve, return 0.
        """
        if player_name == self._player_1.get_player_name():
            return self._player_1.show_reserve()
        elif player_name == self._player_2.get_player_name():
            return self._player_2.show_reserve()

    def show_captured(self, player_name):
        """
        Takes the player name as the parameter and shows the number of pieces captured by that player.
        If no pieces have been captured, return 0.
        """
        if player_name == self._player_1.get_player_name():
            return self._player_1.show_captured()
        elif player_name == self._player_2.get_player_name():
            return self._player_2.show_captured()
