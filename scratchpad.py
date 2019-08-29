unresolved_group_cells = [[3, 1, 1, {2, 5, 6, 7, 8}], [3, 2, 1, {2, 5, 6, 7, 8}], [3, 3, 1, {8, 2, 5}], [1, 1, 1, {2, 4, 6, 7, 8}], [2, 1, 1, {2, 4, 5, 6}], [2, 2, 1, {2, 4, 5, 6}]]
unresolved_group_cells
[[3, 1, 1, {2, 5, 6, 7, 8}], [3, 2, 1, {2, 5, 6, 7, 8}], [3, 3, 1, {8, 2, 5}], [1, 1, 1, {2, 4, 6, 7, 8}], [2, 1, 1, {2, 4, 5, 6}], [2, 2, 1, {2, 4, 5, 6}]]
### Do this if open spaces in group is equal to 2:
no_compare = []
for reference_cell in unresolved_group_cells:
    print("Reference Cell: " + str(reference_cell))
    no_compare.append(reference_cell)
    for comparison_cell in unresolved_group_cells:
        if not comparison_cell in no_compare:
            print("-" + str(comparison_cell))