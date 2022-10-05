import copy
import sys

from tile import tile
from states import state
from tile import tile_direction


def main():
    tile_objects = []
    paired_values, board = prepare_problem_from_input_text('input.txt', tile_objects)
    board_size = len(board) * len(board[0])
    unplaced_tiles = [True] * board_size
    for row in range(len(board)):
        for col in range(len(board[row])):
            test = A_star(row, col, board, tile_objects, paired_values, unplaced_tiles)
            print(int(test))


'''
Function:   A_star()
'''
def A_star(row, col, board, tiles, paired_values, unplaced_tiles):
    root = state(0, [], board, unplaced_tiles)
    root.add_tile(tiles[0], row, col, tiles)
    print("Root Board")
    print_board(root.board)
    return(a_star_helper(root, tiles, paired_values))


'''
Function:   a_star_helper()
'''
def a_star_helper(state, tile_objects, paired_values):
    state.find_valid_children(tile_objects, paired_values)
    if not any(state.unplaced_tiles):
        return state.cost
    if not state.children and any(state.unplaced_tiles):
        return sys.maxsize
    child_cost = []
    opened_children = [False] * len(state.children)
    for child in state.children:
        child_cost.append(child.heuristic + child.cost)
    min_value = min(child_cost)
    min_index = child_cost.index(min_value)
    print("is our best guess, cost to get here", state.children[min_index].cost)
    print_board(state.children[min_index].board)
    true_cost = a_star_helper(state.children[min_index], tile_objects, paired_values)
    opened_children[min_index] = True
    repeat = True
    while repeat:
        repeat = False
        next_child = None
        for i in range(len(state.children)):
            if true_cost > (state.children[i].heuristic + state.children[i].cost) and not opened_children[i]:
                print("Found better alternative", opened_children, "child index", i)
                next_child = state.children[i]
                next_child_index = i
                repeat = True
        if next_child:
            print("Opening this alternative")
            print_board(next_child.board)
            true_cost = a_star_helper(next_child, tile_objects, paired_values)
            opened_children[next_child_index] = True
    return true_cost


'''
Function:   prepare_problem_from_input_text()
This function takes in an input file and parses the dimensions of our board. It then parses the tile values
and generates an object to represent each tile. It calls create_board() to set the
game board to the correct dimensions.
Returns a list of integers for all tile values that have at least 1 pairing and the prepared board
'''
def prepare_problem_from_input_text(file, tiles):
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
    board = create_board(n, m)
    return find_paired_values(tile_values), board


'''
Function:   find_paired_values()
This function takes in a list of integers and returns a list containing the integers
that are not-unique (list contains the number at least twice).
Returns a list of integers for non-unique values
'''
def find_paired_values(tile_values):
    unique_values = []
    for value in tile_values:
        if tile_values.count(value) == 1:
            unique_values.append(value)
    paired_values = [x for x in tile_values if x not in unique_values]
    paired_values = set(paired_values)
    return paired_values


'''
Function:   create_board()
This function takes in a board object (2d array) and sets the board to the specified dimensions
Returns a 2d array of Null (None) Objects of the requested dimensions
'''
def create_board(row_size, column_size):
    board = [[None] * column_size for i in range(row_size)]
    return board


'''
Function:   print_board()
This function takes in a board and iterates through the array, visualizing the state of the board.
The tiles are represented by the tile number and empty spaces are represented by 'E'
'''
def print_board(board):
    result = ""
    for row in range(len(board)):
        for col in range(len(board[row])):
            if not board[row][col] is None:
                result += (str(board[row][col].number)) + " "
            else:
                result += "E "
        result += '\n'
    print(result)


if __name__ == '__main__':
    main()
