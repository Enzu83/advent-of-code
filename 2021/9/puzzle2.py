import numpy as np

# Custom input
input_data = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Functions

def increment_all(grid):
    for i in range(10):
        for j in range(10):
            grid[i, j] += 1

def get_neighbors(octopus):
    neighbors = set()

    i, j = octopus
    # Top-left corner
    if i == 0 and j == 0:
        neighbors.add((i, j+1))     # Bottom
        neighbors.add((i+1, j))     # Right
        neighbors.add((i+1, j+1))   # Bottom-Right
    
    # Top-right corner
    elif i == 9 and j == 0:
        neighbors.add((i-1, j))     # Left
        neighbors.add((i, j+1))     # Bottom
        neighbors.add((i-1, j+1))   # Bottom-Left

    # Bottom-left corner
    elif i == 0 and j == 9:
        neighbors.add((i, j-1))     # Top
        neighbors.add((i+1, j))     # Right
        neighbors.add((i+1, j-1))   # Top-Right

    # Bottom-right corner
    elif i == 9 and j == 9:
        neighbors.add((i-1, j))     # Left
        neighbors.add((i, j-1))     # Top
        neighbors.add((i-1, j-1))   # Top-Left

    # Left side
    elif i == 0:
        neighbors.add((i, j-1))     # Top
        neighbors.add((i, j+1))     # Bottom
        neighbors.add((i+1, j))     # Right
        neighbors.add((i+1, j-1))   # Top-Right
        neighbors.add((i+1, j+1))   # Bottom-Right

    # Right side
    elif i == 9:
        neighbors.add((i-1, j))     # Left
        neighbors.add((i, j-1))     # Top
        neighbors.add((i, j+1))     # Bottom
        neighbors.add((i-1, j-1))   # Top-Left
        neighbors.add((i-1, j+1))   # Bottom-Left
    
    # Top side
    elif j == 0:
        neighbors.add((i-1, j))     # Left
        neighbors.add((i, j+1))     # Bottom
        neighbors.add((i+1, j))     # Right
        neighbors.add((i-1, j+1))   # Bottom-Left
        neighbors.add((i+1, j+1))   # Bottom-Right

    # Bottom side
    elif j == 9:
        neighbors.add((i-1, j))     # Left
        neighbors.add((i, j-1))     # Top
        neighbors.add((i+1, j))     # Right
        neighbors.add((i-1, j-1))   # Top-Left
        neighbors.add((i+1, j-1))   # Top-Right

    # Base case
    else:
        neighbors.add((i-1, j))     # Left
        neighbors.add((i, j-1))     # Top
        neighbors.add((i, j+1))     # Bottom
        neighbors.add((i+1, j))     # Right
        neighbors.add((i-1, j-1))   # Top-Left
        neighbors.add((i-1, j+1))   # Bottom-Left
        neighbors.add((i+1, j-1))   # Top-Right
        neighbors.add((i+1, j+1))   # Bottom-Right

    return neighbors

def flash_octopus(grid, octopus):
    if grid[octopus] > 9:
        grid[octopus] = 0

        # Increment neighbors
        neighbors = get_neighbors(octopus)

        for neighbor in neighbors:
            if grid[neighbor] > 0:
                grid[neighbor] += 1
            
            flash_octopus(grid, neighbor)

def advance_step(grid):

    # Step 1 : All octopus energy +1
    increment_all(grid)

    # Step 2 : Check for flashing octopus (>9)
    for i in range(10):
        for j in range(10):
            octopus = (i, j)

            if grid[octopus] > 9:
                flash_octopus(grid, octopus)

def count_flashes(grid):
    flashes = 0

    for i in range(10):
        for j in range(10):
            if grid[i, j] == 0:
                flashes += 1
    
    return flashes


# Formatting
input_data = [list(line) for line in input_data]

for i in range(len(input_data)):
    for j in range(len(input_data[i])):
        input_data[i][j] = int(input_data[i][j])

input_data = np.matrix(input_data)

print(input_data)


# Code

step = 0
flashes = 0

while flashes < 100:
    advance_step(input_data)
    flashes = count_flashes(input_data)

    step += 1

print("First step: " + str(step))
