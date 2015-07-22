#!/usr/bin/python

print("Welcome to Sudoku Solver")

blank_grid_content = []
for i in range(9):
    blank_grid_content.append([])
    for j in range(9):
        blank_grid_content[i].append(0)


class Grid:
    
    def __init__(self):
        self.contents = []
        for i in range(9):
            self.contents.append([])
            for j in range(9):
                self.contents[i].append(0)
                self.contents[i][j] = blank_grid_content[i][j]
    
    def display(self):
        line = ""
        print "--------------------------"
        for i in range(9):
            line += "| "
            for j in range(9):
                if self.contents[i][j] > 0:
                    line = line + str(self.contents[i][j]) + " "
                else:
                    line = line + "_ "
                if j in [2, 5]:
                    line += "| "
            line += "| "
            print line
            if i in [2, 5]:
                print "--------------------------"
            line = ""
        print "--------------------------"
            
    def copy_to(self, dest):
        for i in range(9):
            for j in range(9):
                dest.contents[i][j] = 0
                dest.contents[i][j] += self.contents[i][j]



class Node:
    def __init__(self, val):
        self.value = val
        self.possibility_set = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        if (val > 0): self.possibility_set = [val]

class NodeGroup:
    def __init__(self):
        self.nodes = []
        self.found = []


