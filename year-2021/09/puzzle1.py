import numpy as np

# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting
input_data = [list(line) for line in input_data]

for i in range(len(input_data)):
    for j in range(len(input_data[i])):
        input_data[i][j] = int(input_data[i][j])

input_data = np.array(input_data)

print(input_data)

# Functions

def get_neighbors(grid, pos):
    neighbors = set()

    i, j = pos
    # Top-left corner
    if i == 0 and j == 0:
        neighbors.add(grid[i][j+1])     # Bottom
        neighbors.add(grid[i+1][j])     # Right
    
    # Top-right corner
    elif i == len(grid)-1 and j == 0:
        neighbors.add(grid[i-1][j])     # Left
        neighbors.add(grid[i][j+1])     # Bottom

    # Bottom-left corner
    elif i == 0 and j == len(grid[0])-1:
        neighbors.add(grid[i][j-1])     # Top
        neighbors.add(grid[i+1][j])     # Right

    # Bottom-right corner
    elif i == len(grid)-1 and j == len(grid[0])-1:
        neighbors.add(grid[i-1][j])     # Left
        neighbors.add(grid[i][j-1])     # Top

    # Left side
    elif i == 0:
        neighbors.add(grid[i][j-1])     # Top
        neighbors.add(grid[i][j+1])     # Bottom
        neighbors.add(grid[i+1][j])     # Right

    # Right side
    elif i == len(grid)-1:
        neighbors.add(grid[i-1][j])     # Left
        neighbors.add(grid[i][j-1])     # Top
        neighbors.add(grid[i][j+1])     # Bottom
    
    # Top side
    elif j == 0:
        neighbors.add(grid[i-1][j])     # Left
        neighbors.add(grid[i][j+1])     # Bottom
        neighbors.add(grid[i+1][j])     # Right

    # Bottom side
    elif j == len(grid[0])-1:
        neighbors.add(grid[i-1][j])     # Left
        neighbors.add(grid[i][j-1])     # Top
        neighbors.add(grid[i+1][j])     # Right

    # Base case
    else:
        neighbors.add(grid[i-1][j])     # Left
        neighbors.add(grid[i][j-1])     # Top
        neighbors.add(grid[i][j+1])     # Bottom
        neighbors.add(grid[i+1][j])     # Right

    return neighbors

def check_low(point, neighbors):
    for neighbor in neighbors:
        if neighbor <= point:
            return False
    
    return True

def get_low_points(grid):
    low_points = {}

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            point = grid[i][j]
            neighbors = get_neighbors(grid, (i, j))
    
            if check_low(point, neighbors):
                if point not in low_points:
                    low_points[int(point)] = 1
                else:
                    low_points[int(point)] += 1

    return low_points

def risk_sum(dic):
    res = 0

    for key in dic:
        res += dic[key] * (key + 1)
    
    return res

# Code

low_points = get_low_points(input_data)

print(low_points)

print(risk_sum(low_points))


