# Advanced-Sudoku-Solver
Solves Kropki Sudoku Puzzles highly efficiently with the option to use different propagators and heuristics

# Usage
clone the repository:
```sh
git clone https://github.com/NathanZC/Advanced-Sudoku-Solver.git
cd Advanced-Sudoku-Solver
python .\csprun.py --inputfile .\test_input_file.txt --outputfile test_output_file.txt --propagator GAC
```
# Input file
* The first line is the dimensions of the board 6 (for 6x6) or 9 (for 9x9)
* Integers 1-9 are fixed inputs
* "*" represents a black dot (which means one of these cells is double the value of the other cell)
* "o" represents a white dot (which means one of these cells is one bigger than the value of the other cell)
* "." represents an empty space
# Example:
```sh
6
-------------
|. .|.o.*2 6|
|  o|  *|* *|
|. .o. .*. .|
|* *|   |   |
|.o.|. .|.o.|
-o-o-----o-o-
|.o.|. .|.o.|
|  o|   |o *|
|. .|.o.*. .|
|o  |*  |* *|
|. .*. .|. .|
-------------
```