class Sudoku:
    def Solve(self, grid_in, grid_out, level=1, max_passes=1):
        grid = grid_out
        grid_in.copy_to(grid_out)
        
        ### Generate Nodes ###
        # Generate grid of nodes from numbers
        nodes = []
        for i in range(9):
            nodes.append([])
            for j in range(9):
                n = Node(grid.contents[i][j])
                nodes[i].append(n)
        
        ### Generate Node Groups ###
        # Generate node groups from rows
        groups = []
        gc = [] # Column groups
        gr = [] # Row groups
        gs = [] # Square groups
        
        # Create groups
        for x in range(9):
            gc.append(NodeGroup())
            gr.append(NodeGroup())
            gs.append(NodeGroup())
        
        # Itterate through each node and add to all applicable groups
        for i in range(9):
            for j in range(9):
                x = nodes[i][j]
                
                # Add to row group
                gr[i].nodes.append(x)
                if x.value > 0: gr[i].found.append(x.value)
                x.gr = gr[i]
                x.i = i
                if gr[i].found.count(x.value) > 1:
                    print "Too many numbers in group!"
                    return False
                
                # Add to column group
                gc[j].nodes.append(x)
                if x.value > 0: gc[j].found.append(x.value)
                x.gc = gc[j]
                x.j = j
                if gc[j].found.count(x.value) > 1:
                    print "Too many numbers in group!"
                    return False
            
                # Add to square group
                k = 0
                if   i < 3 and j < 3: k = 0
                elif i < 3 and j < 6: k = 1
                elif i < 3 and j < 9: k = 2
                elif i < 6 and j < 3: k = 3
                elif i < 6 and j < 6: k = 4
                elif i < 6 and j < 9: k = 5
                elif i < 9 and j < 3: k = 6
                elif i < 9 and j < 6: k = 7
                elif i < 9 and j < 9: k = 8
                gs[k].nodes.append(x)
                if x.value > 0: gs[k].found.append(x.value)
                x.gs = gs[k]
                x.k = k
                if gs[k].found.count(x.value) > 1:
                    print "Too many numbers in group!"
                    return False
            
            # Add groups to main group structure
            for x in range(9):
                groups.append(gc[x])
                groups.append(gr[x])
                groups.append(gs[x])
        
        ### Solve ###
        for pass_i in range(max_passes):
            # For each node in each group
            for g in groups:
                for n in g.nodes:
                    # If has a value, make sure the node group is updated
                    # TODO: Make this automatic at assignment, optimize first statements
                    if n.value > 0 and g.found.count(n.value) == 0:
                        g.found.append(n.value)
                        continue
                    
                    # If already solved, don't continue with algorithms
                    if n.value > 0: continue
                    
                    # Remove all found in group from possibility list
                    for f in g.found:
                        if f in n.possibility_set: n.possibility_set.remove(f)
                    
                    # Determine if there are any unique possibility values
                    # Makes much slower, use for intermediate level
                    if level >= 2:
                        for possible_v in n.possibility_set:
                            possible_v_unique = True
                            
                            for other_n in g.nodes:
                                if n == other_n: continue
                                if other_n.possibility_set.count(possible_v) > 0:
                                    possible_v_unique = False

                            if possible_v_unique == True: #Found!
                                n.possibility_set = [possible_v]
                    
                    # Do eliminations based on possibility set eliminations, sets of 2
                    # Makes much slower, used for advanced level-
                    if level >= 3:
                        pos_len = len(n.possibility_set)
                        if pos_len == 2:
                            for other_n in g.nodes:
                                if n == other_n: continue
                                if len(other_n.possibility_set) == 2:
                                    same = True
                                    for v in n.possibility_set:
                                        if other_n.possibility_set.count(v) == 0: same = False
                                    if same: # Two nodes with same possibility sets of 2
                                    # remove possibilities from other nodes in group
                                        for node_cleaning in g.nodes:
                                            if n == node_cleaning or other_n == node_cleaning: continue
                                            for v in n.possibility_set:
                                                if node_cleaning.possibility_set.count(v) > 0: 
                                                    node_cleaning.possibility_set.remove(v)
                                                    #print "Cleaning from pair " + str(v) + " from (" + str(node_cleaning.i+1) + "," + \
                                                    #    str(node_cleaning.j+1) + "," + str(node_cleaning.k+1) + ")"

                    
                    # Row/col and square overlap, so the value in a row/col must be in a square, 
                    #   eliminating it from the rest of the row/col
                    if level >= 4:
                        # For each possibility value
                        for v in n.possibility_set:
                            # For the square, check if the value occurs in another row
                            occurs = False
                            row_in_sq = set(n.gs.nodes) & set(n.gr.nodes)
                            for other_sq_n in n.gs.nodes:
                                if other_sq_n in row_in_sq: continue
                                if v in other_sq_n.possibility_set:
                                    occurs = True

                            # If not, row elimination of possibility value from all other nodees in row
                            if occurs == False:
                                for node_cleaning in (set(n.gr.nodes) - row_in_sq):
                                    if node_cleaning.possibility_set.count(v) > 0:
                                        node_cleaning.possibility_set.remove(v)

                            # For the square, check if the value occurs in another column 
                            occurs = False
                            col_in_sq = set(n.gs.nodes) & set(n.gc.nodes)
                            for other_sq_n in n.gs.nodes:
                                if other_sq_n in col_in_sq: continue
                                if v in other_sq_n.possibility_set:
                                    occurs = True

                            # If not, column elimination of possibility value from all other nodees in column
                            if occurs == False:
                                for node_cleaning in (set(n.gc.nodes) - col_in_sq):
                                    if node_cleaning.possibility_set.count(v) > 0:
                                        node_cleaning.possibility_set.remove(v)

                    # Do eliminations based on possibility set eliminations, sets of 3
                    # Makes much slower, used for advanced level
                    if level >= 5:
                        pos_len = len(n.possibility_set)
                        if pos_len == 3:
                            matching_nodes = [n]
                            for other_n in g.nodes:
                                if n == other_n: continue
                                if len(other_n.possibility_set) == 3:
                                    same = True
                                    for v in n.possibility_set:
                                        if other_n.possibility_set.count(v) == 0: same = False
                                    if same: # Found another matching node, add to set
                                        matching_nodes.append(other_n)
                            if len(matching_nodes) > 3: print "Something weird in triplets, check it out..."
                            if len(matching_nodes) == 3:
                                print "Triplet!"
                                # remove possibilities from other nodes in group
                                for node_cleaning in g.nodes:
                                    if node_cleaning in matching_nodes: continue
                                    for v in n.possibility_set:
                                        if node_cleaning.possibility_set.count(v) > 0: 
                                            node_cleaning.possibility_set.remove(v)
                                            #print "Cleaning from triplet " + str(v) + " from (" + str(node_cleaning.i+1) + "," + \
                                            #    str(node_cleaning.j+1) + "," + str(node_cleaning.k+1) + ")"
                    
                    # Check for 3 complimentary cells, such as 12 23 13 or 123 23 13
                    if level >= 6:
                        if len(n.possibility_set) == 2 or len(n.possibility_set) == 3:
                            # Generate list of nodes with only 2 possibilities in group
                            two_possibility_nodes = []
                            for other_n in g.nodes:
                                if other_n == n: continue
                                if len(other_n.possibility_set) == 2 or len(other_n.possibility_set) == 3: 
                                    two_possibility_nodes.append(other_n)
                            # Are there enough nodes for a set?
                            if len(two_possibility_nodes) >= 2:
                                # Look for two complimentary nodes with current node
                                for test_n in two_possibility_nodes:
                                    superset = (set(n.possibility_set)|set(test_n.possibility_set))
                                    if len(superset) > 3: continue # Make sure first two nodes match and the set is less than or equal to 3
                                    for test_n2 in set(two_possibility_nodes) - set([test_n]):
                                        if ( superset & set(test_n2.possibility_set) ) == set(test_n2.possibility_set):
                                            # Found complimentary three set
                                            # Remove numbers in set from all other nodes in group
                                            if set(test_n2.possibility_set) == set(test_n.possibility_set) or \
                                                set(test_n2.possibility_set) == set(n.possibility_set) or \
                                                set(test_n.possibility_set) == set(n.possibility_set):
                                                #print "Weird thing with triples, catch this."
                                                continue
                                            for node_cleaning in (set(g.nodes) - set([n,test_n,test_n2])):
                                                for v in superset:
                                                    if node_cleaning.possibility_set.count(v) > 0:
                                                        node_cleaning.possibility_set.remove(v)
                                                        #print superset
                                                        #print "Cleaning from triple pair " + str(v) + " from (" + str(node_cleaning.i+1) + "," + \
                                                        #    str(node_cleaning.j+1) + "," + str(node_cleaning.k+1) + ") on (" + str(n.i+1) + str(n.j+1) + str(n.k+1) + ")"
                                                        #print "Details: " + str(test_n.i+1) + str(test_n.j+1) + str(test_n.k+1) + " " + str(test_n2.i+1) + str(test_n2.j+1) + str(test_n2.k+1)
                    # Check for X-Wings
                    if level >= 7:
                        # For each number in the possibility set
                        for v in n.possibility_set:
                            # Is the node part of a locked pair (the only possible pair of a number in a row)
                            locked_pair = False
                            other_count = 0
                            other_node = None
                            for other_n in n.gr.nodes:
                                if other_n == n: continue
                                if other_n.possibility_set.count(v) > 0: 
                                    other_count += 1
                                    other_node = other_n
                                    locked_pair = True
                                if other_count > 1: 
                                    locked_pair = False
                                    break

                            if locked_pair:
                                # If so, is there a complimentary locked pair of the same number (forming an X)
                                comp_locked_pair = False
                                for other_n in n.gc.nodes:
                                    if other_n == n: continue
                                    if other_n.possibility_set.count(v) == 0: continue
                                    other_count = 0
                                    locked_pair2 = False
                                    other_node2 = None
                                    for other_n2 in other_n.gr.nodes:
                                        if other_n2 == other_n: continue
                                        if other_n2.possibility_set.count(v) == 0: continue
                                        other_count += 1
                                        other_node2 = other_n2
                                        locked_pair2 = True
                                        if other_count > 1: 
                                            locked_pair2 = False
                                            break
                                    
                                    if locked_pair2 == True: # Found locked pair, check if it's complimentary
                                        if other_node.j == other_node2.j:
                                            comp_locked_pair = True
                                            #print "Two locked pairs! " + str(other_node.j) + str(other_node2.j)

                                    if comp_locked_pair:
                                        print "Found X-wing!" 
                                        #for node_cleaning in 

                            # If so, get rid of other occurences of the number in the corresponding col

                            # Repeat for columns
                            locked_pair = False
                            other_count = 0
                            other_node = None
                            for other_n in n.gc.nodes:
                                if other_n == n: continue
                                if other_n.possibility_set.count(v) > 0: 
                                    other_count += 1
                                    other_node = other_n
                                    locked_pair = True
                                if other_count > 1: 
                                    locked_pair = False
                                    break

                            if locked_pair:
                                # If so, is there a complimentary locked pair of the same number (forming an X)
                                comp_locked_pair = False
                                for other_n in n.gr.nodes:
                                    if other_n == n: continue
                                    if other_n.possibility_set.count(v) == 0: continue
                                    other_count = 0
                                    locked_pair2 = False
                                    other_node2 = None
                                    for other_n2 in other_n.gc.nodes:
                                        if other_n2 == other_n: continue
                                        if other_n2.possibility_set.count(v) == 0: continue
                                        other_count += 1
                                        other_node2 = other_n2
                                        locked_pair2 = True
                                        if other_count > 1: 
                                            locked_pair2 = False
                                            break
                                    
                                    if locked_pair2 == True: # Found locked pair, check if it's complimentary
                                        if other_node.i == other_node2.i:
                                            comp_locked_pair = True
                                            #print "Two locked pairs! " + str(other_node.i) + str(other_node2.i)

                                    if comp_locked_pair:
                                        print "Found X-wing!" 



                    # Brute force try things, not elegant but should always work
                    #if level >= 10:

                    # If the possibility set is reduced to 1, set the value
                    if len(n.possibility_set) == 1:
                        n.value = n.possibility_set[0] # Leave solved value in list for other algorithms
                        g.found.append(n.value) # TODO: Link with other groups and update those

            print "Pass "+str(pass_i+1)+" ..."
            # Determine if solved
            done = True
            for i in range(9):
                if len(gr[i].found) < 9: done = False
            if done:
                print "done!"
                break


        # Update grid with solved nodes
        for i in range(9):
            line = ""
            for j in range(9):
                grid_out.contents[i][j] = nodes[i][j].value
                line += str(nodes[i][j].possibility_set) + "\t"
            #print line

        return grid_out



