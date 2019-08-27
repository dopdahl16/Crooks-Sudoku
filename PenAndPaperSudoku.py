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

# Since I have the coordinates baked into each Cell oject, maybe I should subclass Matrix as a set... Faster lookups? The order that the list provides doesn't really matter...
class Matrix(list):
    def __init__(self, cells_list=[]):
        self.cells = cells_list
    def setCells(self, cells_list):
        
        # The commented code below type checks the inputted cells_list, but I've opted not to employ it. It feels more "Pythonic" 
        # to use duck typing here. (see: https://en.wikipedia.org/wiki/Duck_typing)
        '''
        if not isinstance(cells_list, list):
            raise TypeError("Matrix objects only accept lists of Cell objects for method setCells")
        for cell in cells_list:
            if not isinstance(cell, Cell):
                raise TypeError("Matrix objects only accept lists of Cell objects for method setCells")
        '''
        
        self.cells = cells_list
    def getCells(self):
        return self.cells
    def getColumnGroup(self, column_number):
        column_group = []
        for cell in self.cells:
            if cell.getCol() == column_number:
                column_group.append(cell)
        if len(column_group) != 9:
            raise BaseException("Something broke. Contact a developer ASAP!")
        return column_group
    def getRowGroup(self, row_number):
        row_group = []
        for cell in self.cells:
            if cell.getRow() == row_number:
                row_group.append(cell)
        if len(row_group) != 9:
            raise BaseException("Something broke. Contact a developer ASAP!")
        return row_group
    def getBoxGroup(self, box_number):
        box_group = []
        for cell in self.cells:
            if cell.getBox() == box_number:
                box_group.append(cell)
        if len(box_group) != 9:
            raise BaseException("Something broke. Contact a developer ASAP!")
        return box_group
    def markup(self):
        for cell in self.cells:
            if cell.getVal() == 'x':
                cell.setVal(set([1, 2, 3, 4, 5, 6, 7, 8, 9]))
    # There are too many for loops in reduceMarkup, but is there a way to reduce how many we have to use? Can we scan for numbers to be removed in a group while simultaneously remove the numbes that need to be removed from the markedup sets? I'm doubtful
    # I believe the way I have my for loops set up is optimized for more difficult puzzles. If we are dealing with puzzles that give us more numbers to start out with (easier puzzles), then I think the more optimal way would be to scan each group (row, column, box), only make a list of the numbers that need to be removed from that group, then go through again and remove the numbers that need to be removed from the markedup cells. I think the way I do it below is faster for harder puzzles because we have to iterate through fewer total things, even if we have to create an extra list
    def reduceMarkup(self):
        change_made = True
        while change_made == True:
            change_made = False
            for row_number in range(1,10,1):
                numbers_to_remove_from_marked_up_cells = set()
                marked_up_cells = []
                for cell in self.getRowGroup(row_number):
                    if isinstance(cell.getVal(), str):
                        numbers_to_remove_from_marked_up_cells.add(int(cell.getVal()))
                    elif isinstance(cell.getVal(), set):
                        if len(cell.getVal()) == 1:
                            cell.setVal(str(cell.getVal().pop()))
                        else:
                            marked_up_cells.append(cell)
                    else:
                        raise BaseException("Something broke. Contact a developer ASAP!")
                for cell in marked_up_cells:
                    if len(cell.getVal().difference(cell.getVal().difference(numbers_to_remove_from_marked_up_cells))) != 0:
                        cell.setVal(cell.getVal().difference(numbers_to_remove_from_marked_up_cells))
                        change_made = True
            for column_number in range(1,10,1):
                numbers_to_remove_from_marked_up_cells = set()
                marked_up_cells = []
                for cell in self.getColumnGroup(column_number):
                    if isinstance(cell.getVal(), str):
                        numbers_to_remove_from_marked_up_cells.add(int(cell.getVal()))
                    elif isinstance(cell.getVal(), set):
                        if len(cell.getVal()) == 1:
                            cell.setVal(str(cell.getVal().pop()))
                        else:
                            marked_up_cells.append(cell)
                    else:
                        raise BaseException("Something broke. Contact a developer ASAP!")
                for cell in marked_up_cells:
                    if len(cell.getVal().difference(cell.getVal().difference(numbers_to_remove_from_marked_up_cells))) != 0:
                        cell.setVal(cell.getVal().difference(numbers_to_remove_from_marked_up_cells))
                        change_made = True
            for box_number in range(1,10,1):
                numbers_to_remove_from_marked_up_cells = set()
                marked_up_cells = []
                for cell in self.getBoxGroup(box_number):
                    if isinstance(cell.getVal(), str):
                        numbers_to_remove_from_marked_up_cells.add(int(cell.getVal()))
                    elif isinstance(cell.getVal(), set):
                        if len(cell.getVal()) == 1:
                            cell.setVal(str(cell.getVal().pop()))
                        else:
                            marked_up_cells.append(cell)
                    else:
                        raise BaseException("Something broke. Contact a developer ASAP!")
                for cell in marked_up_cells:
                    if len(cell.getVal().difference(cell.getVal().difference(numbers_to_remove_from_marked_up_cells))) != 0:
                        cell.setVal(cell.getVal().difference(numbers_to_remove_from_marked_up_cells))
                        change_made = True
        
    # This step follows from the instructions on page 463 of Crook's paper, reading, "The method proceeds by finding a box that is missing this high-frequency number and determining whether there is one and only one cell into which this number can be entered." If reduceMarkup is called before this, then this method will accomplish what Crook describes here.
    # It is worth noting that this step is, regrettably, for loop intensive
    # //TODO// add change_made flag to this method
    def forceCells(self):
        change_made = True
        while change_made == True:
            change_made = False        
            for row_number in range(1,10,1):
                for reference_cell in self.getRowGroup(row_number):
                    if not isinstance(reference_cell.getVal(), str):
                        reference_cell_value = reference_cell.getVal()
                        number_appearance_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
                        for comparison_cell in self.getRowGroup(row_number):
                            if isinstance(comparison_cell.getVal(), str):
                                comparison_cell_value = set([int(comparison_cell.getVal())])
                            else:
                                comparison_cell_value = comparison_cell.getVal()
                            difference_set = reference_cell_value.difference(comparison_cell_value)
                            for value in difference_set:
                                number_appearance_dict[int(value)] = number_appearance_dict[int(value)] + 1
                                if number_appearance_dict[int(value)] == 8:
                                    self.resolveValue(reference_cell, value)
                                    change_made = True
            for column_number in range(1,10,1):
                for reference_cell in self.getColumnGroup(column_number):
                    if not isinstance(reference_cell.getVal(), str):
                        reference_cell_value = reference_cell.getVal()
                        number_appearance_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
                        for comparison_cell in self.getColumnGroup(column_number):
                            if isinstance(comparison_cell.getVal(), str):
                                comparison_cell_value = set([int(comparison_cell.getVal())])
                            else:
                                comparison_cell_value = comparison_cell.getVal()
                            difference_set = reference_cell_value.difference(comparison_cell_value)
                            for value in difference_set:
                                number_appearance_dict[int(value)] = number_appearance_dict[int(value)] + 1
                                if number_appearance_dict[int(value)] == 8:
                                    self.resolveValue(reference_cell, value)
                                    change_made = True
            for box_number in range(1,10,1):
                for reference_cell in self.getBoxGroup(box_number):
                    if not isinstance(reference_cell.getVal(), str):
                        reference_cell_value = reference_cell.getVal()
                        number_appearance_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
                        for comparison_cell in self.getBoxGroup(box_number):
                            if isinstance(comparison_cell.getVal(), str):
                                comparison_cell_value = set([int(comparison_cell.getVal())])
                            else:
                                comparison_cell_value = comparison_cell.getVal()
                            difference_set = reference_cell_value.difference(comparison_cell_value)
                            for value in difference_set:
                                number_appearance_dict[int(value)] = number_appearance_dict[int(value)] + 1
                                if number_appearance_dict[int(value)] == 8:
                                    self.resolveValue(reference_cell, value)
                                    change_made = True
        
    # When a value of a cell is determined, that value should be removed from the column, row, and box that the cell belongs to. For example, if I determine that a 5 belongs in the cell at [7, 2, 7], I must set the value of that cell to '5', but I must also remove 5 from the options for all the other cells in the 7th row, the 2nd column, and the 7th block.
    def resolveValue(self, cell_to_be_value_updated, cell_value):
        cell_to_be_value_updated.setVal(str(cell_value))
        for cell in self.getRowGroup(cell_to_be_value_updated.getRow()):
            if isinstance(cell.getVal(), set):
                if cell_value in cell.getVal():
                    cell.getVal().remove(cell_value)
        for cell in self.getColumnGroup(cell_to_be_value_updated.getCol()):
            if isinstance(cell.getVal(), set):
                if cell_value in cell.getVal():
                    cell.getVal().remove(cell_value)
        for cell in self.getBoxGroup(cell_to_be_value_updated.getBox()):
            if isinstance(cell.getVal(), set):
                if cell_value in cell.getVal():
                    cell.getVal().remove(cell_value)
        
    def __str__(self):
        return_str = "-----------------\n"
        for cell in self.cells:
            if not isinstance(cell.getVal(), str):
                return_str = return_str + "x" + " "
            else:
                return_str = return_str + str(cell.getVal()) + " "
            if cell.getCol() == 9:
                return_str = return_str + '\n'
        return_str = return_str + "-----------------"
        return return_str
    def __repr__(self):
        return_str = ""
        for cell in self.cells:
            return_str = return_str + cell.getVal() + " "
            if cell.getCol() == 9:
                return_str = return_str + '\n'
        return return_str    
            
            
