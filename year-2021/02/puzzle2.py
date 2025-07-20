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
    aim = 0

    for direction, amplitude in instructions:
        if direction == "forward":
            position[0] += amplitude
            position[1] += amplitude * aim
        elif direction == "up":
            aim -= amplitude
        elif direction == "down":
            aim += amplitude
    
    return position

# Code

horizontal_position, depth = getFinalPosition(instructions)

print(horizontal_position * depth)