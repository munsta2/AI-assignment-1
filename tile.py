from enum import Enum


class tile:
    def __init__(self, top, right, bottom, left, number) -> None:
        self.position_values = [top, right, bottom, left]
        self.open = [True, True, True, True]
        self.number = number

    def minimum(self):
        return min(self.top, self.right, self.bottom, self.left)

    def open_values(self):
        values = []
        if self.open(tile_direction.TOP):
            values.append(self.position_values(tile_direction.TOP))
        if self.open(tile_direction.RIGHT):
            values.append(self.position_values(tile_direction.RIGHT))
        if self.open(tile_direction.BOTTOM):
            values.append(self.position_values(tile_direction.BOTTOM))
        if self.open(tile_direction.LEFT):
            values.append(self.position_values(tile_direction.LEFT))
        return values

    def has_open_direction(self):
        for direction in self.open:
            if direction:
                return True
        return False

    def get_opposite_direction(self, input_direction):
        if input_direction == tile_direction.TOP:
            return tile_direction.BOTTOM
        if input_direction == tile_direction.RIGHT:
            return tile_direction.LEFT
        if input_direction == tile_direction.BOTTOM:
            return tile_direction.TOP
        if input_direction == tile_direction.LEFT:
            return tile_direction.RIGHT


    def __str__(self):
        return str(self.number)


class tile_direction(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3
