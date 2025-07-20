import numpy as np

# Input from file
input_data = open("input.txt").read().split('\n')
input_data = input_data[0].split(',')


# Functions

def total_fuel(crabs, pos):
    used_fuel = 0

    for crab in crabs:
        used_fuel += abs(crab - pos) * (abs(crab - pos) + 1) // 2

    return used_fuel

def sign_sum(list):
    res = 0

    for element in list:
        res += np.sign(element)

    return res

def minimum_position(crabs):
    min_pos = 1 + 2 * np.sum(crabs) / len(crabs)

    step = 0
    previous_step = 2

    while abs(abs(step) - abs(previous_step)) > 1:
        previous_step = step

        step = 1 + 2 * np.sum(crabs - min_pos) / len(crabs)
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