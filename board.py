############################################################
## CSC 384, Intro to AI, University of Toronto.
## Assignment 3 Starter Code
## v1.0
##
############################################################

CHAR_BLACK = '*'
CHAR_WHITE = 'o'
CHAR_EMPTY = '.'

class Dot:

    """
    This class represents a dot drawn on the board.
    """

    def __init__(self, color, cell_row, cell_col, location):
        """
        Creating a dot. 
        Each dot is either between two cells in the same row
        or between two cells in the same column.

        :param color: either CHAR_BLACK or CHAR_WHITE.
        :param cell_row: row for the cell on the left or on top.
        :param cell_col: column for the cell on the left or on top.
        :param location: True if the dot is between two cells in the same row. 
                         False if the dot is between two cells in the same column.
        """

        self.color = color

        self.cell_row = cell_row
        self.cell_col = cell_col

        self.location = location

        if location == True: 
            # dot is to the right of the cell in [cell_row, cell_col].
            self.cell2_row = cell_row
            self.cell2_col = cell_col + 1
        else:
            # dot is below the cell in [cell_row, cell_col].
            self.cell2_row = cell_row + 1
            self.cell2_col = cell_col


class Board:
    def __init__(self, dimension):
        """
        Create a board.

        :param dimension: board dimension. 6 or 9.
        """
        self.dimension = dimension

        # initialize the list of cells
        self.cells = [[0 for i in range(dimension)] for j in range(dimension)]

        # initialize the list of dots
        self.dots = []
        
    def __str__(self):
        """
        Convert the current board to a readable string representation.
        This representation include all the dot constraints.
        """

        out_array = []

        # create an array with space characters.
        out_array.append([' ']*(self.dimension * 2 + 1))
        for row in range(self.dimension):
            tmp = []
            for col in range(self.dimension):
                tmp.append(' ')
                if self.cells[row][col] == 0:
                    tmp.append(CHAR_EMPTY)
                else:
                    tmp.append(self.cells[row][col])
            tmp.append(' ')    
            out_array.append(tmp)
            out_array.append([' ']*(self.dimension * 2 + 1))

        # add borders
        if self.dimension == 6:

            # add borders for dim = 6
            for row in range(len(out_array)):
                for col in range(len(out_array[0])):
                    if col % 4 == 0:
                        out_array[row][col] = '|'    
            for row in range(len(out_array)):
                for col in range(len(out_array[0])):
                    if row % 6 == 0:
                        out_array[row][col] = '-'

        elif self.dimension == 9:

            # add borders for dim = 6
            for row in range(len(out_array)):
                for col in range(len(out_array[0])):
                    if col % 6 == 0:
                        out_array[row][col] = '|'            
            for row in range(len(out_array)):
                for col in range(len(out_array[0])):
                    if row % 6 == 0:
                        out_array[row][col] = '-'

        # add dots
        for d in self.dots:
            if d.location == True:
                out_array[d.cell_row * 2 + 1][d.cell_col * 2 + 2] = d.color
            else:
                out_array[d.cell_row * 2 + 2][d.cell_col * 2 + 1] = d.color

        # convert array to to string
        s = ''
        for row in range(self.dimension * 2 + 1):
            for col in range(self.dimension * 2 + 1):
                s += str(out_array[row][col])
            s += '\n'

        return s
