import sys
import timeit
from tile import Tile
from states import State


def main():
    start = timeit.default_timer()
    sys.setrecursionlimit(5000)
    tile_objects = []
    paired_values, board = prepare_problem_from_input_text('input.txt', tile_objects)
    # board_size = len(board) * len(board[0])
    # unplaced_tiles = [True] * board_size
    # Creating a list of booleans equal in length to the number of tiles to reference to check
    # if a tile has been placed
    unplaced_tiles = [True] * len(tile_objects)

    final_values = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            result = A_star(row, col, board, tile_objects, paired_values, unplaced_tiles)
            final_values.append(result)

    if min(final_values) >= sys.maxsize:
        print("No valid solutions for problem")
    else:
        print("Lowest Solution Found", min(final_values))

    stop = timeit.default_timer()
    print('Time: ', stop - start)


def A_star(row, col, board, tiles, paired_values, unplaced_tiles):
    """
    Function:   A_star()
    """
    root = State(0, [], board, unplaced_tiles)
    root.add_tile(tiles[0], row, col, tiles, paired_values)
    print("Trying Start Position:", [row, col])
    # print_board(root.board)
    fringe_children = []
    return a_star_helper(root, tiles, paired_values, fringe_children)


def a_star_helper(in_state, tile_objects, paired_values, fringe_children):
    """
    Function:   a_star_helper()
    a_star_helper() is a recursive function that searches each fringe child based on a fringe node where the state
    has the lowest f(n) value, that is where the cost + heuristic is the least
    """
    in_state.find_valid_children(tile_objects, paired_values)
    # Base Cases
    if not any(in_state.unplaced_tiles):  # All tiles have been placed
        print("Possible Solution Found, cost:", in_state.cost)
        print_board(in_state.board)
        return in_state.cost
    if not in_state.children and any(in_state.unplaced_tiles):  # No children possible, not all tiles placed
        return sys.maxsize

    # Keep track of children in the fringes
    if not fringe_children:
        fringe_children = fringe_children + in_state.children
    else:
        # Test if a child in the fringe is identical in tile placement
        # of a possible child of the current state. This is an aggressive tree trimming
        # TODO: Note that just because the board looks the same, doesn't mean the cost to arrive at that state
        #  is the same. May need to adjust this logic if the trimming of the tree is too greedy
        identity_list = []
        for fringe in fringe_children:
            identity_list.append(identify_board(fringe.board))
        for child in in_state.children:
            if not identify_board(child.board) in identity_list:
                fringe_children.append(child)

    # Find the best fringe to expand based on cost and heuristic
    min_fringe = fringe_children[0]
    for child in fringe_children:
        if child.cost + child.heuristic < min_fringe.cost + min_fringe.heuristic:
            min_fringe = child
        elif child.cost + child.heuristic == min_fringe.cost + min_fringe.heuristic:
            if child.heuristic < min_fringe.heuristic:
                min_fringe = child
    fringe_children.remove(min_fringe)
    # print("Trying Fringe")
    # print_board(min_fringe.board)
    return a_star_helper(min_fringe, tile_objects, paired_values, fringe_children)


def prepare_problem_from_input_text(file, tiles):
    """
    Function:   prepare_problem_from_input_text()
    This function takes in an input file and parses the dimensions of our board. It then parses the tile values
    and generates an object to represent each tile. It calls create_board() to set the
    game board to the correct dimensions.
    Returns a list of integers for all tile values that have at least 1 pairing and the prepared board
    """
    tile_values = []
    with open(file) as topo_file:
        count = 0
        for line in topo_file:
            if count == 0:
                n, m = map(int, line.strip().split(' '))
            else:
                top, right, bottom, left = map(int, line.strip().split(' '))
                tile_values = tile_values + [top, right, bottom, left]
                tiles.append(Tile(top, right, bottom, left, count))
            count = count + 1
    board = create_board(n, m)
    return find_paired_values(tile_values), board


def find_paired_values(tile_values):
    """
    Function:   find_paired_values()
    This function takes in a list of integers and returns a list containing the integers
    that are not-unique (list contains the number at least twice).
    Returns a list of integers for non-unique values
    """
    unique_values = []
    for value in tile_values:
        if tile_values.count(value) == 1:
            unique_values.append(value)
    paired_values = [x for x in tile_values if x not in unique_values]
    paired_values = set(paired_values)
    return paired_values


def create_board(row_size, column_size):
    """
    Function:   create_board()
    This function takes in a board object (2d array) and sets the board to the specified dimensions
    Returns a 2d array of Null (None) Objects of the requested dimensions
    """
    board = [[None] * column_size for i in range(row_size)]
    return board


def print_board(board):
    """
    Function:   print_board()
    This function takes in a board and iterates through the array, visualizing the state of the board.
    The tiles are represented by the tile number and empty spaces are represented by 'E'
    """
    result = ""
    for row in range(len(board)):
        for col in range(len(board[row])):
            if not board[row][col] is None:
                result += (str(board[row][col].number)) + " "
            else:
                result += "E "
        result += '\n'
    print(result)


def identify_board(board):
    """
    Function:   identify_board()
    This function takes in a board, and builds a string of numbers based on the tiles placed to help identify
    unique board positions
    """
    identifier = ""
    for row in range(len(board)):
        for col in range(len(board[row])):
            if not board[row][col] is None:
                identifier += (str(board[row][col].number))
            else:
                identifier += str(0)
    return identifier


if __name__ == '__main__':
    main()
