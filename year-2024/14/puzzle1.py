# Custom input
input_data = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

robots = []

for line in input_data:
    position, velocity = line.split()

    position = list(map(int, position[2:].split(',')))
    velocity = tuple(map(int, velocity[2:].split(',')))

    robots.append([position, velocity])

# Functions

def updateRobots(robots, steps, grid_size):
    for i, robot in enumerate(robots):
        x_position, y_position = robot[0]

        x_position = (x_position + robot[1][0] * steps) % grid_size[0]
        y_position = (y_position + robot[1][1] * steps) % grid_size[1]

        robots[i][0] = [x_position, y_position]

def getRobotsInQuadrants(robots, grid_size):
    # grid width and height are odds
    n, m = grid_size[0] // 2, grid_size[1] // 2

    quadrants = [0] * 4

    for robot in robots:
        x, y = robot[0]

        # top left
        if x < n and y < m:
            quadrants[0] += 1

        elif x > n and y < m:
            quadrants[1] += 1
        
        elif x < n and y > m:
            quadrants[2] += 1
        
        elif x > n and y > m:
            quadrants[3] += 1

    return quadrants


def printRobots(robots, grid_size):
    grid = [[0 for _ in range(grid_size[0])] for _ in range(grid_size[1])]

    for robot in robots:
        x, y = robot[0]

        grid[y][x] += 1
    
    # print
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                print('.', end="")
            else:
                print(grid[i][j], end="")
            
        print("")
    
    print("")

 
# Code

grid_size = (101, 103)

updateRobots(robots, 100, grid_size)

quadrants = getRobotsInQuadrants(robots, grid_size)

print(quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3])