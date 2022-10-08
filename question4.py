import sys
import timeit
from tile import Tile
from states import State

max_child_Size = 0


def main():
    start = timeit.default_timer()
    tile_objects = []
    paired_values, board = prepare_problem_from_input_text('input.txt', tile_objects)
    # Creating a list of booleans equal in length to the number of tiles to reference to check
    # if a tile has been placed
    unplaced_tiles = [True] * len(tile_objects)

    # Attempt the algorithm at all positions of the board. While placing the first tile in a position where some edges
    # with matches are blocked may not be the best state, there is still a possibility it leads to a valid goal
    final_results = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            result = A_star(row, col, board, tile_objects, paired_values, unplaced_tiles)
            final_results.append(result)

    # Storing the final results and outputting for clarity
    final_values = []
    for result in final_results:
        final_values.append(result[0])
    if min(final_values) >= sys.maxsize:
        print("No valid solutions for problem")
    else:
        print("Lowest Solution Found", min(final_values))
        index = final_values.index(min(final_values))
        print_board(final_results[index][1].board)

    # Time it took to run program for debugging
    stop = timeit.default_timer()
    print("Time: ", stop - start)
    print("Maximum number of fringe children during runtime:", max_child_Size)


def A_star(row, col, board, tiles, paired_values, unplaced_tiles):
    """
    Function:   A_star()
    """
    # Create a root node for the starting position and add the first tile to that position.
    root = State(0, [], board, unplaced_tiles)
    root.add_tile(tiles[0], row, col, tiles, paired_values)
    # Run A* search on this starting state
    print("Trying Start Position:", [row, col])
    # print_board(root.board)
    fringe_children = []
    return a_star_helper(root, tiles, paired_values, fringe_children)


def a_star_helper(in_state, tile_objects, paired_values, fringe_children):
    # Open the root node and add its children to the fringe_children
    in_state.find_valid_children(tile_objects, paired_values)
    fringe_children = fringe_children + in_state.children
    # If the root note does not have any valid children, the problem cannot be solved at this position
    if not fringe_children:
        return [sys.maxsize, None]

    goal_states = []
    while True:
        # If no states exist in the fringe_children, the problem cannot be solved with these positions
        if not fringe_children:
            return [sys.maxsize, None]

        # Find the best child state based on the cost and the heuristic element
        chosen_state = fringe_children[0]
        minimum_fn = fringe_children[0].cost + chosen_state.heuristic
        for child in fringe_children:
            if minimum_fn > (child.cost + child.heuristic):
                chosen_state = child
                minimum_fn = child.cost + child.heuristic

        # If we have found goal states, check to see if these are better than any possible fringe state
        if goal_states:

            # Find the best goal state
            minimum_goal_cost = goal_states[0].cost
            best_goal = goal_states[0]
            for goal in goal_states:
                if minimum_goal_cost > goal.cost:
                    minimum_goal_cost = goal.cost
                    best_goal = goal

            # If the best goal state is better than any fringe state, A* has completed
            if minimum_goal_cost < minimum_fn:
                print("Board State:")
                print_board(best_goal.board)
                print("Solution cost:", best_goal.cost)
                return [best_goal.cost, best_goal]

        # Test to see if our best state is a goal state
        if not any(chosen_state.unplaced_tiles):
            goal_states.append(chosen_state)

        # Remove the best state from the fringe state. Expand the state by adding it's children to the fringe
        fringe_children.remove(chosen_state)
        chosen_state.find_valid_children(tile_objects, paired_values)

        # Test the new states to see if the board state is identical in tile placement to existing fringe states
        identity_list = []
        for fringe in fringe_children:
            identity_list.append(identify_board(fringe.board))

        # Add the children to the fringe states
        for child in chosen_state.children:
            # If the new child has a unique board configuration, add it
            if not identify_board(child.board) in identity_list:
                fringe_children.append(child)
            # The child has a configuration the same as some of our fringe states, only keep the most efficient path
            else:
                # There exists a duplicate board state, we need to keep only the most efficient version
                duplicate_state_object_list_for_comparison = []  # aka bad boi
                # While a duplicate state exists, remove them and
                while identify_board(child.board) in identity_list:
                    # Find the index of the duplicate state
                    index_of_duplicate = identity_list.index(identify_board(child.board))

                    # Remove the duplicate state from the fringe, and our identity list
                    popped_state = fringe_children.pop(index_of_duplicate)
                    identity_list.pop(index_of_duplicate)

                    # Keep a record of the duplicate states in bad boi
                    duplicate_state_object_list_for_comparison.append(popped_state)

                # Find the most efficient duplicate state
                min_state = duplicate_state_object_list_for_comparison[0]
                min_cost = min_state.cost
                for state in duplicate_state_object_list_for_comparison:
                    if state.cost < min_cost:
                        min_state = state
                        min_cost = state.cost
                # only re-add the most efficient state to our fringe children
                fringe_children.append(min_state)

        # Track the maximum fringe size for debugging
        global max_child_Size
        if max_child_Size < len(fringe_children):
            max_child_Size = len(fringe_children)
        # end of while loop


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
        if not row == len(board)-1:
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
