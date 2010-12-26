import argparse #module for parsing command line input
import time, datetime #module for tracking time elapsed to solution
from copy import deepcopy #function to copy array. used in Sudoku class

#logger function, only works if verbose mode is active
def log(s):
    global args
    if args.verbose:
        print s

def interactive(s): #prints when interactive enabled, waits for user to press enter
    global args
    if args.interactive:
        raw_input(s + "\nEnter to continue...")


class Sudoku(object):
    global args
    """represents the sudoku game board"""
    @classmethod
    def sudoku_from_iterator(cls, iterator): #create a sudoku board from a iterator containing iterators
        """must contain lines which contain characters"""
        return Sudoku([[int(i) for i in line.strip()] for line in iterator])
    @classmethod
    def is_solution(cls, array): #determine if the given array has no blank spaces (this may return true to invalid arrays. Sudoku.valid() is a better test)
        for row in array: 
            if 0 in row:
                return False
        return True

    def __init__(self, array): #create with array
        super(Sudoku, self).__init__()
        self.array = array #will only store integer values, squares with multiple possible values will be 0s
        self.possibilities = [] #will store the same array as array but with 0s replaced by a set containing the possible values for the square
        
    def __str__(self): #convert self
        s = ""
        if args.prettyoutput: # if -p flag
            s += "-"*13+"\n|" #add header line
            ycount = 1 #used to determine when to add box separator
            for x in self.array:
                if ycount % 4 == 0:
                    s += "|\n|"+"-"*11 #horizontal box separator
                    ycount += 1
                if ycount != 1:
                    s += "|\n|"
                xcount = 1 #used to determine when to add box separator
                for i in x:
                    if xcount % 4 == 0:
                        s += "|" #vertical box separator
                        xcount += 1
                    if i == 0:
                        s += " "
                    else:
                        s += str(i)
                    xcount += 1
                ycount += 1
            s += "|\n"+"-"*13
        else:
            for x in self.array: #without pretty mode, print same way input file is formatted
                for i in x:
                    s += str(i)
                s += "\n"
        return s
        
    def solved(self): #check to see if I am solved. equivalent to calling Sudoku.is_solved(self.array)
        return Sudoku.is_solution(self.array)
    
    def valid(self): #check to see if I'm valid.  That is: every column, row, and box only contains one of each number (1-9)
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
    #(x,y) x is vertical column, y is horizontal row
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
        
    #solver functions
    #################
    def fill(self):
        """fill empty grid with possibilities and populate the self.possibilities matrix"""
        if self.valid(): #if already solved, return -1
            return -1
        
        self.calculatePossibilities()
        
        #detect possibilities that can be replaced with a number
        row_i = 0
        space_i = 0
        replace_count = 0
        for row in self.possibilities: #go through each row in the possibilities array
            for space in row: #go through each space
                if type(space) == set: #if it's a set (meaning that is isn't already given or solved for)
                    #if it's a set and it contains 1 element, replace it in both arrays (possibilities and self.array) with the element
                    if len(space) == 1:
                        num = space.pop() #get element
                        self.array[row_i][space_i] = num
                        self.possibilities[row_i][space_i] = num #replace in arrays
                        #count this as a replacement to return
                        replace_count += 1
                space_i += 1
            row_i += 1
            space_i = 0
        #return the number of replacements we made
        return replace_count
    
    def calculatePossibilities(self):
        """calculate the possibilities without performing filling when there is only 1 option"""
        row_i = 0
        space_i = 0
        #copy the state of the main array
        self.possibilities = deepcopy(self.array)
        for row in self.array: #go through rows
            for space in row: #go through spaces
                #calculate possibilities by removing the numbers already in the row, column and box (the box array must be flattened first to avoid an unhashable type error)
                if space == 0:
                    the_set = set([1,2,3,4,5,6,7,8,9]) - set(row) - set(self.column(space_i)) - set([item for sublist in self.boxContaining(space_i, row_i) for item in sublist])
                    if the_set == set():
                        #if no solution (because a spot becomes impossible to fill, return -1 [this will tell the Sudoku.backtrack() function to fall through])
                        return -1
                    self.possibilities[row_i][space_i] = the_set
                space_i += 1
            row_i += 1
            space_i = 0
        log("Possibilities calculated by as:\n%s" % self.possibilities)
        return 0 #we're fine :D
        
    #backtracking algorithm, will return the solution.
    #runs recursivly
    def backtrack(self):
        interactive("%d began backtracking algorithm" % hash(self))
        log("backtracking on \n%s" % self)
        if self.valid(): #check to see if we're solved
            return self #return myself down the function call tree
        
        #pick the easiest location to solve in the possibilites list
        row_i = 0
        column_i = 0
        minimum = None
        min_row = None
        min_col = None
        interactive("possibilities: %s" % self.possibilities)
        for row in self.possibilities:
            for column in row:
                if type(column) == set:
                    if (minimum == None or len(column) < minimum):
                        min_row = row_i
                        min_col = column_i
                        minimum = len(column)
                column_i += 1
            row_i += 1
            column_i = 0
        interactive("%d picked %s at position (%d,%d) as easiest to solve" % (hash(self), self.possibilities[min_row][min_col],min_row,min_col))
        for x in self.possibilities[min_row][min_col]: #go through possibilities for the chosen space to solve
            interactive("%d tried %d to solve" % (hash(self), x))
            reccur_on = Sudoku(deepcopy(self.array)) #create a new board representation with a copy of my array
            reccur_on.array[min_row][min_col] = x #try a value in the possibilites set for the chosen position
            interactive("\n%s\n created \n%s\nposition (%d,%d) changed\n to begin backtrack recursivley" % (self, reccur_on,min_row,min_col))
            solution = None 
            if reccur_on.calculatePossibilities() != -1: #if there are possibilities for every space,
                solution = reccur_on.backtrack() #begin backtrack algorithm
            if solution != None: #if the solution is returned, return it down and set it to my array
                self.array = solution.array
                return solution
            interactive("solution fell through at %d" % hash(self))
        
        return None #there's no solution at this stage
    
