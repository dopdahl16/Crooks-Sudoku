# Copyright (C) 2019 Daniel Opdahl (dopdahl16@gmail.com) Some Rights Reserved. 
# Permission to copy and modify is granted under the GNU General Public License v3.0 license
# Last revised 8/27/2019

class Cell:
    def __init__(self, cell_row, cell_col, cell_box, cell_val):
        self.row = cell_row
        self.col = cell_col
        self.box = cell_box
        self.val = cell_val
    def getRow(self):
        return self.row
    def getCol(self):
        return self.col
    def getBox(self):
        return self.box
    def getVal(self):
        return self.val
    def setRow(self, new_row):
        self.row = new_row
    def setCol(self, new_col):
        self.col = new_col
    def setBox(self, new_box):
        self.box = new_box
    def setVal(self, new_val):
        self.val = new_val
    def __str__(self):
        cors_val = [self.row, self.col, self.box, self.val]
        return_str = str(cors_val)
        return return_str
    def __repr__(self):
        cors_val = [self.row, self.col, self.box, self.val]
        return_str = str(cors_val)
        return return_str

class Matrix(list):
    def __init__(self, cells_list=[]):
        self.cells = cells_list
    def setCells(self, cells_list):
        
        # The commented code below type checks the inputted cells_list, but I've opted not to employ it. It feels more "Pythonian" 
        # to use duck typing here. (see: https://en.wikipedia.org/wiki/Duck_typing)
        '''
        if not isinstance(cells_list, list):
            raise TypeError("Matrix objects only accept lists of Cell objects for method setCells")
        for cell in cells_list:
            if not isinstance(cell, Cell):
                raise TypeError("Matrix objects only accept lists of Cell objects for method setCells")
        '''
        
        self.cells = cells_list
    def __repr__(self):
        return_str = "------------------\n"
        for element in self.cells:
            return_str = return_str + element.getVal() + " "
            if element.getCol() == 9:
                return_str = return_str + '\n'
        return_str = return_str + "------------------"
        return return_str
            
            
def constructCellList(matrix):
    ordered_cell_list = []
    cell_count = 0
    for cell_starting_val in matrix:
        row = (cell_count // 9) + 1
        column = (cell_count % 9) + 1
        box = (((column - 1) // 3) + 1) + (((row - 1) // 3) * 3)
        ordered_cell_list.append(Cell(row, column, box, cell_starting_val))
        cell_count += 1
    return ordered_cell_list
        
def openPuzzle():
    matrix = []
    file = open("C:\\Users\\danielopdahl\\Desktop\\Crooks_Sudoku\\Puzzles\\Sudoku1.txt", "r")
    matrix = file.read()
    print("Solving this puzzle \n------------------")
    print(matrix)
    print()
    matrix = matrix.split()
    return matrix



puzzle = openPuzzle()
#print(puzzle)
ordered_cell_list = constructCellList(puzzle)
#print(ordered_cell_list)
my_matrix = Matrix()
my_matrix.setCells(ordered_cell_list)
print(my_matrix)