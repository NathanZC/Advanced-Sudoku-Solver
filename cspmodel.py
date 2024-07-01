import math
from board import *
from cspbase import *


def kropki_model(board):
    """
    Create a CSP for a Kropki Sudoku Puzzle given a board of dimension.

    If a variable has an initial value, its domain should only contain the initial value.
    Otherwise, the variable's domain should contain all possible values (1 to dimension).

    We will encode all the constraints as binary constraints.
    Each constraint is represented by a list of tuples, representing the values that
    satisfy this constraint. (This is the table representation taught in lecture.)

    Remember that a Kropki sudoku has the following constraints.
    - Row constraint: every two cells in a row must have different values.
    - Column constraint: every two cells in a column must have different values.
    - Cage constraint: every two cells in a 2x3 cage (for 6x6 puzzle) 
            or 3x3 cage (for 9x9 puzzle) must have different values.
    - Black dot constraints: one value is twice the other value.
    - White dot constraints: the two values are consecutive (differ by 1).

    Make sure that you return a 2D list of variables separately. 
    Once the CSP is solved, we will use this list of variables to populate the solved board.
    Take a look at csprun.py for the expected format of this 2D list.

    :returns: A CSP object and a list of variables.
    :rtype: CSP, List[List[Variable]]

    """
    dim = board.dimension
    csp = CSP("KropkiSudoku")
    variables = create_variables(dim)

    for row in range(dim):
        for col in range(dim):
            var = variables[row][col]
            if board.cells[row][col] != 0:  # If the cell has a pre-assigned value
                var.add_domain_values([board.cells[row][col]])
            else:
                var.add_domain_values(create_initial_domain(dim))

    for row in variables:
        for var in row:
            csp.add_var(var)
    # Creating different types of constraints
    diff_tuples = satisfying_tuples_difference_constraints(dim)
    white_dot_tuples = satisfying_tuples_white_dots(dim)
    black_dot_tuples = satisfying_tuples_black_dots(dim)

    # Adding Row and Column Constraints
    row_col_constraints = create_row_and_col_constraints(dim, diff_tuples, variables)
    for constraint in row_col_constraints:
        csp.add_constraint(constraint)

    # Adding Cage Constraints
    cage_constraints = create_cage_constraints(dim, diff_tuples, variables)
    for constraint in cage_constraints:
        csp.add_constraint(constraint)

    dot_constraints = create_dot_constraints(dim, board.dots, white_dot_tuples, black_dot_tuples, variables)
    for constraint in dot_constraints:
        csp.add_constraint(constraint)

    return csp, variables


def create_initial_domain(dim):
    """
    Return a list of values for the initial domain of any unassigned variable.
    [1, 2, ..., dimension]

    :param dim: board dimension
    :type dim: int

    :returns: A list of values for the initial domain of any unassigned variable.
    :rtype: List[int]
    """

    return list(range(1, dim + 1))


def create_variables(dim):
    """
    Return a list of variables for the board.

    We recommend that your name each variable Var(row, col).

    :param dim: Size of the board
    :type dim: int

    :returns: A list of variables, one for each cell on the board
    :rtype: List[Variables]
    """
    variables = []
    for row in range(dim):
        row_variables = []
        for col in range(dim):
            name = f"Var({row},{col})"
            var = Variable(name)
            row_variables.append(var)
        variables.append(row_variables)
    return variables


def satisfying_tuples_difference_constraints(dim):
    """
    Return a list of satifying tuples for binary difference constraints.

    :param dim: Size of the board
    :type dim: int

    :returns: A list of satifying tuples
    :rtype: List[(int,int)]
    """
    sat_tuples = []
    for i in range(1, dim + 1):
        for j in range(1, dim + 1):
            if i != j:
                sat_tuples.append((i, j))
    return sat_tuples


def satisfying_tuples_white_dots(dim):
    """
    Return a list of satifying tuples for white dot constraints.

    :param dim: Size of the board
    :type dim: int

    :returns: A list of satifying tuples
    :rtype: List[(int,int)]
    """
    sat_tuples = []
    for i in range(1, dim):
        sat_tuples.append((i, i + 1))
        sat_tuples.append((i + 1, i))
    return sat_tuples


