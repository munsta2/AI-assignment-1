from enum import IntEnum


class tile:
    def __init__(self, top, right, bottom, left, number) -> None:
        self.row = -1
        self.col = -1
        self.position_values = [top, right, bottom, left]
        self.open = [True, True, True, True]
        self.number = number

    def minimum(self):
        return min(self.position_values)

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

    def set_position(self, in_row, in_col):
        self.row = in_row
        self.col = in_col


    def __str__(self):
        return str(self.number)


class tile_direction(IntEnum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3
