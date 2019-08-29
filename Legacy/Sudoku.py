# Copyright (C) 2019 Daniel Opdahl (dopdahl16@gmail.com) Some Rights Reserved. 
# Permission to copy and modify is granted under the GNU General Public License v3.0 license
# Last revised 8/26/2019

def reduce(matrix, groups):
    changed = True
    while changed:
        changed = reduceGroups(groups)



def reduceGroups(groups):
    changed = False
    for group in groups:
        boo = reduceGroup(group)
        changed = boo or changed
    return changed



'''
#ORIGINAL
def reduceGroup(group):
    changed = False
    for set1 in group:
        if len(set1) == 1:
            rmitem = set1.pop()
            set1.add(rmitem)
            rmitem = set([rmitem])
            for j in group:
                if len(j) != 1:
                    p = j
                    j.difference_update(rmitem)
                    if p != j:
                        changed = True
        else:
            temp = set()
            for i in range(len(set1)):
                count = 0
                num = set1.pop()
                temp.add(num)
                for j in group:
                    if num in j:
                        count+=1
                if count == 0:
                    set1.clear()
                    set1.add(num)
                    return True
            for k in range(len(temp)):
                b = temp.pop()
                set1.add(b)
    return changed
'''



def reduceGroup(group):
    changed = False

    '''
    #Rule 1
    for index in range(9):
        count = 0

        for idx in range(9):
            if group[index] == group[idx]:
                count += 1

        if count == len(group[index]):
            for i in range(9):
                if group[index] != group[i]:
                    copyIndex = group[i].copy()

                    group[i].difference_update(group[index])

                    if copyIndex != group[i]:
                        changed = True

    #Rule 2
    for i in range(9):
        copyIndex = group[i].copy()

        for setI in group:
            copyIndex.difference_update(setI)

        if len(copyIndex) == 1:
            group[i].clear()
            group[i] = set(copyIndex)
            changed = True

            '''
    for set1 in group:
        if len(set1) == 1:
            rmitem = set1.pop()
            set1.add(rmitem)
            rmitem = set([rmitem])
            for j in group:
                if len(j) != 1:
                    p = j
                    j.difference_update(rmitem)
                    if p != j:
                        changed = True
        else:
            temp = set()
            for i in range(len(set1)):
                count = 0
                num = set1.pop()
                temp.add(num)
                for j in group:
                    if num in j:
                        count += 1
                if count == 0:
                    set1.clear()
                    set1.add(num)
                    return True
            for k in range(len(temp)):
                b = temp.pop()
                set1.add(b)
    print(group)
    return changed



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



def main():
    
    valid_input = True
    
    while valid_input:
        user_in = input("Please enter a Sudoku puzzle file name: ")
        try:
            file = open(user_in, "r")
            valid_input = False
        except IOError:
            print("No such file name. Please input a valid filename.")
            
    matrix = getMatrix(user_in)
    
    
    groups = []
    for n in range(0,9,3):
        for m in range(0,9,3):
            group = []
            for i in range(0,3):
                for j in range(0,3):
                    a = matrix[n+i][m+j]
                    group.append(a)
            groups.append(group)
    for row in matrix:
        groups.append(row)
    for row in range(9):
        group = []
        for i in range(9):
            group.append(matrix[i][row])
        groups.append(group)
        
        
    reduce(matrix, groups)
    solved = user_in[:len(user_in)-4] + "_solved.txt"
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

    

if __name__ == "__main__":
    main()
