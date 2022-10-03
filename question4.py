import copy
from tile import tile
from states import state
from states import find_adjacent as finderizer
from tile import tile_direction

def main():
    board = []
    tiles = []
    paired_values, board = prepare_problem_from_input_text('input.txt', board, tiles)
    # root = state(0, board)
    # root.add_tile(tiles[0], 0, 0)
    # root.add_tile(tiles[1], 0, 1)
    # print(root.used_tiles[0].open[1])
    print_board(board)


def prepare_problem_from_input_text(file, board, tiles):
    tile_values = []
    with open(file) as topo_file:
        count = 0
        for line in topo_file:
            if count == 0:
                n, m = map(int, line.strip().split(' '))

            else:
                top, right, bottom, left = map(int, line.strip().split(' '))
                tile_values = tile_values + [top, right, bottom, left]
                tiles.append(tile(top, right, bottom, left, count))
            count = count + 1
    board = create_board(n, m, board)
    return find_paired_values(tile_values), board


def find_paired_values(tile_values):
    unique_values = []
    for value in tile_values:
        if tile_values.count(value) == 1:
            unique_values.append(value)
    paired_values = [x for x in tile_values if x not in unique_values]
    paired_values = set(paired_values)
    return paired_values


def create_board(row_size, column_size, board):
    board = [[None] * column_size for i in range(row_size)]
    return board


# def generate_trees(start_tile, board, paired_values):
#     for row in board:
#         for col in row:
#             pass
#
# def create_solution_tree(start_tile, board, paired_values):
#     pass

def print_board(board):
    result = ""
    for row in range(len(board)):
        for col in range(len(board[row])):
            if not board[row][col] is None:
                result += (str(board[row][col].number)) + " "
            else:
                result += "E "
        result += ('\n')
    print(result)


if __name__ == '__main__':
    main()