def main():
    global sudoku
    global args
    #setup argument parser
    parser = argparse.ArgumentParser(description="Solves sudoku Puzzles.")
    parser.add_argument('file_handle', type=open, help="name of file to load for sudoku puzzle", metavar="filename")
    parser.add_argument('-v', '--verbose', help='produce detailed output', action='store_true')
    parser.add_argument('-p', '--prettyoutput', help="print a nicely formatted output", action='store_true')
    parser.add_argument('--checkvalidity', help='check validity after solving. shouldn\'t be needed', action='store_true')
    parser.add_argument('-i', '--interactive', help='go through the algorithm with pauses step by step', action='store_true')
    #gather arguments in namespace
    args = parser.parse_args()
    log(args)
    #GO!
    #create the 2D list to represent 9*9 sudoku and return a Sudoku object
    sudoku = Sudoku.sudoku_from_iterator(args.file_handle)
    print "Input:\n%s" % str(sudoku)
    #start tracking time to solve
    start_time = time.clock()
    print "Solving..."
    #simplify with basic sudoku game rules (only will simplify when there are squares that MUST contain a given value based on the rules)
    solve_number = None
    #loop through here till we're solved or there is no more possible rule based simplifications
    while solve_number != 0 and not sudoku.solved():
        solve_number = sudoku.fill()
        log("Reduction round using possible value rules produced:\n%s\nSolved %i spaces" % (sudoku, solve_number))
        interactive("Basic simplification round produced:\n%s\nSolved %d locations" % (sudoku, solve_number))
    log("Finished using basic rules. Reduced to:\n%s" % sudoku)
    if not sudoku.solved(): #if we're still not solved go to backtracking
        interactive("Sudoku not yet solved.  Beginning backtracking method.")
        log("solving with backtracking")
        solved = sudoku.backtrack() #begin backtracking, storing solution in solved
        if not solved: #if there was a solution  
            print "Error: Unsolvable"
            solved = False
    
    if sudoku.solved():
        print "Solved in %s." % datetime.timedelta(seconds=time.clock()-start_time) 
        print sudoku 
   
    if args.checkvalidity:
        print "Checking Validity..."
        if sudoku.valid():
            print "Solution Valid!"
        else:
            print "Please retry. There has been an error or there is no solution."
    
if __name__ == '__main__':
    main()