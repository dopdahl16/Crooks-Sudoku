import copy

def findNLevelUnions(my_list_of_unresolved_group_cells, master_list_of_all_unions):
    running_union = set()
    for cell in my_list_of_unresolved_group_cells:
        running_union = running_union.union(cell[3]) # would be cell.getVal() irl instead of cell[3]
    val_is_in_list = True
    try:
        master_list_of_all_unions.index(running_union)
    except:
        val_is_in_list = False
    if not val_is_in_list:
        master_list_of_all_unions.append(running_union)
    for unresolved_cell in my_list_of_unresolved_group_cells:
        insertion_index = my_list_of_unresolved_group_cells.index(unresolved_cell)
        my_list_of_unresolved_group_cells.remove(unresolved_cell)
        working_list = copy.copy(my_list_of_unresolved_group_cells)
        if len(working_list) == 1:
            return
        findNLevelUnions(working_list, master_list_of_all_unions)
        my_list_of_unresolved_group_cells.insert(insertion_index, unresolved_cell)
    return master_list_of_all_unions




master_list_of_all_unions = []
unresolved_group_cells = [[3, 1, 1, {2, 5, 6, 7, 8}], [3, 2, 1, {2, 5, 6, 7, 8}], [3, 3, 1, {8, 2, 5}], [1, 1, 1, {2, 4, 6, 7, 8}], [2, 1, 1, {2, 4, 5, 6}], [2, 2, 1, {2, 4, 5, 6}]]
print(findNLevelUnions(unresolved_group_cells, master_list_of_all_unions))
#no_compare = []
#for reference_cell in unresolved_group_cells:
    #print("Reference Cell: " + str(reference_cell))
    #no_compare.append(reference_cell)
    #for comparison_cell in unresolved_group_cells:
        #if not comparison_cell in no_compare:
            #print("-" + str(comparison_cell))

