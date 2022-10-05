import copy
from tile import tile_direction as directions
from tile import tile as tile
from tile import get_opposite_direction


'''
Function:   has_match()
This static function takes two tiles and return true if there are open facings opposite of eachother
that have the same value
'''
def has_match(tile1, tile2):
    for direction in directions:
        if tile1.open[direction]:
            if tile1.position_values[direction] == tile2.position_values[get_opposite_direction(direction)]:
                return True
    return False

'''
Function:   find_ajacent()
This static function takes a board position and returns the adjacent position in the
specified direction. This function can return positions outside the board.
Returns an array of size 2 containing integers for the row and column positions
'''
def find_adjacent(row, col, direction):
    if direction == directions.TOP:
        return row-1, col
    if direction == directions.RIGHT:
        return row, col+1
    if direction == directions.BOTTOM:
        return row+1, col
    if direction == directions.LEFT:
        return row, col-1

'''
Class:  state()
'''
class state:
    def __init__(self, in_cost, in_used, in_board, in_unplaced) -> None:
        self.heuristic = 0
        self.used_tiles = copy.deepcopy(in_used) #List of Tile Objects representing placed tiles
        self.children = [] #List of State Objects
        self.cost = in_cost
        self.unplaced_tiles = copy.deepcopy(in_unplaced) #List of Booleans representing unplaced tiles
        self.board = copy.deepcopy(in_board) #2D Array of Tiles
    '''
    Function:   add_tile()
    This function takes a tile object and the desired position. It generates a copy of the tile to be modified for
    the specific states. It adds the tile to the used_tile list and updates the reference list of unplaced_tiles.
    With the new tile added it will update the states calculated heuristic and place the tile on the states board,
    updating tile facings as needed.
    '''
    def add_tile(self, tile, row, col, tile_object_list):
        copied_tile = copy.deepcopy(tile)
        copied_tile.set_position(row, col)
        self.used_tiles.append(copied_tile)
        self.unplaced_tiles[copied_tile.number-1] = False
        self.calculate_heuristic(tile_object_list)
        self.place_tile_fix_openings(copied_tile, self.board)

    '''
    Function:   place_tile_fix_openings()
    This function takes in a tile object with initialized coordinates and a board. It places the tile on the board
    and checks adjacent spaces of each tile face to see if the openings should be closed. If it is adjacent to another
    tile, the adjacent tile is checked to ensure the correct tile face opening is also closed.
    '''
    #TODO: Seperate this into two seperate functions?
    def place_tile_fix_openings(self, new_tile, board):
        board[new_tile.row][new_tile.col] = new_tile
        for direction in directions:
            if new_tile.open[int(direction)]:
                new_coordinates = find_adjacent(new_tile.row, new_tile.col, direction)
                if not 0 <= new_coordinates[0] < len(board[0]) or not 0 <= new_coordinates[1] < len(board):
                    new_tile.open[int(direction)] = False
                    # print(new_coordinates, "out of board")
                else:
                    if not (board[new_coordinates[0]][new_coordinates[1]] is None):
                        # print(new_coordinates, "found adjacent tile")
                        new_tile.open[int(direction)] = False
                        opposite_direction = get_opposite_direction(direction)
                        board[new_coordinates[0]][new_coordinates[1]].open[int(opposite_direction)] = False
                    else:
                        new_tile.open[int(direction)] = True
                        # print(new_coordinates, "stays open")
    '''
    Function:   add_child()
    '''
    #TODO: Handled in find_valid_children? Will we be adding children outside of calling state functions?
    def add_child(self, tile):
        self.children.append(tile)

    '''
    Function:   calculate_heuristic()
    This function iterates through the states used_tiles list and estimates the minimum possible value to arrive at the
    current state by taking the minimum value of each tile face and calculating the sum. Sets the state's heuristic
    variable to the calculate value.
    '''
    def calculate_heuristic(self, tile_object_list):
        self.heuristic = 0
        # for tile in self.used_tiles:
        #     self.heuristic += tile.minimum()
        for i in range(len(self.unplaced_tiles)):
            if self.unplaced_tiles[i]: # Tile has not been placed if true
                self.heuristic += tile_object_list[i].minimum()



    '''
    Function:   copy_used_tiles()
    '''
    # TODO Handled in state constructor already?
    def copy_used_tiles(self, parents_tiles):
        self.used_tiles = copy.deepcopy(parents_tiles)

    '''
    Function:   find_valid_children()
    This function finds all possible combinations of new states by checking if available tiles can be placed on all
    currently placed tiles on the board. First checks the existing placed tiles to see if a tile facing is open, and if
    that facing has a value that has a pairing. If it has a potential pairing, and that potential paired tile has
    not been placed yet, we then check if faces of the connection to ensure they are open and the numbers match.
    Should all these constraints be valid, a new state is generated and is placed in the current states child list
    at a cost of the connection.
    
    '''
    def find_valid_children(self, tile_object_list, paired_values):
        # print("Amount of used tiles in this state", len(self.used_tiles))
        for usedtile in self.used_tiles:
            # print("Checking conections for tile", usedtile.number, "Open board around tile?:", usedtile.has_open_direction())
            if usedtile.has_open_direction():
                if usedtile.are_open_directions_paired(paired_values):
                    for i in range(len(self.unplaced_tiles)):
                        if self.unplaced_tiles[i]:
                            if has_match(usedtile, tile_object_list[i]):
                                connection_check = self.valid_connection(usedtile, tile_object_list[i])
                                if connection_check[0]:
                                    for connection_direction in connection_check[1]:
                                        new_state = state(usedtile.position_values[int(connection_direction)]+self.cost, self.used_tiles, self.board, self.unplaced_tiles)
                                        new_coordinates = find_adjacent(usedtile.row, usedtile.col, connection_direction)
                                        new_state.add_tile(tile_object_list[i], new_coordinates[0], new_coordinates[1], tile_object_list)
                                        print("New State Found by attaching", usedtile.number, "to", tile_object_list[i].number, "at", new_coordinates, connection_direction)
                                        self.children.append(new_state)

    
    '''
    Function:   valid_conection()
    This function compares the opposite direction of two tiles to ensure they are open, and the values match. Returns
    an array of size 2. The first index is a boolean if the two tiles can be connected, the second index is the
    direction of the pairing relative to the placed_tile.
    '''
    def valid_connection(self,placed_tile,potential_tile):
        valid_directions = []
        found_valid = False
        for direction in directions:
            opposite_direction = get_opposite_direction(direction)
            #print("Looking to the", direction, placed_tile.position_values[int(direction)], "to find", opposite_direction, potential_tile.position_values[int(opposite_direction)])
            if placed_tile.open[int(direction)] and potential_tile.open[int(opposite_direction)]:
                if placed_tile.position_values[int(direction)] == potential_tile.position_values[int(opposite_direction)]:
                    #print("match found babyyyy")
                    found_valid = True
                    valid_directions.append(direction)
        return found_valid, valid_directions
