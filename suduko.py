import argparse
def log(s):
    global args
    if args.verbose:
        print s
 
class Suduko(object):
    """docstring for Suduko"""
    @classmethod
    def suduko_from_iterator(cls, iterator):
        """must contain lines which contain characters"""
        return Suduko([[i for i in line.strip()] for line in iterator])
    def __init__(self, array):
        super(Suduko, self).__init__()
        self.array = array
        
    def __str__(self):
        s = ""
        for x in self.array:
            for i in x:
                s += i
            s += "\n"
        return s
    
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

#how many zeros are in this list?
def num_zero(array):
    count = 0
    for x in array:
        count += 1
    return count
    
def main():
    global suduko
    global args
    #setup argument parser
    parser = argparse.ArgumentParser(description="Solves Suduko Puzzles.")
    parser.add_argument('file_handle', type=open, help="name of file to load for suduko puzzle", metavar="filename")
    parser.add_argument('-v', '--verbose', help='produce detailed output', action='store_true')
    #gather arguments in namespace
    args = parser.parse_args()
    log(args)
    #GO!
    #create the 2D list to represent 9*9 suduko
    suduko = Suduko.suduko_from_iterator(args.file_handle)
    log("Read suduko file as\n%s" % str(suduko))
    
    #find path of least resistance
    #eg, column, box, or row with least empty spaces
    
if __name__ == '__main__':
    main()