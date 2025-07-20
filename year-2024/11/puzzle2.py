# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

stones = {}

for stone in input_data[0].split():
    if stone not in stones:
        stones[int(stone)] = 1
    else:
        stones[int(stone)] += 1


# Functions

def splitNumber(number):
    number = str(number)
    N = len(number)

    left = int(number[:N//2])
    right = int(number[N//2:])

    return left, right

def addStones(stones, key, value):
    if key not in stones:
        stones[key] = value
    else:
        stones[key] += value

def nextStep(stones):
    new_stones = {}

    for stone, amount in stones.items():
        # rule 0 : 0 -> 1
        if stone == 0:
            addStones(new_stones, 1, amount)

        # rule 1 : even length -> splitted in two
        elif len(str(stone)) % 2 == 0:
            left, right = splitNumber(stone)

            addStones(new_stones, left, amount)
            addStones(new_stones, right, amount)
        
        # rule 2 : else -> * 2024
        else:
            addStones(new_stones, stone * 2024, amount)
    
    return new_stones
        

def countStones(stones, steps):
    for _ in range(steps):
        stones = nextStep(stones)

    return sum(stone_amount for stone_amount in stones.values())
# Code

print(countStones(stones, 75))

