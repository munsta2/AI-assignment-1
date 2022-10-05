from enum import IntEnum

'''
Function:   get_opposite_direction()
This static function takes in a direction enum and returns the opposite direction.
Returns a direction enum that is the opposite of the input parameter
'''
def get_opposite_direction(input_direction):
    if input_direction == tile_direction.TOP:
        return tile_direction.BOTTOM
    if input_direction == tile_direction.RIGHT:
        return tile_direction.LEFT
    if input_direction == tile_direction.BOTTOM:
        return tile_direction.TOP
    if input_direction == tile_direction.LEFT:
        return tile_direction.RIGHT

'''
Class:  tile()
The tile class represents a tile in the problem. It's number depends on the order it was parsed by the input file.
It contains a value for each tile facing, holds it's position on the board, and tracks if tile face
is not on the edge of the board and if that space is unoccupied.
'''
class tile:
    def __init__(self, top, right, bottom, left, number) -> None:
        self.row = -1
        self.col = -1
        self.position_values = [top, right, bottom, left]
        self.open = [True, True, True, True]
        self.number = number

    '''
    Function:   tile.minimum()
    This function finds the smallest value of each of the tiles facing.
    Returns an integer for minimum value of the facings
    '''
    def minimum(self):
        return min(self.position_values)

    '''
    Function:   tile.open_values()
    This function finds which facings are available and returns a list of the values of those facings
    Returns a list of integers for the facings that are available
    '''
    def open_values(self):
        values = []
        if self.open[int(tile_direction.TOP)]:
            values.append(self.position_values[int(tile_direction.TOP)])
        if self.open[int(tile_direction.RIGHT)]:
            values.append(self.position_values[int(tile_direction.RIGHT)])
        if self.open[int(tile_direction.BOTTOM)]:
            values.append(self.position_values[int(tile_direction.BOTTOM)])
        if self.open[int(tile_direction.LEFT)]:
            values.append(self.position_values[int(tile_direction.LEFT)])
        return values

    '''
    Functions:  tile.has_open_direction()
    This function checks the tile to see if at least one of the tile facings are open
    Returns true if one of the tile facings are open
    '''
    def has_open_direction(self):
        return max(self.open)

    '''
    Function:   tile.set_position()
    This function sets the integer position variables of the tile to the specified integer parameters
    '''
    def set_position(self, in_row, in_col):
        self.row = in_row
        self.col = in_col

    # '''
    # Function:   override __str__
    # This functions overrides the default print function and returns
    # the tile number as a string when printing a tile object.
    # '''
    # def __str__(self):
    #     return str(self.number)

    def are_open_directions_paired(self, paired_values):
        for value in self.open_values():
            if value in paired_values:
                return True
        return False


'''
Class:  tile_direction()
This class is an enum that equates the direction of a tile to an integer value.
This is useful when having to access list indices. A list of size 4 will have each
index represented by a direction (0-3).
'''
class tile_direction(IntEnum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3
