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
            if tile1.position_values[direction] == tile2.position_values[tile.get_opposite_direction(direction)]:
                return True
    return False


class state:
    def __init__(self, ) -> None:
        self.heuristic
        self.used_tiles = []
        self.children = []

    def add_tile(self, tile):
        self.used_tiles.append(tile)

    def add_child(self, tile):
        self.children.append(tile)

    def calculate_heuristic(self):
        self.heuristic = 0
        for tile in self.used_tiles:
            self.heuristic += tile.minimum()

    def copy_used_tiles(self, parents_tiles):
        self.used_tiles = copy.deepcopy(parents_tiles)

    def find_valid_children(self, tile_list, paired_values):
        for usedtile in self.usedtile:
            if usedtile.has_open_direction() and any(value in usedtile.open_values() for value in paired_values):
                for matched_tile in tile_list:
                    if has_match(usedtile, matched_tile):
                        self.children.append(matched_tile)



