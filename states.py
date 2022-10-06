import copy
from tile import TileDirection as Directions
from tile import get_opposite_direction


def has_match(tile1, tile2):
    """Function:   has_match()
    This static function takes two tiles and return true if there are open facings opposite of each other
    that have the same value"""
    for direction in Directions:
        if tile1.open[direction]:
            if tile1.position_values[direction] == tile2.position_values[get_opposite_direction(direction)]:
                return True
    return False


def find_adjacent(row, col, direction):
    """Function:   find_adjacent()
    This static function takes a board position and returns the adjacent position in the
    specified direction. This function can return positions outside the board.
    Returns an array of size 2 containing integers for the row and column positions"""
    if direction == Directions.TOP:
        return row - 1, col
    if direction == Directions.RIGHT:
        return row, col + 1
    if direction == Directions.BOTTOM:
        return row + 1, col
    if direction == Directions.LEFT:
        return row, col - 1


class State:
    """Class:  state()
    The state class represents a valid state of the board when solving the tile placement game. It stores a unique copy
    of tile objects in the used_tile list. The unplaced_tiles list is a unique list of boolean values that correspond
    to the list of tile objects created on the problem's initialization.
    """

    def __init__(self, in_cost, in_used, in_board, in_unplaced) -> None:
        self.heuristic = 0
        self.used_tiles = copy.deepcopy(in_used)  # List of Tile Objects representing placed tiles
        self.children = []  # List of State Objects
        self.cost = in_cost
        self.unplaced_tiles = copy.deepcopy(in_unplaced)  # List of Booleans representing unplaced tiles
        self.board = copy.deepcopy(in_board)  # 2D Array of Tiles

    def add_tile(self, tile, row, col, tile_object_list, paired_values):
        """Function:   add_tile()
        This function takes a tile object and the desired position. It generates a copy of the tile to be modified for
        the specific states. It adds the tile to the used_tile list and updates the reference list of unplaced_tiles.
        With the new tile added it will update the states calculated heuristic and place the tile on the states board,
        updating tile facings as needed."""
        copied_tile = copy.deepcopy(tile)
        copied_tile.set_position(row, col)
        self.used_tiles.append(copied_tile)
        self.unplaced_tiles[copied_tile.number - 1] = False
        self.calculate_heuristic(tile_object_list, paired_values)
        self.place_tile_fix_openings(copied_tile, self.board)

    # TODO: Separate this into two separate functions?
    def place_tile_fix_openings(self, new_tile, board):
        """ Function:   place_tile_fix_openings()
        This function takes in a tile object with initialized coordinates and a board. It places the tile on the board
        and checks adjacent spaces of each tile face to see if the openings should be closed. If it is adjacent to
        another tile, the adjacent tile is checked to ensure the correct tile face opening is also closed."""
        board[new_tile.row][new_tile.col] = new_tile
        for direction in Directions:
            if new_tile.open[int(direction)]:
                new_coordinates = find_adjacent(new_tile.row, new_tile.col, direction)
                if not 0 <= new_coordinates[0] < len(board) or not 0 <= new_coordinates[1] < len(board[new_coordinates[0]]):
                    new_tile.open[int(direction)] = False
                else:
                    if not (board[new_coordinates[0]][new_coordinates[1]] is None):
                        new_tile.open[int(direction)] = False
                        opposite_direction = get_opposite_direction(direction)
                        board[new_coordinates[0]][new_coordinates[1]].open[int(opposite_direction)] = False
                    else:
                        new_tile.open[int(direction)] = True

    def calculate_heuristic(self, tile_object_list, paired_values):
        """Function:   calculate_heuristic()
        This function iterates through the states unplaced tile list and estimates the minimum possible
        value to arrive at the goal state where all tiles are placed. The Heuristic is calculated by taking all
        unplaced tile's minimum face value and calculating the sum. Sets the state's heuristic variable
        to the calculated value."""
        self.heuristic = 0
        for i in range(len(self.unplaced_tiles)):
            if self.unplaced_tiles[i]:  # Tile has not been placed if true
                possible_values = []
                for value in tile_object_list[i].open_values():
                    if value in paired_values:
                        possible_values.append(value)
                self.heuristic += min(possible_values)

    def find_valid_children(self, tile_object_list, paired_values):
        """Function:   find_valid_children()
        This function finds all possible combinations of new states by checking if available tiles can be placed on all
        currently placed tiles on the board. First checks the existing placed tiles to see if a tile facing is open, and
        if that facing has a value that has a pairing. If it has a potential pairing, and that potential paired tile has
        not been placed yet, we then check if faces of the connection to ensure they are open and the numbers match.
        Should all these constraints be valid, a new state is generated and is placed in the current state's child list
        at a cost of the connection."""
        for usedtile in self.used_tiles:
            if usedtile.has_open_direction():  # Check to see there is an open space around the tile
                if usedtile.are_open_directions_paired(paired_values):  # Does the open space have a potential pair
                    # Unplaced tiles is a list the length of the total amount of tiles
                    # It tracks which tiles have been placed by assigning False to the index corresponding
                    # to a placed tile. We can use this to only test tiles that haven't been placed.
                    for i in range(len(self.unplaced_tiles)):
                        if self.unplaced_tiles[i]:
                            # test if a tile on the board can match with one corresponding unused tile
                            if has_match(usedtile, tile_object_list[i]):
                                # If there is a potential match, finally iterate through all possible directions
                                connection_check = self.valid_connection(usedtile, tile_object_list[i])
                                # Connection check will hold a boolean if there was a valid connection
                                # and all possible directions to add (if a tile has a valid connection
                                # in multiple directions)
                                if connection_check[0]:
                                    for connection_direction in connection_check[1]:
                                        # Find the coordinates where we want to place the valid connected tile
                                        # and test to make sure it's empty
                                        new_coordinates = find_adjacent(usedtile.row, usedtile.col,
                                                                        connection_direction)
                                        if self.board[new_coordinates[0]][new_coordinates[1]] is None:
                                            # Generate the new state when the new tile is placed and add it to
                                            # the current states children
                                            new_state = State(
                                                usedtile.position_values[int(connection_direction)] + self.cost,
                                                self.used_tiles, self.board, self.unplaced_tiles)
                                            new_state.add_tile(tile_object_list[i], new_coordinates[0],
                                                               new_coordinates[1], tile_object_list, paired_values)
                                            self.children.append(new_state)

    def valid_connection(self, placed_tile, potential_tile):
        """Function:   valid_connection()
        This function compares the opposite direction of two tiles to ensure they are open, and the values match.
        Returns an array of size 2. The first index is a boolean if the two tiles can be connected,
        the second index is a list with all valid direction of the pairing relative to the already placed_tile."""
        valid_directions = []
        found_valid = False
        for direction in Directions:
            opposite_direction = get_opposite_direction(direction)
            # If the opposite edges are considered open for each tile object
            if placed_tile.open[int(direction)] and potential_tile.open[int(opposite_direction)]:
                # If the edge values are equal for the opposite directions
                if placed_tile.position_values[int(direction)] == potential_tile.position_values[int(opposite_direction)]:
                    found_valid = True
                    valid_directions.append(direction)
        return found_valid, valid_directions
