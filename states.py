import copy
from tile import tile_direction as directions
from tile import tile as tile


#
# function: has_match()
#
# This function takes two tiles and an array
def has_match(tile1, tile2):
    for direction in directions:
        if tile1.open[direction]:
            if tile1.position_values[direction] == tile2.position_values[tile1.get_opposite_direction(direction)]:
                return True
    return False

def find_adjacent(row, col, direction):
    if direction == directions.TOP:
        return row-1, col
    if direction == directions.RIGHT:
        return row, col+1
    if direction == directions.BOTTOM:
        return row+1, col
    if direction == directions.LEFT:
        return row, col-1


class state:
    def __init__(self, in_cost, in_board, in_unplaced) -> None:
        self.heuristic = 0
        self.used_tiles = []
        self.children = []
        self.cost = in_cost
        self.unplaced_tiles = copy.deepcopy(in_unplaced)
        self.board = copy.deepcopy(in_board)

    def add_tile(self, tile, row, col):
        copied_tile = copy.deepcopy(tile)
        copied_tile.set_position(row, col)
        self.used_tiles.append(copied_tile)
        self.unplaced_tiles[copied_tile.number-1] = False
        self.calculate_heuristic()
        self.place_tile_fix_openings(copied_tile, self.board)

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
                        opposite_direction = new_tile.get_opposite_direction(direction)
                        board[new_coordinates[0]][new_coordinates[1]].open[int(opposite_direction)] = False
                    else:
                        new_tile.open[int(direction)] = True
                        # print(new_coordinates, "stays open")

    def add_child(self, tile):
        self.children.append(tile)

    def calculate_heuristic(self):
        self.heuristic = 0
        for tile in self.used_tiles:
            self.heuristic += tile.minimum()

    def copy_used_tiles(self, parents_tiles):
        self.used_tiles = copy.deepcopy(parents_tiles)

    def find_valid_children(self, tile_list, paired_values):
        for usedtile in self.used_tiles:
            if usedtile.has_open_direction() and any(value in usedtile.open_values() for value in paired_values):
                for matched_tile in tile_list:
                    print("Match Test between", usedtile.number, matched_tile.number, has_match(usedtile, matched_tile))
                    if has_match(usedtile, matched_tile) and self.unplaced_tiles[matched_tile.number-1]:
                        connection_check = self.valid_connection(usedtile, matched_tile)
                        print(connection_check)
                        if connection_check[0]:
                            connection_direction = connection_check[1]
                            new_state = state(usedtile.position_values[int(connection_direction)], self.board, self.unplaced_tiles)
                            new_coordinates = find_adjacent(usedtile.row, usedtile.col, connection_direction)
                            new_state.add_tile(matched_tile, new_coordinates[0], new_coordinates[1])
                            self.children.append(new_state)
                            print("Added child by placing", matched_tile.number, "at", new_coordinates)
    
    def valid_connection(self,placed_tile,potential_tile):
        for direction in directions:
            opposite_direction = placed_tile.get_opposite_direction(direction)
            print("Looking to the", direction, placed_tile.position_values[int(direction)], "to find", opposite_direction, potential_tile.position_values[int(opposite_direction)])
            if placed_tile.open[int(direction)] and potential_tile.open[int(opposite_direction)]:
                if placed_tile.position_values[int(direction)] == potential_tile.position_values[int(opposite_direction)]:
                    print("match found babyyyy")
                    return True, direction
        return False, None
    def create_child_state(self):
        pass
