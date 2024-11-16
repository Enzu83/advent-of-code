import numpy as np

# Custom input
input_data = """16,1,2,0,4,2,7,1,2,14"""
input_data = input_data.split(',')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data = input_data[0].split(',')


# Functions

def total_fuel(crabs, pos):
    return np.sum(abs(crabs - pos))

def sign_sum(list):
    res = 0

    for element in list:
        res += np.sign(element)

    return res

def minimum_position(crabs):
    min_pos = np.sum(crabs) / len(crabs)

    step = 0
    previous_step = 2

    while abs(abs(step) - abs(previous_step)) > 1:
        previous_step = step

        step = sign_sum(crabs - min_pos)
        min_pos += step

        print(min_pos, step)

    min_pos = round(min_pos)

    for pos in range(min_pos - round(abs(step)), min_pos + round(abs(step)) + 1):
        if total_fuel(crabs, pos) < total_fuel(crabs, min_pos):
            min_pos = pos

    return min_pos



# Formatting

crabs = np.array([int(crab) for crab in input_data])

#print(crabs)


min_pos = minimum_position(crabs)
print("Optimal position: " + str(min_pos))

used_fuel = total_fuel(crabs, min_pos)

print("Used fuel: " + str(used_fuel))