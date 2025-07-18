# Custom input
input_data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting
obstacles = set()
guard_initial_position = None

for i in range(len(input_data)):
    for j, char in enumerate(input_data[i]):
        if char == '#':
            obstacles.add((j, i))
        elif char == '^':
            guard_initial_position = (j, i)


# Functions
def getNextPosition(position, facing):
    # get offset
    if facing == 0:
        return (position[0], position[1] - 1)
    elif facing == 90:
        return (position[0] + 1, position[1])
    elif facing == 180:
        return (position[0], position[1] + 1)
    elif facing == 270:
        return (position[0] - 1, position[1])
    else:
        return None

def findNextPosition(position, facing, obstacles):

    next_position = getNextPosition(position, facing)
    
    if next_position not in obstacles:
        return next_position, facing
    else:
        return position, (facing + 90) % 360

def findPath(initial_position, grid_size, obstacles):
    # Facing % 360
    # 0: Up
    # 90: Right
    # 180: Down
    # 270: Left
    
    positions = set()

    position = initial_position
    facing = 0

    while 0 <= position[0] < grid_size[0] and 0 <= position[1] < grid_size[1]:
        positions.add(position)

        position, facing = findNextPosition(position, facing, obstacles)
    
    return positions

def checkForLoop(initial_position, grid_size, obstacles):
    # Facing % 360
    # 0: Up
    # 90: Right
    # 180: Down
    # 270: Left
    
    states = set()

    current_state = (initial_position, 0)

    while 0 <= current_state[0][0] < grid_size[0] and 0 <= current_state[0][1] < grid_size[1]:
        states.add(current_state)

        current_state = findNextPosition(current_state[0], current_state[1], obstacles)

        if current_state in states:
            return True

    return False

def findLoopObstacles(initial_position, positions, grid_size, obstacles):
    loop_obstacles = set()

    for obstacle in positions:
        if checkForLoop(initial_position, grid_size, obstacles | {obstacle}):
            loop_obstacles.add(obstacle)

    return loop_obstacles

def printPath(grid_size, obstacles, positions):
    grid = [['.'] * grid_size[1] for _ in range(grid_size[0])]

    for position in positions:
        grid[position[1]][position[0]] = 'X'
    
    for obstacle in obstacles:
        grid[obstacle[1]][obstacle[0]] = '#'
    
    for line in grid:
        for char in line:
            print(char, end="")
        print("")

# Code

grid_size = (len(input_data), len(input_data[0]))

# get the path of the guard
guard_positions = findPath(guard_initial_position, grid_size, obstacles)

# place an obstacle for each position and check if the guard is stuck in a loop

loop_obstacles = findLoopObstacles(guard_initial_position, guard_positions, grid_size, obstacles)

print(len(loop_obstacles))