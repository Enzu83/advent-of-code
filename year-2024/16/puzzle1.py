# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

# (y, x)
grid = [[cell for cell in row] for row in input_data]

# Functions

def getNeighbors(grid, cell):
    y, x, orientation = cell

    neighbors = set()

    # possible neighbor directly in front
    if orientation == 0 and y > 0 and grid[y - 1][x] != '#':
        neighbors.add((y - 1, x, orientation))
    
    elif orientation == 90 and x > 0 and grid[y][x - 1] != '#':
        neighbors.add((y, x - 1, orientation))
    
    elif orientation == 180 and y < len(grid)-1 and grid[y + 1][x] != '#':
        neighbors.add((y + 1, x, orientation))
    
    elif orientation == 270 and x < len(grid[0])-1 and grid[y][x + 1] != '#':
        neighbors.add((y, x + 1, orientation))

    # the 2 turn (clockwise and counterclockwise)
    neighbors.add((y, x, (orientation + 90) % 360))
    neighbors.add((y, x, (orientation - 90) % 360))


    return neighbors

def computeCost(current_cell, neighbor_cell):
    # check if the orientations are identical
    if current_cell[2] == neighbor_cell[2]:
        return 1
    # else: a turn needs to be performed
    else:
        return 1000

def getMinimumCostCell(cells, costs):
    return min(cells, key=lambda cell: costs[cell])

def getBestCost(grid, start, end, initial_orientation):
    # orientations
    # up: 0
    # left: 90
    # down: 180
    # right: 270

    # graph
    remaining_cells = {(y, x, orientation) for orientation in {0, 90, 180, 270} for x in range(len(grid[0])) for y in range(len(grid)) if grid[y][x] != '#'}
    costs = {cell: float("inf") for cell in remaining_cells}
    costs[(start[0], start[1], initial_orientation)] = 0

    # exploration
    while remaining_cells:
        current = getMinimumCostCell(remaining_cells, costs)
        remaining_cells.remove(current)

        for neighbor in getNeighbors(grid, current):
            if neighbor in remaining_cells:
                new_cost = costs[current] + computeCost(current, neighbor)

                if new_cost < costs[neighbor]:
                    costs[neighbor] = new_cost
    
    return min(costs[(end[0], end[1], orientation)] for orientation in {0, 90, 180, 270})

# Code

start = (len(grid)-2, 1)
end = (1, len(grid[0])-2)

print(getBestCost(grid, start, end, 270))