############################################################
## CSC 384, Intro to AI, University of Toronto.
## Assignment 3 Starter Code
## v1.1
## Changes:
##  - changed the command line arguments so that not providing the heuristic 
##    flag means not using the MRV heuristic, and providing the flag means 
##    using the heuristic.
############################################################

import argparse

from board import *
from cspmodel import *
from propagators import *

def read_from_file(filename):
    """
    Create and return a board using the input file
    """

    inputfile = open(filename, 'r')
    lines = inputfile.readlines()
    inputfile.close()
    
    # get the dimension
    dimension = int(lines[0].strip())

    board = Board(dimension)

    # populate the initial values
    for row in range(dimension):
        line = lines[row * 2 + 2].strip()

        for col in range(dimension):
            col_actual = col * 2 + 1
            if line[col_actual] != CHAR_EMPTY:
                board.cells[row][col] = int(line[col_actual])

    # add the dot constraints between two cells in the same row (location is True)
    for row in range(dimension):
        line = lines[row * 2 + 2].strip()

        for col in range(dimension - 1):
            col_actual = col * 2 + 2
            if line[col_actual] == CHAR_BLACK or line[col_actual] == CHAR_WHITE:
                dot = Dot(line[col_actual], row, col, True)
                board.dots.append(dot)

    # adding the dot constraints between two cells in the same column (location is False)
    for row in range(dimension - 1):
        line = lines[row * 2 + 3].strip()

        for col in range(dimension):
            col_actual = col * 2 + 1
            if line[col_actual] == CHAR_BLACK or line[col_actual] == CHAR_WHITE:
                dot = Dot(line[col_actual], row, col, False)
                board.dots.append(dot)

    return board


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzle."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    parser.add_argument(
        "--propagator",
        type=str,
        required=False,
        default='BT',
        choices=['BT', 'FC', 'GAC'],
        help="Propagator to be used. Options are BT, FC, and GAC."
    )
    parser.add_argument(
        "--heuristic",
        required=False,
        action="store_true",
        help="Select the next variable using the MRV heuristic."
    )

    args = parser.parse_args()

    # create th board from the input file
    puzz_file = args.inputfile
    board = read_from_file(puzz_file)

    print("Solving the Kropki Sudoku Puzzle below.")
    if args.propagator == 'FC':
        print("with Backtracking Search + Forward Checking")
        prop = prop_FC
    elif args.propagator == 'GAC':
        print("with Backtracking Search + The AC-3 Algorithm")
        prop = prop_AC3
    else:
        print("with Backtracking Search only")
        prop = prop_BT

    # print the board
    print("The initial board is below.\n{}".format(board))

    csp, var_list = kropki_model(board)
    
    solver = BT(csp)

    if args.heuristic:
        print("Using the MRV heuristic")
        solver.bt_search(prop, ord_mrv)
    else:
        print("NOT using the MRV heuristic")
        solver.bt_search(prop)

    # fill the board with the variables' assigned values.
    for row in range(board.dimension):
        for col in range(board.dimension):
            board.cells[row][col] = var_list[row][col].get_assigned_value()

    # print the solution
    print("The solved board is below.\n{}".format(board))

    # saving the board to the output file
    print("Saving the solved board to outputfile {}".format(args.outputfile))
    outputfile = open(args.outputfile, "w")
    print(board.dimension, file=outputfile)
    print(board, file=outputfile)
    outputfile.close()


