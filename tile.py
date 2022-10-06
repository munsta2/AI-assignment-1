from enum import IntEnum


def get_opposite_direction(input_direction):
    """
    Function:   get_opposite_direction()
    This static function takes in a direction enum and returns the opposite direction.
    Returns a direction enum that is the opposite of the input parameter
    """
    if input_direction == TileDirection.TOP:
        return TileDirection.BOTTOM
    if input_direction == TileDirection.RIGHT:
        return TileDirection.LEFT
    if input_direction == TileDirection.BOTTOM:
        return TileDirection.TOP
    if input_direction == TileDirection.LEFT:
        return TileDirection.RIGHT


class Tile:
    """
    Class:  tile()
    The tile class represents a tile in the problem. It's number depends on the order it was parsed by the input file.
    It contains a value for each tile facing, holds its position on the board, and tracks if tile face
    is not on the edge of the board and if that space is unoccupied.
    """
    def __init__(self, top, right, bottom, left, number) -> None:
        self.row = -1
        self.col = -1
        self.position_values = [top, right, bottom, left]
        self.open = [True, True, True, True]
        self.number = number

    def minimum(self):
        """
        Function:   tile.minimum()
        This function finds the smallest value of each of the tiles facing.
        Returns an integer for minimum value of the facings
        """
        return min(self.position_values)

    def open_values(self):
        """
        Function:   tile.open_values()
        This function finds which facings are available and returns a list of the values of those facings
        Returns a list of integers for the facings that are available
        """
        values = []
        if self.open[int(TileDirection.TOP)]:
            values.append(self.position_values[int(TileDirection.TOP)])
        if self.open[int(TileDirection.RIGHT)]:
            values.append(self.position_values[int(TileDirection.RIGHT)])
        if self.open[int(TileDirection.BOTTOM)]:
            values.append(self.position_values[int(TileDirection.BOTTOM)])
        if self.open[int(TileDirection.LEFT)]:
            values.append(self.position_values[int(TileDirection.LEFT)])
        return values

    def has_open_direction(self):
        """
        Functions:  tile.has_open_direction()
        This function checks the tile to see if at least one of the tile facings are open
        Returns true if one of the tile facings are open
        """
        return max(self.open)

    def set_position(self, in_row, in_col):
        """
        Function:   tile.set_position()
        This function sets the integer position variables of the tile to the specified integer parameters
        """
        self.row = in_row
        self.col = in_col

    def are_open_directions_paired(self, paired_values):
        for value in self.open_values():
            if value in paired_values:
                return True
        return False


class TileDirection(IntEnum):
    """
    Class:  tile_direction()
    This class is an enum that equates the direction of a tile to an integer value.
    This is useful when having to access list indices. A list of size 4 will have each
    index represented by a direction (0-3).
    """
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3
