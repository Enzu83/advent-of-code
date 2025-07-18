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
                grid[-1].append(0)
            
            elif cell == '#':
                grid[-1].append(1)
                grid[-1].append(1)
            
            elif cell == 'O':
                grid[-1].append(2)
                grid[-1].append(4)
            
            elif cell == '@':
                grid[-1].append(3)
                grid[-1].append(0)
    
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

def moveBox(grid, x, y, dx, dy, size):
    # (x, y): left box position
    # (dx, dy): movement that needs no be checked if it's possible
    # size: size of the box

    next_cells = [grid[x + dx][y + i + dy] for i in range(size)]

    # empty: can directly be shifted
    if all(cell == 0 for cell in next_cells):
        for i in range(size):
            grid[x + dx][y + i + dy] = grid[x][y + i] # shift the cell
            grid[x][y + i] = 0 # original cell empty

        return True

    # wall: no movement possible
    if any(cell == 1 for cell in next_cells):
        return False


    # try to push a 2-cells box with up or down movement (due to the function move())
    # check if it's one or two boxes, and which part is pushed, there are 4 cases:
    # one box aligned with the current one / only one box on the left side / only one box on the right side / 2 boxes on both sides

    # relative position of the next box
    next_box_left = -1
    next_box_right = size

    while grid[x + dx][y + next_box_left + dy] != 2:
        next_box_left += 1
    
    while grid[x + dx][y + next_box_right + dy] != 4:
        next_box_right -= 1

    if moveBox(grid, x + dx, y + next_box_left + dy, dx, dy, next_box_right - next_box_left + 1):
        for i in range(size):
            grid[x + dx][y + i + dy] = grid[x][y + i] # shift the cell
            grid[x][y + i] = 0 # original cell empty

        return True

    return False

def move(grid, x, y, dx, dy):
    # (x, y): original cell position
    # (dx, dy): movement that needs no be checked if it's possible

    next_cell = grid[x + dx][y + dy]

    # empty: can directly be shifted
    if next_cell == 0:
        grid[x + dx][y + dy] = grid[x][y] # shift the cell
        grid[x][y] = 0 # the original cell is now empty

        return True

    # wall: no movement possible
    if next_cell == 1:
        return False
    
    # 2-cells box: both parts of the box need to be able to be pushed

    # left or right movement : nothing changes from part 1
    if dx == 0:
        if move(grid, x + dx, y + dy, dx, dy):
            grid[x + dx][y + dy] = grid[x][y] # shift the cell
            grid[x][y] = 0 # the original cell is now empty

            return True
    
        return False

    # up or down movement: need to do the recursion for both '[' and ']'
    else:
        y_shift = 0

        # always check for the left part '['
        if next_cell == 4:
            y_shift = -1

        if moveBox(grid, x + dx, y + y_shift + dy, dx, dy, 2):
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
                print('[', end="")
            
            elif cell == 4:
                print(']', end="")
            
            elif cell == 3:
                print('@', end="")
        
        print("")
    
    print("")

# Code

printGrid(grid)
computeMovement(grid, sequence)
printGrid(grid)

print(getBoxSum(grid))
