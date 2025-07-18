# Custom input
input_data = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""
input_data = input_data.split('\n')

# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting
instructions = []
for line in input_data:
    line = line.split()
    instructions.append((line[0], int(line[1])))

# Functions
def getFinalPosition(instructions):
    position = [0, 0]

    for direction, amplitude in instructions:
        if direction == "forward":
            position[0] += amplitude
        elif direction == "up":
            position[1] -= amplitude
        elif direction == "down":
            position[1] += amplitude
    
    return position

# Code

horizontal_position, depth = getFinalPosition(instructions)

print(horizontal_position * depth)