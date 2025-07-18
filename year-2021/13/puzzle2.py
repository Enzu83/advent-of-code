import numpy as np

# Custom input
input_data = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting
points = []
folds = []

for line in input_data:
    if line[:1] == 'f': #fold
        coordinate, index = line[11:].split('=')
        folds.append((coordinate, int(index)))
    
    elif line != "":
        x, y = line.split(',')
        points.append((int(x), int(y)))

# Functions

def init_grid(points):
    rows = max([point[1] for point in points]) + 1
    cols = max([point[0] for point in points]) + 1

    grid = np.zeros((rows, cols))

    for point in points:
        x = point[0]
        y = point[1]
        grid[y, x] = 1

    return grid


def fold_grid(grid, fold):
    coordinate, index = fold[0], fold[1]

    rows, cols = len(grid), len(grid[0])

    if coordinate == 'x':
        new_grid = np.zeros((rows, index))

        for x in range(index + 1, cols):
            for y in range(rows):
                new_grid[y, cols - 1 - x] = max(grid[y, x], grid[y, cols - 1 - x])

    elif coordinate == 'y':
        new_grid = np.zeros((index, cols))

        for x in range(cols):
            for y in range(index + 1, rows):
                new_grid[rows - 1 - y, x] = max(grid[y, x], grid[rows - 1 - y, x])

    else:
        raise ValueError("Unknown fold coordinate.")
    
    return new_grid

def print_grid(grid, fold=('', 0)):
    coordinate, index = fold

    for y in range(len(grid)):
        line = ""

        if coordinate == 'y' and y == index:
            line += (2 * len(grid[0]) - 1) * "_"
        else:
            for x in range(len(grid[0])):
                if x > 0:
                    line += " "
                
                if coordinate == 'x' and x == index:
                    line += "|"
                else:
                    if grid[y, x] == 1:
                        line += "#"
                    else:
                        line += "."
            
        print(line)
    
    print('')


# Code

grid = init_grid(points)

for fold in folds:
    grid = fold_grid(grid, fold)

print_grid(grid)