def satisfying_tuples_black_dots(dim):
    """
    Return a list of satifying tuples for black dot constraints.

    :param dim: Size of the board
    :type dim: int

    :returns: A list of satifying tuples
    :rtype: List[(int,int)]
    """
    sat_tuples = []
    for i in range(1, dim // 2 + 1):
        if 2 * i <= dim:
            sat_tuples.append((i, 2 * i))
            sat_tuples.append((i * 2, i))
    return sat_tuples


def create_row_and_col_constraints(dim, sat_tuples, variables):
    """
    Create and return a list of binary all-different row/column constraints.

    :param dim: Size of the board
    :type dim: int

    :param sat_tuples: A list of domain value pairs (value1, value2) such that 
        the two values in each tuple are different.
    :type sat_tuples: List[(int, int)]

    :param variables: A list of all the variables in the CSP
    :type variables: List[Variable]
        
    :returns: A list of binary all-different constraints
    :rtype: List[Constraint]
    """
    constraints = []

    # Create row constraints
    for row in range(dim):
        for i in range(dim):
            for j in range(i + 1, dim):
                constraint = Constraint(f"Row{row}Var{i}Var{j}", [variables[row][i], variables[row][j]])
                constraint.add_satisfying_tuples(sat_tuples)
                constraints.append(constraint)

    # Create column constraints
    for col in range(dim):
        for i in range(dim):
            for j in range(i + 1, dim):
                constraint = Constraint(f"Col{col}Var{i}Var{j}", [variables[i][col], variables[j][col]])
                constraint.add_satisfying_tuples(sat_tuples)
                constraints.append(constraint)

    return constraints


def create_cage_constraints(dim, sat_tuples, variables):
    """
    Create and return a list of binary all-different constraints for all cages.

    :param dim: Size of the board
    :type dim: int

    :param sat_tuples: A list of domain value pairs (value1, value2) such that 
        the two values in each tuple are different.
    :type sat_tuples: List[(int, int)]

    :param variables: A list of all the variables in the CSP
    :type variables: List[Variable]
        
    :returns: A list of binary all-different constraints
    :rtype: List[Constraint]
    """
    constraints = []
    row_cage_size = 3  # Rows in each cage
    col_cage_size = 2 if dim == 6 else 3  # Columns in each cage

    for block_row in range(0, dim, row_cage_size):
        for block_col in range(0, dim, col_cage_size):
            cage_vars = [variables[block_row + i][block_col + j]
                         for i in range(row_cage_size)
                         for j in range(col_cage_size)]
            for i in range(len(cage_vars)):
                for j in range(i + 1, len(cage_vars)):
                    constraint = Constraint(f"Var{i}Var{j}", [cage_vars[i], cage_vars[j]])
                    constraint.add_satisfying_tuples(sat_tuples)
                    constraints.append(constraint)

    return constraints


def create_dot_constraints(dim, dots, white_tuples, black_tuples, variables):
    """
    Create and return a list of binary constraints, one for each dot.

    :param dim: Size of the board
    :type dim: int
    
    :param dots: A list of dots, each dot is a Dot object.
    :type dots: List[Dot]

    :param white_tuples: A list of domain value pairs (value1, value2) such that 
        the two values in each tuple satisfy the white dot constraint.
    :type white_tuples: List[(int, int)]
    
    :param black_tuples: A list of domain value pairs (value1, value2) such that 
        the two values in each tuple satisfy the black dot constraint.
    :type black_tuples: List[(int, int)]

    :param variables: A list of all the variables in the CSP
    :type variables: List[Variable]
        
    :returns: A list of binary dot constraints
    :rtype: List[Constraint]
    """
    constraints = []

    for dot in dots:
        # Determine the variables (cells) adjacent to the dot
        var1 = variables[dot.cell_row][dot.cell_col]
        var2 = variables[dot.cell2_row][dot.cell2_col]

        # Choose the correct tuples based on the dot's color
        sat_tuples = black_tuples if dot.color == CHAR_BLACK else white_tuples

        # Create a constraint between the two variables
        constraint_name = f"DotConstraint_{dot.cell_row}_{dot.cell_col}_{dot.cell2_row}_{dot.cell2_col}"
        constraint = Constraint(constraint_name, [var1, var2])
        constraint.add_satisfying_tuples(sat_tuples)
        constraints.append(constraint)

    return constraints
#
# dim = 6
# csp = CSP("KropkiSudoku")
# variables = create_variables(dim)
# for row in variables:
#     for var in row:
#         csp.add_var(var)
#
# diff_tuples = satisfying_tuples_difference_constraints(dim)
# white_dot_tuples = satisfying_tuples_white_dots(dim)
# black_dot_tuples = satisfying_tuples_black_dots(dim)
#
# # Adding Row and Column Constraints
# row_col_constraints = create_row_and_col_constraints(dim, diff_tuples, variables)
# for constraint in row_col_constraints:
#     csp.add_constraint(constraint)
#
# # Adding Cage Constraints
# cage_constraints = create_cage_constraints(dim, diff_tuples, variables)
# for constraint in cage_constraints:
#     csp.add_constraint(constraint)
