# Copyright (C) 2019 Daniel Opdahl (dopdahl16@gmail.com) Some Rights Reserved. 
# Permission to copy and modify is granted under the GNU General Public License v3.0 license
# Last revised 8/26/2019

import copy
import sys
import time


def CreateGroups(matrix):
    rows = matrix
    columns = []
    boxes = []
    for i in range(0,9):
        column = []
        for row in matrix:
            column.append(row[i])
        columns.append(column)
    for n in range(0,9,3):
        for m in range(0,9,3):
            box = []
            for i in range(0,3):
                for j in range(0,3):
                    a = matrix[n+i][m+j]
                    box.append(a)
            boxes.append(box)
    return [rows, columns, boxes]
    
        

def ending(user_in, matrix):
    solved = user_in[:len(user_in)-4] + "_solved_by_brute_force.txt"
    solved_file = open(solved, 'w')
    for row in matrix:
        for item in row:
            solved_file.write(str(item.pop()) + " ")
        solved_file.write("\n")
    solved_file.close()
    solved_file = open(solved, 'r')
    print("Solution \n------------------")
    print(solved_file.read())
    print("Valid Solution!")
    sys.exit()



def preemptiveReduce(groups):
    changed = True
    changed_at_all = False
    while changed == True:
        changed = False
        for group in groups:
            for rcb in group:
                for cell in rcb:
                    count = 1
                    if len(cell) > 1 and len(cell) < 9:
                        for cell2 in rcb:
                            if cell == cell2 and not cell is cell2:
                                count += 1
                                if len(cell) == count:
                                    preemptive_set = copy.deepcopy(cell)
                                    for i in rcb:
                                        if not i == cell:
                                            OG = copy.deepcopy(i)
                                            i.difference_update(cell)
                                            if OG != i:
                                                changed = True
                                                changed_at_all = True
    return changed_at_all



def groupReduce(groups):
    changed = True
    changed_at_all = False
    while changed == True:
        changed = False
        for group in groups:
            for rcb in group:
                for cell in rcb:
                    if len(cell) == 1:
                        for cell2 in rcb:
                            if cell != cell2:
                                OG = copy.deepcopy(cell2)
                                if len(OG) == 0 or len(cell) == 0 or len(cell2)== 0:
                                    print("WTF")                                
                                cell2.difference_update(cell)
                                if OG != cell2:
                                    changed = True
                                    changed_at_all = True
                                if len(OG) == 0 or len(cell) == 0 or len(cell2)== 0:
                                    print("WTF")
    return changed_at_all



def isFinished(matrix):
    for row in matrix:
        for cell in row:
            if len(cell) != 1:
                return False
    return True




def brute(groups, user_in):
    print(groups)
    
    flag = True
    while flag:
        flag1 = groupReduce(groups)
        flag2 = preemptiveReduce(groups)
        if flag1 == False or flag2 == False:
            flag = False
        
    print(groups)
    for group in groups:
        for rcb in group:
            for cell in rcb:
                if len(cell) != 1:
                    old_cell = copy.deepcopy(cell)
                    for j in range(len(cell)):
                        num = old_cell.pop() #CANT just have it pop a number off. Have to have it choose a number intelligently. See number '4' in group 1 with sudoku2.txt
                        cell.clear()
                        cell.add(num)
                        print(groups)
                        print()
                        brute(groups, user_in)
                        
                        
                        
def getMatrix(filename):
    matrix = []
    file = open(filename, "r")
    matrix = file.read()
    print("Solving this puzzle \n------------------")
    print(matrix)
    print()
    matrix = matrix.split()
    row1 = list(matrix)[:9]
    row2 = list(matrix)[9:18]
    row3 = list(matrix)[18:27]
    row4 = list(matrix)[27:36]
    row5 = list(matrix)[36:45]
    row6 = list(matrix)[45:54]
    row7 = list(matrix)[54:63]
    row8 = list(matrix)[63:72]
    row9 = list(matrix)[72:]
    matrix = [row1, row2, row3, row4, row5, row6, row7, row8, row9]
    
    for row in matrix:
        for i in row:
            if i == "x":
                row[row.index(i)] = set([1,2,3,4,5,6,7,8,9])
            else:
                row[row.index(i)] = set([int(i)])
                
    file.close()
    return matrix





def solve(groups, user_in):
    brute(groups, user_in)
    printInMatrix(matrix)
    return



def printInMatrix(matrix):
    for i in range(9):
            for j in range(9):
                if len(matrix[i][j]) != 1:
                    matrix[i][j] = "X"
    print(matrix)
    print()
    print()
    print()


def main(hhh):
    
    valid_input = True
    
    while valid_input:
        user_in = hhh #input("Please enter a Sudoku puzzle file name: ")
        try:
            file = open(user_in, "r")
            valid_input = False
        except IOError:
            print("No such file name. Please input a valid filename.")
            
    matrix = getMatrix(user_in)
        
    groups = CreateGroups(matrix)
    
    
    solve(groups, user_in)
    
    sys.exit()
        

        
        
    
    
if __name__ == "__main__":
    main("Sudoku2.txt")
