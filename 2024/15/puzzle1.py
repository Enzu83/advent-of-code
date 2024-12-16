# Custom input
input_data = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

# 0: Empty
# 1: Wall
# 2: Box
# 3: Robot
grid = []

sequence = []

for row in input_data:
    # grid
    if len(row) > 0 and row[0] not in {'<', '>', '^', 'v'}:
        grid.append([])

        for cell in row:
            if cell == '.':
                grid[-1].append(0)
            
            elif cell == '#':
                grid[-1].append(1)
            
            elif cell == 'O':
                grid[-1].append(2)
            
            elif cell == '@':
                grid[-1].append(3)
    
    # instructions
    elif len(row) > 0:
        for movement in row:
            if movement == '<':
                sequence.append((0, -1))
            
            elif movement == '>':
                sequence.append((0, 1))
            
            elif movement == '^':
                sequence.append((-1, 0))
            
            elif movement == 'v':
                sequence.append((1, 0))


# Functions

def findRobot(grid):
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 3:
                return x, y
    
    return None


def move(grid, x, y, dx, dy):
    # (x, y): original cell position
    # (dx, dy): movement that needs no be checked if it's possible

    next_cell = grid[x + dx][y + dy]

    # empty: can directly be shifted
    if next_cell == 0:
        grid[x + dx][y + dy] = grid[x][y] # shift the guard cell
        grid[x][y] = 0 # the original cell is now empty

        return True

    # wall: no movement possible
    if next_cell == 1:
        return False
    
    # box: need to check if the box that is pushed can also be pushed
    if move(grid, x + dx, y + dy, dx, dy):
        grid[x + dx][y + dy] = grid[x][y] # shift the cell
        grid[x][y] = 0 # the original cell is now empty

        return True
    
    return False

def computeMovement(grid, sequence):
    robot_x, robot_y = findRobot(grid)

    for movement in sequence:
        # check if the robot has moved : if then, update its position
        if move(grid, robot_x, robot_y, movement[0], movement[1]):
            robot_x += movement[0]
            robot_y += movement[1]


def getBoxSum(grid):
    return sum(100 * x + y for x in range(len(grid)) for y in range(len(grid[0])) if grid[x][y] == 2)


def printGrid(grid):
    for row in grid:
        for cell in row:
            if cell == 0:
                print('.', end="")
        
            elif cell == 1:
                print('#', end="")
            
            elif cell == 2:
                print('O', end="")
            
            elif cell == 3:
                print('@', end="")
        
        print("")
    
    print("")


# Code

printGrid(grid)
computeMovement(grid, sequence)
printGrid(grid)

print(getBoxSum(grid))