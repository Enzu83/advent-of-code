import math
from matplotlib import pyplot as plt

def next_step(position, velocity):
    # update position
    position[0] += velocity[0]
    position[1] += velocity[1]

    # update velocity
    if velocity[0] != 0: # horiztonal drag
        velocity[0] -= velocity[0] // abs(velocity[0])
    
    velocity[1] -= 1 # gravity


def get_trajectory(initial_velocity, target=None, steps=float("inf")):
    if target == None:
        target = [None, None, None, None]

    positions = [[0, 0]]
    speeds = [initial_velocity]

    position = [0, 0]
    velocity = initial_velocity[:]

    step = 0

    while step < steps and (target != None and not check_target_collision(position, target)):
        next_step(position, velocity)

        positions.append(position[:])
        speeds.append(velocity[:])

        step += 1
    
    return positions, speeds

def check_target_collision(position, target):
    x_min, x_max, y_min, y_max = target

    if x_min <= position[0] <= x_max and y_min <= position[1] <= y_max: # Square collision
        return True 
    else:
        return False

def trajectory_hit_target(trajectory, target):
    for position in trajectory[0]: 
        if check_target_collision(position, target):
            return True

    return False

def valid_initial_velocity(initial_velocity, target):
    x_min, x_max, y_min, y_max = target

    positions = [[0, 0]]
    speeds = [initial_velocity]

    position = positions[0]
    velocity = speeds[0]

    while not(position[1] < y_min and velocity[1] <= 0):
        next_step(position, velocity)

        positions.append(position[:])
        speeds.append(velocity[:])
    
    return trajectory_hit_target([positions, speeds], target)

def get_horizontal_velocity_range(target):
    speeds = []

    x_min, x_max = target[:2]

    for x in range(x_min, x_max+1):
        speed = (-1 + math.sqrt(1 + 8*x)) // 2
        speeds.append(speed)
    
    return speeds

def get_minimal_vertical_velocity(target):
    y_max = target[3]

    return (-1 + math.sqrt(1 + 8*abs(y_max))) // 2

def valid_vertical_velocity(vertical_velocity, horizontal_velocity_range, target):
    for x_speed in horizontal_velocity_range:
        if valid_initial_velocity([x_speed, vertical_velocity], target):
            return True
    
    return False

def find_maximum_height(target):
    x_min, x_max, y_min, y_max = target

    horizontal_velocity_range = get_horizontal_velocity_range(target) # all initial horizontal speeds leading to a final horizontal postion between the range of the target

    optimal_velocity = [0, 0]
    maximum_height = y_min

    y_speed = 500

    while valid_vertical_velocity(y_speed, horizontal_velocity_range, target) or y_speed < 550:
        for x_speed in horizontal_velocity_range:
            current_maximum_height = (y_speed * (y_speed + 1)) // 2

            if current_maximum_height > maximum_height:
                maximum_height = current_maximum_height
                optimal_velocity = [x_speed, y_speed]
                
        y_speed += 1

    
    return optimal_velocity, maximum_height

def max_height(v0):
    return (v0 * (v0 + 1)) / 2


def find_best_trajectory(target):
    x_min, x_max, y_min, y_max = target
    
    u_min = math.floor((1 + math.sqrt(1 + 8 * x_min)) / 2)
    u_max = math.floor((1 + math.sqrt(1 + 8 * x_max)) / 2)

    best_velocity = [0, 0]
    best_height = -float("inf")

    for u0 in range(u_min, u_max+1):
        v0 = math.floor((u0 - 1) / 2 + y_max / u0)

        while abs(v0 - u0) <= y_max - y_min:
            if valid_initial_velocity([u0, v0], target) and max_height(v0) > best_height:
                best_velocity = [u0, v0]
                best_height = max_height(v0)
            
            v0 += 1
    
    return best_velocity, best_height


def print_trajectory(trajectory, target=None):
    x_pos = [pos[0] for pos in trajectory[0]]
    y_pos = [pos[1] for pos in trajectory[0]]

    plt.scatter(x_pos, y_pos)

    if target != None:
        x_min, x_max, y_min, y_max = target

        plt.plot([x_min, x_min, x_max, x_max, x_min], [y_min, y_max, y_max, y_min, y_min], color='r')        

    plt.show()

# Code

### Conditions for hitting target ###
# old: (x_min <= (u0 * (u0 + 1)) // 2 <= x_max)
#
#   (1 + sqrt(1 + 8 * x_min**2)) / 2 <= u0 <= (1 + sqrt(1 + 8 * x_max**2)) / 2
#          (u0 - 1) / 2 + y_max / u0 <= v0 <= u0 + (y - y_min)

# test each value of u0 and v0, keep the one with the highest y

# best_vel, best_h = find_best_trajectory(target)

# print(best_vel, best_h)



# initial_velocity = [14, 71]
# trajectory = get_trajectory(initial_velocity, target, 1e+6)

# print_trajectory(trajectory, target)
# print(trajectory[0])

# print(trajectory_hit_target(trajectory, target))

#optimal_velocity, max_height = find_maximum_height(target)

#print(optimal_velocity, max_height)

#print(valid_initial_velocity([6, 11], target))