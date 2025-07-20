# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

height_grid = [[int(height) for height in input_data[i]] for i in range(len(input_data))]


# Functions

def printGrid(grid):
    for i in range(len(grid)):
        for height in grid[i]:
            print(height, end="")
        
        print("")

def printVisited(grid, visited):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) in visited:
                print(getHeight(grid, (i, j)), end="")
            else:
                print('.', end="")
        
        print("")

def getZeros(grid):
    return set([(i, j) for j in range(len(grid[0])) for i in range(len(grid)) if grid[i][j] == 0])

def getNeighbors(grid, point):
    neighbors = set()

    i, j = point

    if i > 0:
        neighbors.add((i - 1, j))
    
    if j > 0:
        neighbors.add((i, j - 1))
    
    if i < len(grid) - 1:
        neighbors.add((i + 1, j))
    
    if j < len(grid[0]) - 1:
        neighbors.add((i, j + 1))
    
    return neighbors

def getHeight(grid, point):
    return grid[point[0]][point[1]]

def getTrailheadScore(grid, start):
    score = 0

    # DFS without visited nodes
    points = [start]

    while points:
        point = points.pop()
        point_height = getHeight(grid, point)
        
        for neighbor in getNeighbors(grid, point):
            neighbor_height = getHeight(grid, neighbor)

            if neighbor_height == point_height + 1:
                points.append(neighbor)

                if neighbor_height == 9:
                    score += 1

    return score
    

def getGridScore(grid):
    score = 0

    for zero in getZeros(grid):
        score += getTrailheadScore(grid, zero)
    
    return score

# Code

printGrid(height_grid)

print(getGridScore(height_grid))
