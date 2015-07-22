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
        if (val > 0): self.possibility_set.remove(val)

class NodeGroup:
    def __init__(self):
        self.nodes = []
        self.found = []


class Sudoku:
    def Solve(self, grid_in, grid_out, max_passes=1):
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
                if gr[i].found.count(x.value) > 1:
                    print "Too many numbers in group!"
                    return False
                
                # Add to column group
                gc[j].nodes.append(x)
                if x.value > 0: gc[j].found.append(x.value)
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
                if gs[k].found.count(x.value) > 1:
                    print "Too many numbers in group!"
                    return False
            
            # Add groups to main group structure
            for x in range(9):
                groups.append(gc[x])
                groups.append(gr[x])
                groups.append(gs[x])
        
        ### Solve ###
        # Single pass
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

                # If the possibility set is reduced to 1, set the value
                if len(n.possibility_set) == 1:
                    n.value = n.possibility_set[0] # Leave solved value in list for other algorithms
                    g.found.append(n.value) # TODO: Link with other groups and update those
        
        # Update grid with solved nodes
        for i in range(9):
            for j in range(9):
                grid_out.contents[i][j] = nodes[i][j].value

        return grid_out



if __name__ == "__main__":
    print "Hello!"
    sudoku = Sudoku()
    solved = Grid()
    
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










