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


# Code
pos = [0, 0]
aim = 0

for command in input_data:
    direction, amplitude = command.split(' ')
    amplitude = int(amplitude)

    if direction == "forward":
        pos[0] += amplitude
        pos[1] += amplitude * aim
    elif direction == "up":
        aim -= amplitude
    elif direction == "down":
        aim += amplitude

print(pos[0]*pos[1])
