# Custom input
input_data = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""
input_data = input_data.split('\n\n')


# Input from file
input_data = open("input.txt").read()[:-1]
input_data = input_data.split('\n\n')

# Formatting

locks = set()
keys = set()

for layout in input_data:
    layout = layout.split('\n')
    heights = [sum(layout[row][col] == '#' for row in range(1, len(layout)-1)) for col in range(len(layout[0]))]
    
    if layout[0] == '#####':
        locks.add(tuple(heights))
    elif layout[-1] == '#####':
        keys.add(tuple(heights))


# Functions

def getLockKeyPairs(locks, keys):
    pairs = set()

    for lock in locks:
        for key in keys:
            if not any(lock[i] + key[i] > 5 for i in range(5)):
                pairs.add((lock, key))
    
    return len(pairs)


# Code

print(getLockKeyPairs(locks, keys))