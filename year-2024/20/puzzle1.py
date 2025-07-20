# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

grid = [[cell for cell in line] for line in input_data]


# Functions

def getStartEnd(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 'S':
                start = (y, x)
            elif grid[y][x] == 'E':
                end = (y, x)
    
    return start, end

def getNeighbors(grid, cell, type={'.', 'S', 'E'}):
    y, x = cell

    neighbors = set()

    if y > 0 and grid[y - 1][x] in type:
        neighbors.add((y - 1, x))
    
    if x > 0 and grid[y][x - 1] in type:
        neighbors.add((y, x - 1))
    
    if y < len(grid)-1 and grid[y + 1][x] in type:
        neighbors.add((y + 1, x))
    
    if x < len(grid[0])-1 and grid[y][x + 1] in type:
        neighbors.add((y, x + 1))

    return neighbors

def getPath(grid, start, end):
    visited = set()

    path = [start]

    while path[-1] != end:
        cell = path[-1]
        visited.add(cell)

        for neighbor in getNeighbors(grid, cell):
            if neighbor not in visited:
                path.append(neighbor)
    
    return path

def getCheatTime(grid, path, wall):
    # get the neighbors of the wall we will go through
    # then, follow the path until it mets two of the neighbors
    # the differences between their indexes in the path corresponds to the time save

    neighbors = getNeighbors(grid, wall)

    shortcut_index = None # beginning of the shortcut

    for i, cell in enumerate(path):
        if cell in neighbors:
            # get the beginning of the shortcut
            if shortcut_index is None:
                shortcut_index = i

            # when the second neighbor is found, return the time save ('-2' is the time to go through the wall)
            else:
                return (i - shortcut_index - 2)
    
    return 0

def getTimeSaves(grid):
    start, end = getStartEnd(grid)
    path = getPath(grid, start, end)

    visited_walls = set()
    time_saves = {}

    # for each path cells, test to check for each neighbors walls
    for cell in path:
        for wall in getNeighbors(grid, cell, {'#'}):
            if wall not in visited_walls:
                visited_walls.add(wall)

                time_with_cheat = getCheatTime(grid, path, wall)

                # if the cheat leads to a correct path
                if time_with_cheat > 0 and time_with_cheat not in time_saves:
                    time_saves[time_with_cheat] = 1
                
                elif time_with_cheat > 0:
                    time_saves[time_with_cheat] += 1 
    
    return time_saves

def countTimeSavesMoreThan(time_saves, threshold):
    return sum(amount for time_save, amount in time_saves.items() if time_save >= threshold)

def printPath(grid, path):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '.' and (y, x) in path:
                print('O', end="")
            else:
                print(grid[y][x], end="")
        
        print("")
    
    print("")


def timeSavesInfo(time_saves):
    for time_save in sorted(time_saves.keys()):
        if time_saves[time_save] > 1:
            print(f"There are {time_saves[time_save]} cheats that save {time_save} picoseconds.")
        else:
            print(f"There is one cheat that save {time_save} picoseconds.")


# Code

time_saves = getTimeSaves(grid)

print(countTimeSavesMoreThan(time_saves, 100))