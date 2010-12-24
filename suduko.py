import argparse
from copy import deepcopy

#logger function, only works if verbose mode is active
def log(s):
    global args
    if args.verbose:
        print s
 

class Sudoku(object):
    global args
    """represents the sudoku game board"""
    @classmethod
    def sudoku_from_iterator(cls, iterator):
        """must contain lines which contain characters"""
        return Sudoku([[int(i) for i in line.strip()] for line in iterator])
    def __init__(self, array):
        super(Sudoku, self).__init__()
        self.array = array
        
    def __str__(self):
        s = ""
        if args.prettyoutput:
            s += "-"*13+"\n|"
            ycount = 1
            for x in self.array:
                if ycount % 4 == 0:
                    s += "|\n|"+"-"*11
                    ycount += 1
                if ycount != 1:
                    s += "|\n|"
                xcount = 1
                for i in x:
                    if xcount % 4 == 0:
                        s += "|"
                        xcount += 1
                    s += str(i)
                    xcount += 1
                ycount += 1
            s += "|\n"+"-"*13
        else:
            for x in self.array:
                for i in x:
                    s += str(i)
                s += "\n"
        return s
        
    def solved(self):
        for row in self.array: 
            if 0 in row:
                return False
        return True
    
    def valid(self):
        for x in xrange(9):
            if sum(self.column(x)) != 45:
                return False
            if sum(self.row(x)) != 45:
                return False
            if sum([item for sublist in self.box(x) for item in sublist]) != 45:
                return False
        return True

    #grid functions
    #(0,0) is top left
    #(8,8) is bottom right
    #(x,y) x is column, y is row
    def row(self, y):
        return self.array[y]
    def column(self, x):
        return [i[x] for i in self.array]
    
    #numbered 0,1,2,... from top left to bottom right
    def box(self, n):
        return [[x for x in i[(n % 3)*3:(n % 3)*3 + 3]] for i in self.array[(n//3)*3:(n//3)*3 + 3]]
        
    def boxContaining(self, x, y): 
        """get the box which contains the element at the position defined by (x,y)"""
        return self.box((x//3) + (y//3)*3)
        
    #def solvers
    def fill(self):
        """fill empty grid with possibilities and populate the self.possibilities matrix"""
        #fill empty spaces, removing non possible numbers
        if self.solved():
            return -1
        
        row_i = 0
        space_i = 0
        #copy the state of the array
        self.possibilities = deepcopy(self.array)
        for row in self.array:
            for space in row:
                #calculate possibilities by removing the numbers already in the row, column and box
                if space == 0:
                    the_set = set([1,2,3,4,5,6,7,8,9]) - set(row) - set(self.column(space_i)) - set([item for sublist in self.boxContaining(space_i, row_i) for item in sublist])
                    self.possibilities[row_i][space_i] = the_set
                space_i += 1
            row_i += 1
            space_i = 0
        log("Possibilities calculated by as:\n%s" % self.possibilities)
        #detect possibilities that can be replaced with a number
        row_i = 0
        space_i = 0
        replace_count = 0
        for row in self.possibilities: 
            for space in row:
                if type(space) == set:
                    #if it's a set and it contains 1 element, replace it in both arrays with the element
                    if len(space) == 1:
                        num = space.pop()
                        self.array[row_i][space_i] = num
                        self.possibilities[row_i][space_i] = num
                        #count this as a replacement to return
                        replace_count += 1
                space_i += 1
            row_i += 1
            space_i = 0
        #return the number of replacements we made
        return replace_count
        
#how many zeros are in this list?
def num_zero(array):
    count = 0
    for x in array:
        count += 1
    return count
    
def main():
    global sudoku
    global args
    #setup argument parser
    parser = argparse.ArgumentParser(description="Solves sudoku Puzzles.")
    parser.add_argument('file_handle', type=open, help="name of file to load for sudoku puzzle", metavar="filename")
    parser.add_argument('-v', '--verbose', help='produce detailed output', action='store_true')
    parser.add_argument('-p', '--prettyoutput', help="print a nicely formatted output", action='store_true')
    #gather arguments in namespace
    args = parser.parse_args()
    log(args)
    #GO!
    #create the 2D list to represent 9*9 sudoku
    sudoku = Sudoku.sudoku_from_iterator(args.file_handle)
    log("File Input:\n%s" % str(sudoku))
    print "Solving..."
    #simplify with basic sudoku rules
    solve_number = None
    while solve_number != 0 and not sudoku.solved():
        solve_number = sudoku.fill()
        log("Reduction round using possible value rules produced:\n%s\nSolved %i spaces" % (sudoku, solve_number))
    log("Finished using basic rules. Reduced to:\n%s" % sudoku)
    print "Solved."
    print sudoku
    print "Checking Validity..."
    if sudoku.valid():
        print "Solution Valid!"
    else:
        print "Please retry. There has been an error."
    
if __name__ == '__main__':
    main()