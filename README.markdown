A Suduko Solver written in python for the Forrst Code Challenge.

[Original Code Challenge](http://forr.st/~047)

### Requires: ###
- Python 2.7

### usage: ###
    sudoku.py [-h] [-v] [-p] [--checkvalidity] [-i] filename

### positional arguments: ###

    filename            name of file to load for sudoku puzzle

### optional arguments: ###
    -h, --help          show this help message and exit  
    -v, --verbose       produce detailed output
    -p, --prettyoutput  print a nicely formatted output
    --checkvalidity     check validity after solving. shouldn't be needed
    -i, --interactive   go through the algorithm with pauses step by step

----------------------------------------------------------------------------------
**Note**: you probably want to use the -p option to produce more readable output.

#### Output Without -p: ####
    815493762
    362875149
    479261853
    694357218
    123984675
    758126934
    581732496
    246519387
    937648521

#### Output With -p: ####
    -------------
    |815|493|762|
    |362|875|149|
    |479|261|853|
    |-----------|
    |694|357|218|
    |123|984|675|
    |758|126|934|
    |-----------|
    |581|732|496|
    |246|519|387|
    |937|648|521|
    -------------
    
### Algorithm Details ###

1. Use basic sudoku rules to produce possible values for board
2. If there are spaces that must contain a value based on the possible values, fill them.
3. Repeat from step 1 as long as new values are being filled.
4. If board is still unsolved, begin [backtracking](http://www.cse.ohio-state.edu/~gurari/course/cis680/cis680Ch19.html) algorithm.
5. Start by choosing easiest square to solve (least possible solutions).
6. Choose a solution and create a new board instance, build it's possible values list (*but without filling*) and continue backtracking on that board.
7. Continue steps 4-6 recursively
8. Return solution or no possible solution.
