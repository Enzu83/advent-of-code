import math
from matplotlib import pyplot as plt

# Custom input
input_data = """target area: x=20..30, y=-10..-5"""
input_data = input_data.split('\n')


# Input from file
# input_data = open("input.txt").read().split('\n')
# input_data.pop()


# Formatting
input_data = input_data[0][13:].split(', ')

x_min, x_max = input_data[0][2:].split('..')
y_min, y_max = input_data[1][2:].split('..')

target = [int(x_min), int(x_max)+1, int(y_min), int(y_max)+1]

# Functions

def find_max_height(target):
    x_min, x_max, y_min, y_max = target

    highest_velocity = 0

    for v0 in range(abs(y_min) + 1):
        print(v0)
        if y_max < 0:
            v0 *= -1

        y = 0

        while y >= y_min:
            if y <= y_max: #en lien avec u0 pour conconder en meme temps sur la target
                print('in')
                highest_velocity = v0
                break

            y += v0
            v0 -= 1
    
    return (highest_velocity * (highest_velocity + 1)) // 2

# Code

print(find_max_height(target))