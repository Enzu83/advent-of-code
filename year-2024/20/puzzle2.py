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

    if y > 1 and grid[y - 1][x] in type:
        neighbors.add((y - 1, x))
    
    if x > 1 and grid[y][x - 1] in type:
        neighbors.add((y, x - 1))
    
    if y < len(grid)-2 and grid[y + 1][x] in type:
        neighbors.add((y + 1, x))
    
    if x < len(grid[0])-2 and grid[y][x + 1] in type:
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

def getTimeSaves(grid, cheat_duration):
    start, end = getStartEnd(grid)
    path = getPath(grid, start, end)
    path_index = {cell: i for i, cell in enumerate(path)} # get the path index of cell

    time_saves = {}

    # for each path cells, test to check for each neighbors walls
    for index, cell in enumerate(path):
        cell_time_saves = {}
        visited = set() # cells explored during the cheat

        # bfs while the cheat is still active
        queue = [(cell, cheat_duration - 1)]

        while queue:
            current, cheat = queue.pop(0)
            visited.add(current)

            for neighbor in getNeighbors(grid, current, {'.', '#', 'S', 'E'}):
                # add neighbor for the bfs
                if neighbor not in visited and cheat > 0:
                    visited.add(neighbor)
                    queue.append((neighbor, cheat - 1))

                # found a cell that is in path : update the time save if it's better
                if grid[neighbor[0]][neighbor[1]] != '#':
                    time_save = path_index[neighbor] - index - (cheat_duration - cheat)

                    # only keep the best time save for each cell in path
                    if time_save > 0 and neighbor not in cell_time_saves:
                        cell_time_saves[neighbor] = time_save
                    
                    elif neighbor in cell_time_saves and time_save > cell_time_saves[neighbor]:
                        cell_time_saves[neighbor] = time_save 
        
        # after the bfs, add the best time saves of each cell in path that was reached with the cheat
        for time_save in cell_time_saves.values():
            if time_save not in time_saves:
                time_saves[time_save] = 1
            else:
                time_saves[time_save] += 1
    
    return time_saves

def countTimeSavesMoreThan(time_saves, threshold):
    return sum(amount for time_save, amount in time_saves.items() if time_save >= threshold)

def printPath(grid, path):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (y, x) in path:
                print('O', end="")
            else:
                print(grid[y][x], end="")
        
        print("")
    
    print("")

def timeSavesInfo(time_saves, minimum_time_save=0):
    for time_save in sorted(time_saves.keys()):
        if time_save >= minimum_time_save:
            if time_saves[time_save] > 1:
                print(f"There are {time_saves[time_save]} cheats that save {time_save} picoseconds.")
            else:
                print(f"There is one cheat that save {time_save} picoseconds.")


# Code

time_saves = getTimeSaves(grid, 20)

# timeSavesInfo(time_saves, 100)

print(countTimeSavesMoreThan(time_saves, 100))


