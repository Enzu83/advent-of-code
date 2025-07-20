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

def getNextPoint(current_point, visited, max_size):
    # iterate through the column
    # if there's no available point, start from the beginning of the next row
    # if there is no point, return None

    row, col = current_point

    while (row, col) in visited:
        if col < max_size[1] - 1:
            col += 1
        elif row < max_size[0] - 1:
            row += 1
            col = 0
        else:
            return None

    return (row, col)

def getRegions(grid):
    regions = []
    visited = set()

    current_point = (0, 0)

    while current_point:
        region = exploreRegion(grid, current_point)
        regions.append(region)

        visited |= region

        current_point = getNextPoint(current_point, visited, (len(grid), len(grid[0])))
     
    return regions


def getRegionPrice(region):
    area = len(region)

    perimeter = 0

    for plant in region:
        # initially, the perimeter is 0 and increases by 1 for each direction where there isn't a neighbor
        plant_perimeter = 0

        i, j = plant

        if (i - 1, j) not in region:
            plant_perimeter += 1
    
        if (i + 1, j) not in region:
            plant_perimeter += 1
        
        if (i, j - 1) not in region:
            plant_perimeter += 1
        
        if (i, j + 1) not in region:
            plant_perimeter += 1
        

        perimeter += plant_perimeter

    return area * perimeter

def getTotalPrice(regions):
    return sum([getRegionPrice(region) for region in regions])

# Code

regions = getRegions(plants)

print(getTotalPrice(regions))