if __name__ == "__main__":
    print "Hello!"
    sudoku = Sudoku()
    solved = Grid()
    
    if False:
        print "Empty grid"
        first_test_grid = Grid()
        first_test_grid.display()
        solved = sudoku.Solve(first_test_grid,solved)
        solved.display()

        print "Top row, number 9 missing"
        row_test_grid = Grid()
        row_test_grid.contents[0] = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        row_test_grid.display()
        solved = sudoku.Solve(row_test_grid, solved)
        solved.display()

        print "Top row, number 6 missing"
        row_test_grid = Grid()
        row_test_grid.contents[0] = [1, 2, 3, 4, 5, 0, 7, 8, 9]
        row_test_grid.display()
        solved = sudoku.Solve(row_test_grid, solved)
        solved.display()

        print "Fifth row, number 1 missing"
        row_test_grid = Grid()
        row_test_grid.contents[4] = [0, 2, 3, 4, 5, 6, 7, 8, 9]
        row_test_grid.display()
        solved = sudoku.Solve(row_test_grid, solved)
        solved.display()

        print "First column, number 2 missing"
        row_test_grid = Grid()
        row_test_grid.contents[0][0] = 1
        row_test_grid.contents[1][0] = 0
        row_test_grid.contents[2][0] = 3
        row_test_grid.contents[3][0] = 4
        row_test_grid.contents[4][0] = 5
        row_test_grid.contents[5][0] = 6
        row_test_grid.contents[6][0] = 7
        row_test_grid.contents[7][0] = 8
        row_test_grid.contents[8][0] = 9
        row_test_grid.display()
        solved = sudoku.Solve(row_test_grid, solved)
        solved.display()

        print "Middle square, number 4 missing"
        row_test_grid = Grid()
        row_test_grid.contents[3][3] = 1
        row_test_grid.contents[4][3] = 2
        row_test_grid.contents[5][3] = 3
        row_test_grid.contents[3][4] = 0
        row_test_grid.contents[4][4] = 5
        row_test_grid.contents[5][4] = 6
        row_test_grid.contents[3][5] = 7
        row_test_grid.contents[4][5] = 8
        row_test_grid.contents[5][5] = 9
        row_test_grid.display()
        solved = sudoku.Solve(row_test_grid, solved)
        solved.display()

        print "Medley 1 - Easy"
        row_test_grid = Grid()
        row_test_grid.contents[3][3] = 1
        row_test_grid.contents[4][3] = 2
        row_test_grid.contents[5][3] = 3
        row_test_grid.contents[3][4] = 0
        row_test_grid.contents[4][4] = 5
        row_test_grid.contents[5][4] = 6
        row_test_grid.contents[8][5] = 7
        row_test_grid.contents[4][5] = 8
        row_test_grid.contents[5][5] = 9
        row_test_grid.display()
        solved = sudoku.Solve(row_test_grid, solved)
        solved.display()

        print "Medley 2 - Medium"
        row_test_grid = Grid()
        row_test_grid.contents[0] = [0,0,0, 0,0,0, 0,0,0]
        row_test_grid.contents[1] = [0,0,0, 0,0,0, 0,0,0]
        row_test_grid.contents[2] = [0,0,0, 0,0,0, 0,0,0]
        
        row_test_grid.contents[3] = [0,0,0, 1,0,0, 0,0,0]
        row_test_grid.contents[4] = [0,0,0, 2,5,8, 0,0,0]
        row_test_grid.contents[5] = [0,0,0, 3,6,9, 0,0,0]
        
        row_test_grid.contents[6] = [7,0,0, 4,1,0, 0,0,5]
        row_test_grid.contents[7] = [0,0,0, 8,2,0, 0,0,0]
        row_test_grid.contents[8] = [0,5,0, 9,3,0, 0,0,0]
        row_test_grid.display()
        solved = sudoku.Solve(row_test_grid, solved)
        solved.display()
        
        print "Medley 3 - Crossout"
        row_test_grid = Grid()
        row_test_grid.contents[0] = [1,0,0, 0,0,0, 0,0,0]
        row_test_grid.contents[1] = [0,0,0, 0,0,0, 0,0,0]
        row_test_grid.contents[2] = [0,0,0, 1,0,0, 0,0,0]
        
        row_test_grid.contents[3] = [0,0,0, 0,0,0, 1,0,0]
        row_test_grid.contents[4] = [0,1,0, 0,0,0, 0,0,0]
        row_test_grid.contents[5] = [0,0,0, 0,1,0, 0,0,0]
        
        row_test_grid.contents[6] = [0,0,1, 0,0,0, 0,0,0]
        row_test_grid.contents[7] = [0,0,0, 0,0,1, 0,0,0]
        row_test_grid.contents[8] = [0,0,0, 0,0,0, 0,1,0]
        row_test_grid.display()
        solved = sudoku.Solve(row_test_grid, solved)
        solved.display()

        print "Real 1 - Easy"
        row_test_grid = Grid()
        row_test_grid.contents[0] = [1,4,2, 0,9,0, 0,0,5]
        row_test_grid.contents[1] = [7,0,0, 4,0,0, 0,8,9]
        row_test_grid.contents[2] = [8,0,5, 0,0,0, 0,2,4]
        
        row_test_grid.contents[3] = [2,0,0, 0,0,4, 8,0,0]
        row_test_grid.contents[4] = [0,3,0, 0,0,1, 2,6,0]
        row_test_grid.contents[5] = [0,8,0, 0,7,2, 9,4,1]
        
        row_test_grid.contents[6] = [0,5,0, 2,0,6, 0,0,0]
        row_test_grid.contents[7] = [0,2,8, 0,0,9, 4,1,0]
        row_test_grid.contents[8] = [0,7,9, 1,0,8, 5,3,0]
        row_test_grid.display()
        solved = sudoku.Solve(row_test_grid, solved)
        solved.display()

        print "Real 2 - Easy"
        row_test_grid = Grid()
        row_test_grid.contents[0] = [1,0,0, 0,9,4, 7,0,5]
        row_test_grid.contents[1] = [5,7,3, 1,0,2, 0,0,0]
        row_test_grid.contents[2] = [0,4,0, 0,5,3, 1,0,8]
        
        row_test_grid.contents[3] = [0,8,1, 5,6,7, 3,4,0]
        row_test_grid.contents[4] = [0,0,0, 8,0,1, 0,0,7]
        row_test_grid.contents[5] = [0,5,6, 4,0,9, 0,0,2]
        
        row_test_grid.contents[6] = [4,6,0, 0,0,0, 0,9,0]
        row_test_grid.contents[7] = [0,3,0, 9,1,0, 0,7,6]
        row_test_grid.contents[8] = [9,0,0, 0,4,0, 0,0,0]
        row_test_grid.display()
        solved = sudoku.Solve(row_test_grid, solved)
        solved.display()

        print "Real 3 - Medium"
        row_test_grid = Grid()
        row_test_grid.contents[0] = [3,9,0, 4,0,6, 0,0,0]
        row_test_grid.contents[1] = [0,0,7, 0,0,0, 3,0,2]
        row_test_grid.contents[2] = [0,0,6, 3,7,0, 5,0,0]
        
        row_test_grid.contents[3] = [0,0,3, 0,4,9, 0,0,0]
        row_test_grid.contents[4] = [7,6,0, 0,0,0, 4,5,0]
        row_test_grid.contents[5] = [9,0,4, 0,6,7, 0,1,0]
        
        row_test_grid.contents[6] = [1,5,0, 0,3,0, 0,2,6]
        row_test_grid.contents[7] = [4,0,0, 0,0,0, 0,0,0]
        row_test_grid.contents[8] = [0,0,9, 0,0,2, 0,4,7]
        row_test_grid.display()
        solved = sudoku.Solve(row_test_grid, solved)
        solved.display()

        print "Real 4 - Hard"
        row_test_grid = Grid()
        row_test_grid.contents[0] = [0,0,0, 0,0,0, 0,0,6]
        row_test_grid.contents[1] = [1,0,0, 0,0,0, 0,8,9]
        row_test_grid.contents[2] = [0,2,4, 3,0,0, 0,0,0]

        row_test_grid.contents[3] = [0,4,0, 8,0,0, 7,0,1]
        row_test_grid.contents[4] = [6,0,0, 0,0,2, 5,0,0]
        row_test_grid.contents[5] = [9,1,0, 0,0,0, 0,0,0]
        
        row_test_grid.contents[6] = [0,0,1, 0,0,9, 0,0,0]
        row_test_grid.contents[7] = [0,9,8, 0,0,3, 4,1,0]
        row_test_grid.contents[8] = [0,0,2, 0,7,1, 0,0,0]
        row_test_grid.display()
        solved = sudoku.Solve(row_test_grid, solved)
        solved.display()
        
        print "Real 5 - Hard"
        row_test_grid = Grid()
        row_test_grid.contents[0] = [2,1,0, 6,0,0, 0,8,0]
        row_test_grid.contents[1] = [5,4,0, 0,0,0, 0,1,0]
        row_test_grid.contents[2] = [0,3,0, 2,0,0, 9,4,0]
        
        row_test_grid.contents[3] = [1,0,2, 0,5,0, 4,0,0]
        row_test_grid.contents[4] = [0,0,8, 0,9,0, 6,0,0]
        row_test_grid.contents[5] = [0,0,0, 0,4,0, 0,0,1]
        
        row_test_grid.contents[6] = [0,0,0, 4,0,0, 0,3,5]
        row_test_grid.contents[7] = [0,0,0, 0,0,0, 0,0,4]
        row_test_grid.contents[8] = [7,0,0, 9,0,0, 0,0,0]
        row_test_grid.display()
        solved = sudoku.Solve(row_test_grid, solved, level=2)
        solved.display()
    
    if False:
        # Test doesn't work
        print "Medley 4 - Induction"
        row_test_grid = Grid()
        row_test_grid.contents[0] = [0,0,0, 0,0,0, 0,0,0]
        row_test_grid.contents[1] = [4,5,6, 0,0,0, 0,0,0]
        row_test_grid.contents[2] = [0,0,0, 0,0,0, 1,2,3]
        
        row_test_grid.contents[3] = [0,0,0, 2,7,0, 0,0,0]
        row_test_grid.contents[4] = [0,0,0, 3,0,0, 0,0,0]
        row_test_grid.contents[5] = [0,0,0, 0,0,0, 0,0,0]
        
        row_test_grid.contents[6] = [0,0,0, 0,2,7, 0,0,0]
        row_test_grid.contents[7] = [0,0,0, 0,0,3, 0,0,0]
        row_test_grid.contents[8] = [0,0,0, 0,0,0, 0,0,0]
        row_test_grid.display()
        solved = sudoku.Solve(row_test_grid, solved, level=2, max_passes = 1)
        solved.display()

    if True:
        print "Real 6 - Evil"
        row_test_grid = Grid()
        row_test_grid.contents[0] = [0,5,0, 2,0,0, 1,0,0]
        row_test_grid.contents[1] = [0,7,0, 0,3,1, 0,8,6]
        row_test_grid.contents[2] = [3,0,0, 0,0,0, 0,0,0]
        
        row_test_grid.contents[3] = [0,3,0, 1,0,2, 0,0,7]
        row_test_grid.contents[4] = [0,8,0, 0,0,0, 0,4,0]
        row_test_grid.contents[5] = [2,0,0, 9,0,3, 0,1,0]
        
        row_test_grid.contents[6] = [0,0,0, 0,0,0, 0,0,9]
        row_test_grid.contents[7] = [4,2,0, 6,7,0, 0,3,0]
        row_test_grid.contents[8] = [0,0,3, 0,0,5, 0,6,0]
        row_test_grid.display()
        solved = sudoku.Solve(row_test_grid, solved, level=100, max_passes = 2)
        solved.display()

    if True and False:
        print "Real 6 - Hardest (11 Star)"
        row_test_grid = Grid()
        row_test_grid.contents[0] = [8,0,0, 0,0,0, 0,0,0]
        row_test_grid.contents[1] = [0,0,3, 6,0,0, 0,0,0]
        row_test_grid.contents[2] = [0,7,0, 0,9,0, 2,0,0]
        
        row_test_grid.contents[3] = [0,5,0, 0,0,7, 0,0,0]
        row_test_grid.contents[4] = [0,0,0, 0,4,5, 7,0,0]
        row_test_grid.contents[5] = [0,0,0, 1,0,0, 0,3,0]
        
        row_test_grid.contents[6] = [0,0,1, 0,0,0, 0,6,8]
        row_test_grid.contents[7] = [0,0,8, 5,0,0, 0,1,0]
        row_test_grid.contents[8] = [0,9,0, 0,0,0, 4,0,0]
        row_test_grid.display()
        solved = sudoku.Solve(row_test_grid, solved, level=100, max_passes = 3)
        solved.display()
    
    exit()
    
    print ""
    row_test_grid = Grid()
    row_test_grid.contents[0] = []
    row_test_grid.contents[1] = []
    row_test_grid.contents[2] = []

    row_test_grid.contents[3] = []
    row_test_grid.contents[4] = []
    row_test_grid.contents[5] = []
                             
    row_test_grid.contents[6] = []
    row_test_grid.contents[7] = []
    row_test_grid.contents[8] = []
    row_test_grid.display()
    solved = sudoku.Solve(row_test_grid, solved)
    solved.display()

    print ""
    row_test_grid = Grid()
    row_test_grid.contents[0] = [8,0,0, 0,0,0, 0,0,0]
    row_test_grid.contents[1] = [0,0,0, 0,0,0, 0,0,0]
    row_test_grid.contents[2] = [0,0,0, 0,0,0, 0,0,0]
    
    row_test_grid.contents[3] = [0,0,0, 0,0,0, 0,0,0]
    row_test_grid.contents[4] = [0,0,0, 0,0,0, 0,0,0]
    row_test_grid.contents[5] = [0,0,0, 0,0,0, 0,0,0]
    
    row_test_grid.contents[6] = [0,0,0, 0,0,0, 0,0,0]
    row_test_grid.contents[7] = [0,0,0, 0,0,0, 0,0,0]
    row_test_grid.contents[8] = [0,0,0, 0,0,0, 0,0,0]
    row_test_grid.display()
    solved = sudoku.Solve(row_test_grid, solved, level=100, max_passes = 2)
    solved.display()











