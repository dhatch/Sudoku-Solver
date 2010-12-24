import argparse
from copy import deepcopy

#logger function, only works if verbose mode is active
def log(s):
    global args
    if args.verbose:
        print s
 

class Sudoku(object):
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
        for x in self.array:
            for i in x:
                s += str(i)
            s += "\n"
        return s
    
    #grid functions
    #(0,0) is top left
    #(8,8) is bottom right
    #(x,y) x is column, y is row
    def row(self, y):
        log("row returned %s" % self.array[y])
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
    #gather arguments in namespace
    args = parser.parse_args()
    log(args)
    #GO!
    #create the 2D list to represent 9*9 sudoku
    sudoku = Sudoku.sudoku_from_iterator(args.file_handle)
    log("Read sudoku file as\n%s" % str(sudoku))
    
    #fill empty spaces with possibilities
    sudoku.fill()
    
if __name__ == '__main__':
    main()