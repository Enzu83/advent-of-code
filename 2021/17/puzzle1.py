from math import floor, ceil, sqrt
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

def next_x(x: int, u: int) -> tuple:
    return x + u, max(u - 1, 0)

def next_y(y: int, v: int) -> tuple:
    return y + v, v - 1

def x_vect(u0:int, n: int) -> int:
    if n < u0:
        x = n*u0 - (n * (n - 1)) // 2
        u = u0 - n
    else:
        x = (u0 * (u0 + 1)) // 2
        u = 0

    return x, u

def y_vect(v0:int, n: int) -> int:
    return n*v0 - (n * (n - 1)) // 2, v0 - n

def get_u0_range(target: list) -> list:
    x_min, x_max, y_min, y_max = target

    u_min = (sqrt(1 + 8*x_min) - 1) / 2
    u_max = (sqrt(1 + 8*x_max) - 1) / 2

    if ceil(u_max) == floor(u_max):
        u_max += 1

    return [k for k in range(ceil(u_min), ceil(u_max))]

def get_v0_range(target: list) -> list:
    x_min, x_max, y_min, y_max = target

    return [k for k in range(abs(y_min) + 1)]

def hit_target(x: int, y: int, target: list) -> list:
    x_min, x_max, y_min, y_max = target

    return (x_min <= x <= x_max) and (y_min <= y <= y_max)

def find_max_height(target: list) -> list:
    x_min, x_max, y_min, y_max = target

    u0_range = get_u0_range(target)

    max_height = -float("inf")


    for u0 in u0_range:
        v0 = 0
        y = 0

        while v0 < 500:
            y_at_u0, v_at_u0 = y_vect(v0, u0)
            x_at_u0 = x_vect(u0, u0)[0]

            if hit_target(x_at_u0, y_at_u0, target):
                max_height = (v0 * (v0 + 1)) // 2
            elif y_at_u0 < y_min:
                break

            x, u = 0, u0
            y, v = 0, v0

            if hit_target(x, y, target):
                max_height = (v0 * (v0 + 1)) // 2

            x, u = next_x(x, u)
            y, v = next_y(y, v)

            print(f"({u0}, {v0}): {x}, {y}")

            v0 += 1

    return max_height


    # highest_velocity = 0

    # for v0 in range(abs(y_min) + 1):
    #     print(v0)
    #     if y_max < 0:
    #         v0 *= -1

    #     y = 0

    #     while y >= y_min:
    #         if y <= y_max: #en lien avec u0 pour conconder en meme temps sur la target
    #             print('in')
    #             highest_velocity = v0
    #             break

    #         y += v0
    #         v0 -= 1
    
    # return (highest_velocity * (highest_velocity + 1)) // 2


# Code

print(find_max_height(target))
