# Custom input
input_data = """AAAA
BBCD
BBCC
EEEC"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

plants = [[plant for plant in row] for row in input_data]

# Functions

def getNeighbors(grid, point):
    neighbors = set()

    i, j = point

    if i > 0 and grid[i - 1][j] == grid[i][j]:
        neighbors.add((i - 1, j))
    
    if j > 0 and grid[i][j - 1] == grid[i][j]:
        neighbors.add((i, j - 1))
    
    if i < len(grid) - 1 and grid[i + 1][j] == grid[i][j]:
        neighbors.add((i + 1, j))
    
    if j < len(grid[0]) - 1 and grid[i][j + 1] == grid[i][j]:
        neighbors.add((i, j + 1))
    
    return neighbors

def exploreRegion(grid, start):
    region = set()

    stack = [start]

    while stack:
        point = stack.pop()
        region.add(point)

        for neighbor in getNeighbors(grid, point):
            if neighbor not in region:
                region.add(neighbor)
                stack.append(neighbor)
    
    return region

def getNextPoint(grid, current_point, visited):
    # iterate through the column
    # if there's no available point, start from the beginning of the next row
    # if there is no point, return None

    size = (len(grid), len(grid[0]))
    row, col = current_point

    while (row, col) in visited:
        if col < size[1] - 1:
            col += 1
        elif row < size[0] - 1:
            row += 1
            col = 0
        else:
            return None

    return (row, col)

def getRegions(grid):
    regions = []
    visited = set()

    current_point = getNextPoint(grid, (0, 0), visited)

    while current_point:
        region = exploreRegion(grid, current_point)
        regions.append(region)

        visited |= region

        current_point = getNextPoint(grid, current_point, visited)
     
    return regions

def getRegionFences(region):
    fences = []

    for plant in region:
        i, j = plant

        if (i - 1, j) not in region:
            fences.append((i - 1, j, "up"))
    
        if (i + 1, j) not in region:
            fences.append((i + 1, j, "down"))
        
        if (i, j - 1) not in region:
            fences.append((i, j - 1, "left"))
        
        if (i, j + 1) not in region:
            fences.append((i, j + 1, "right"))

    fences.sort() # sort the list of the fences to start from the top-left corner

    return fences

def isPartOfSide(fence, side):
    i, j, orientation = fence

    if (i - 1, j, orientation) in side:
        return True

    if (i + 1, j, orientation) in side:
        return True
    
    if (i, j - 1, orientation) in side:
        return True
    
    if (i, j + 1, orientation) in side:
        return True
    
    return False

def getRegionPrice(region):
    area = len(region)

    fences = getRegionFences(region)
    sides = []

    
    for fence in fences:
        part_of_a_side = False

        for side in sides:
            if isPartOfSide(fence, side):
                part_of_a_side = True
                side.add(fence)
                break
        
        if part_of_a_side is False:
            sides.append({fence})

    return area * len(sides)

def getTotalPrice(regions):
    return sum([getRegionPrice(region) for region in regions])

# Code

regions = getRegions(plants)

print(getTotalPrice(regions))