def constructCellList(puzzle):
    ordered_cell_list = []
    cell_count = 0
    for cell_starting_val in puzzle:
        row = (cell_count // 9) + 1
        column = (cell_count % 9) + 1
        box = (((column - 1) // 3) + 1) + (((row - 1) // 3) * 3)
        ordered_cell_list.append(Cell(row, column, box, cell_starting_val))
        cell_count += 1
    return ordered_cell_list
        
def openPuzzle():
    matrix = []
    file = open("C:\\Users\\danielopdahl\\Desktop\\Crooks_Sudoku\\Puzzles\\Sudo_ku.txt", "r")
    matrix = file.read()
    print("Solving this puzzle \n-----------------")
    print(matrix)
    print("-----------------")
    matrix = matrix.split()
    return matrix


puzzle = openPuzzle()
#print(puzzle)
ordered_cell_list = constructCellList(puzzle)
#print(ordered_cell_list)
my_matrix = Matrix()
my_matrix.setCells(ordered_cell_list)
#print(str(my_matrix))

# If I were staying absolutely true to Crook's algorithm, I would call a function here called forceBoxes. This initial step is described on page 463 in his paper. The specific paragraph in which he describes this step beings, "One should always begin the solution of a Sudoku puzzle by looking for cells within boxes to enter numbers within that box that are missing." While on actual pen and paper, this may be the more efficient manner of doing things, I believe that doing this initial step in a computer algorithm can be better accomplished by first marking up the entire matrix, then doing an initial "hunt" for boxes that can be forced. This is the approach I go with in my algorithm.

my_matrix.markup()
my_matrix.reduceMarkup()
print(my_matrix)
my_matrix.forceCells()
print(my_matrix)