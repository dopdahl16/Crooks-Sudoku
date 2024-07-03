# Copyright (C) 2024 Daniel Opdahl (daniel@danielopdahl.com) Some Rights Reserved. 
# Permission to copy and modify is granted under the GNU General Public License v3.0 license
# Last revised 7/3/2024

# TODO: Tell someone you love that you love them today :) 

import copy

class Cell:
    def __init__(self, cell_row, cell_col, cell_box, cell_val):
        self.row = cell_row
        self.col = cell_col
        self.box = cell_box
        self.val = cell_val
    def setRow(self, new_row):
        self.row = new_row
    def getRow(self):
        return self.row
    def setCol(self, new_col):
        self.col = new_col
    def getCol(self):
        return self.col
    def setBox(self, new_box):
        self.box = new_box
    def getBox(self):
        return self.box
    def setVal(self, new_val):
        self.val = new_val
    def getVal(self):
        return copy.copy(self.val)
    def __str__(self):
        cors_val = [self.row, self.col, self.box, self.val]
        return_str = str(cors_val)
        return return_str
    def __repr__(self):
        cors_val = [self.row, self.col, self.box, self.val]
        return_str = str(cors_val)
        return return_str

class Matrix(list):
    # It would be possible to generalize the methods reduceMarkup, forceCells, findPreemptiveSets into one method. However, I think the readability and clarity of having those distinct functions call helper functions (reduceGroupMarkup forceCellsInGroup findPreemptiveSetsInGroup) is well worth the extra few kilobytes. This note is only here to satisfy the pedants and acknowledge that yes, I do notice the redundancy. It is intentional.

    def __init__(self, cells_list=[]):
        self.cells = cells_list

    def __str__(self):
        return_str = "-------------------\n"
        for cell in self.getCells():
            if not isinstance(cell.getVal(), str):
                return_str = return_str + "x" + " "
            else:
                return_str = return_str + str(cell.getVal()) + " "
            if cell.getCol() == 9:
                return_str = return_str + '\n'
        return_str = return_str + "-------------------"
        return return_str

    def __repr__(self):
        return_str = ""
        for cell in self.getCells():
            return_str = return_str + cell.getVal() + " "
            if cell.getCol() == 9:
                return_str = return_str + '\n'
        return return_str

    def setCells(self, cells_list):
        self.cells = cells_list
        
    def getCells(self):
        return self.cells
    
    def getCellsSnapshot(self):
        cells_snapshot = []
        for cell in self.cells:
            cells_snapshot.append(cell.getVal())
        return cells_snapshot

    def getColumnGroup(self, column_number):
        column_group = []
        for cell in self.getCells():
            if cell.getCol() == column_number:
                column_group.append(cell)
        if len(column_group) != 9:
            raise BaseException("Something broke. Contact a developer ASAP!")
        return column_group
    
    def getRowGroup(self, row_number):
        row_group = []
        for cell in self.getCells():
            if cell.getRow() == row_number:
                row_group.append(cell)
        if len(row_group) != 9:
            raise BaseException("Something broke. Contact a developer ASAP!")
        return row_group
    
    def getBoxGroup(self, box_number):
        box_group = []
        for cell in self.getCells():
            if cell.getBox() == box_number:
                box_group.append(cell)
        if len(box_group) != 9:
            raise BaseException("Something broke. Contact a developer ASAP!")
        return box_group

    def markup(self):
        for cell in self.getCells():
            if cell.getVal() == 'x':
                cell.setVal(set([1, 2, 3, 4, 5, 6, 7, 8, 9]))
                
    def reduceMarkup(self):
        change_made = True
        getter_functions = [self.getRowGroup, self.getColumnGroup, self.getBoxGroup]
        while change_made == True:
            change_made = False
            for getter_function in getter_functions:
                prior_state = list(self.getCellsSnapshot())
                for subset_number in range(1,10,1):
                    self.reduceGroupMarkup(getter_function, subset_number)
                    if prior_state != list(self.getCellsSnapshot()):
                        change_made = True
        
    # I force cells a little differently than Crook. I recognized that a forced cell would always be a cell who has a unique number in its markup as compared to the markup of other cells in its three groups. As such, I first reduce markups, then use markups to identify forced cells. Crook first forces cells and then marks up cells, although he alludes to using a computer to mark up cells. I can only assume that were he to convert his algorithm to code, he would reach the same ordering of steps as I have.
    def forceCells(self):
        change_made = True
        getter_functions = [self.getRowGroup, self.getColumnGroup, self.getBoxGroup]
        while change_made == True:
            change_made = False
            for getter_function in getter_functions:
                prior_state = list(self.getCellsSnapshot())
                for subset_number in range(1,10,1):
                    self.forceCellsInGroup(getter_function, subset_number)
                    if prior_state != list(self.getCellsSnapshot()):
                        change_made = True
                        self.reduceMarkup()

    def findPreemptiveSets(self):
        change_made = True
        getter_functions = [self.getRowGroup, self.getColumnGroup, self.getBoxGroup]
        while change_made == True:
            change_made = False
            for getter_function in getter_functions:
                prior_state = list(self.getCellsSnapshot())
                for subset_number in range(1,10,1):
                    self.findPreemptiveSetsInGroup(getter_function, subset_number)
                    if prior_state != list(self.getCellsSnapshot()):
                        change_made = True

    def reduceGroupMarkup(self, getFunction, subset_number):
        numbers_to_remove_from_marked_up_cells = set()
        marked_up_cells = []
        for cell in getFunction(subset_number):
            if isinstance(cell.getVal(), str):
                numbers_to_remove_from_marked_up_cells.add(int(cell.getVal()))
            elif isinstance(cell.getVal(), set):
                if len(cell.getVal()) == 1:
                    cell.setVal(str(cell.getVal().pop()))
                    numbers_to_remove_from_marked_up_cells.add(int(cell.getVal()))
                else:
                    marked_up_cells.append(cell)
            else:
                raise BaseException("Invalid type in cell value")
        for cell in marked_up_cells:
            if len(cell.getVal().difference(cell.getVal().difference(numbers_to_remove_from_marked_up_cells))) != 0:
                cell.setVal(cell.getVal().difference(numbers_to_remove_from_marked_up_cells))

    def forceCellsInGroup(self, getFunction, subset_number):
        number_appearance_dict = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
        for cell in getFunction(subset_number):
            if isinstance(cell.getVal(), set):
                for potential_value in cell.getVal():
                    number_appearance_dict[int(potential_value)] = number_appearance_dict[int(potential_value)] + 1
        for number in number_appearance_dict:
            if number_appearance_dict[number] == 1:
                for cell in getFunction(subset_number):
                    if isinstance(cell.getVal(), set):
                        if number in cell.getVal():
                            cell.setVal(str(number))

    def findPreemptiveSetsInGroup(self, getFunction, subset_number):
        self.reduceGroupMarkup(getFunction, subset_number)
        for cell in getFunction(subset_number):
            if isinstance(cell.getVal(), set):
                preemptive_set_cells = []
                for other_cell in getFunction(subset_number):
                    if isinstance(other_cell.getVal(), set):
                        if other_cell.getVal().issubset(cell.getVal()):
                            preemptive_set_cells.append(other_cell)
                if len(cell.getVal()) == len(preemptive_set_cells):
                    preemptive_set_numbers = set()
                    for preemptive_cell in preemptive_set_cells:
                        preemptive_set_numbers = preemptive_cell.getVal().union(preemptive_set_numbers)
                    for number in preemptive_set_numbers:
                        self.stripPreemptiveSetFromGroup(getFunction, subset_number, preemptive_set_cells, number)

    def resolveValue(self, cell_to_be_updated, cell_value):
        cell_to_be_updated.setVal(str(cell_value))
        group_getter_functions = [self.getRowGroup, self.getColumnGroup, self.getBoxGroup]
        cell_getter_functions = [cell_to_be_updated.getRow, cell_to_be_updated.getCol, cell_to_be_updated.getBox]
        for getter_function_index in range(len(group_getter_functions)):
            self.stripValueFromGroup(group_getter_functions[getter_function_index], cell_getter_functions[getter_function_index](), cell_value)

    def stripValueFromGroup(self, getFunction, subset_number, cell_value_to_remove):
        for cell in getFunction(subset_number):    
            if isinstance(cell.getVal(), set):
                if cell_value_to_remove in cell.getVal():
                    updated_cell_markup = copy.copy(cell.getVal())
                    updated_cell_markup.remove(cell_value_to_remove)
                    cell.setVal(updated_cell_markup)
        self.reduceGroupMarkup(getFunction, subset_number)

    def stripPreemptiveSetFromGroup(self, getFunction, subset_number, preemptive_set_cells, cell_value_to_remove):
        for cell in getFunction(subset_number):    
            if isinstance(cell.getVal(), set):
                if cell not in preemptive_set_cells:
                    if cell_value_to_remove in cell.getVal():
                        updated_cell_markup = copy.copy(cell.getVal())
                        updated_cell_markup.remove(cell_value_to_remove)
                        cell.setVal(updated_cell_markup)
 
    def checkSolved(self):
        if self.checkFilled() == False:
            return
        if self.checkValidSolution() == False:
            return
        print("SOLVED")
        print(self)
        quit()

    def checkFilled(self):
        for cell in self.getCells():
            if isinstance(cell.getVal(), set):
                return False
        return True

    def checkValidSolution(self):
        getter_functions = [self.getRowGroup, self.getColumnGroup, self.getBoxGroup]
        for getter_function in getter_functions:
            for subset_number in range(1,10,1):
                subset = []
                for cell in getter_function(subset_number):
                    if cell.getVal() not in ['1','2','3','4','5','6','7','8','9']:
                        return False
                    subset.append(cell.getVal())
                if len(subset) != len(set(subset)):
                    return False
        return True
    
    def checkViolation(self):
        getter_functions = [self.getRowGroup, self.getColumnGroup, self.getBoxGroup]
        for getter_function in getter_functions:
            for subset_number in range(1,10,1):
                subset = []
                for cell in getter_function(subset_number):
                    if cell.getVal() in ['1','2','3','4','5','6','7','8','9']:
                        subset.append(cell.getVal())
                if len(subset) != len(set(subset)):
                    return True
        return False

    def checkValidPuzzle(self):
        getter_functions = [self.getRowGroup, self.getColumnGroup, self.getBoxGroup]
        for getter_function in getter_functions:
            for subset_number in range(1,10,1):
                subset = []
                for cell in getter_function(subset_number):
                    if cell.getVal() not in ['1','2','3','4','5','6','7','8','9','x']:
                        print("Invalid Puzzle: illegal character included")
                        quit()
                    subset.append(cell.getVal())
                if len(list(filter(('x').__ne__, subset))) != len(set(list(filter(('x').__ne__, subset)))):
                    print("Invalid Puzzle: duplicate number in a row, column, or box")
                    quit()
        return

    def guess(self):
        smallest_markup_cell = Cell(0, 0, 0, {1,2,3,4,5,6,7,8,9,10})
        for cell in self.getCells():
            if isinstance(cell.getVal(), set) and len(cell.getVal()) < len(smallest_markup_cell.getVal()):
                smallest_markup_cell = cell
        index_of_smallest_markup_cell = self.getCells().index(smallest_markup_cell)
        for guess in smallest_markup_cell.getVal():
            possible_smallest_markup_cell = copy.deepcopy(smallest_markup_cell)
            possible_smallest_markup_cell.setVal(str(guess))
            possible_cell_list = copy.deepcopy(self.getCells())
            possible_cell_list[index_of_smallest_markup_cell] = possible_smallest_markup_cell
            possible_matrix = copy.deepcopy(self)
            possible_matrix.setCells(possible_cell_list)
            while True:
                puzzle_state = list(possible_matrix.getCellsSnapshot())
                possible_matrix.reduceMarkup()
                if possible_matrix.checkViolation() == True:
                    break
                possible_matrix.checkSolved()
                possible_matrix.forceCells()
                if possible_matrix.checkViolation() == True:
                    break
                possible_matrix.reduceMarkup()
                if possible_matrix.checkViolation() == True:
                    break
                possible_matrix.checkSolved()
                possible_matrix.findPreemptiveSets()
                if possible_matrix.checkViolation() == True:
                    break
                if puzzle_state == list(possible_matrix.getCellsSnapshot()):
                    possible_matrix.guess()
                    break
        return


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
    matrix = " "
    ask_for_input = True
    while ask_for_input:
        # user_input = input("Please enter the path to a Sudoku puzzle file: ")
        user_input = "Puzzles/Sudoku1.txt"
        try:
            file = open(user_input, "r")
            ask_for_input = False
        except IOError:
            print("No such file name. Please input a valid path and filename.")
    file_in = file.read()
    char_count = 0
    for char in file_in:
        if char == "0":
            char = "x"
        matrix += char
        if char_count == 9:
            matrix += "\n"
        else:
            matrix += " "
    print("Solving this puzzle \n-------------------")
    print(matrix)
    print("-------------------")
    matrix = matrix.split()
    return matrix


puzzle = openPuzzle()
ordered_cell_list = constructCellList(puzzle)
my_matrix = Matrix()
my_matrix.setCells(ordered_cell_list)
my_matrix.checkValidPuzzle()
my_matrix.markup()
while True:
    puzzle_state = list(my_matrix.getCellsSnapshot())
    my_matrix.reduceMarkup()
    my_matrix.checkSolved()
    my_matrix.forceCells()
    my_matrix.reduceMarkup()
    my_matrix.checkSolved()
    my_matrix.findPreemptiveSets()
    if puzzle_state == list(my_matrix.getCellsSnapshot()):
        my_matrix.guess()